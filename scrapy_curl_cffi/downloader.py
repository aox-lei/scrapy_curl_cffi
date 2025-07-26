"""Download handlers for http and https schemes"""

from __future__ import annotations

import asyncio
import ipaddress
import logging
import random
from time import time
from typing import TYPE_CHECKING, TypeVar
from urllib.parse import urldefrag

from twisted.internet.defer import Deferred

from scrapy import Request, Spider
from scrapy.http import Headers, Response
from scrapy.responsetypes import responsetypes
from curl_cffi import Response as TxResponse, AsyncSession

if TYPE_CHECKING:
    # typing.NotRequired and typing.Self require Python 3.11
    from typing_extensions import Self

    from scrapy.crawler import Crawler
    from scrapy.settings import BaseSettings


logger = logging.getLogger(__name__)

_T = TypeVar("_T")


class HTTPDownloadHandler:
    lazy = False
    session_handler: AsyncSession

    def __init__(self, settings: BaseSettings, crawler: Crawler):
        self._crawler = crawler

        self.session_handler = AsyncSession()

        self._default_maxsize: int = settings.getint("DOWNLOAD_MAXSIZE")
        self._default_warnsize: int = settings.getint("DOWNLOAD_WARNSIZE")
        self._fail_on_dataloss: bool = settings.getbool("DOWNLOAD_FAIL_ON_DATALOSS")
        self._impersonates: list[str] = settings.getlist("DOWNLOAD_IMPERSONATES")

    @classmethod
    def from_crawler(cls, crawler: Crawler) -> Self:
        settings = crawler.settings
        return cls(settings, crawler)

    def download_request(self, request: Request, spider: Spider) -> Deferred[Response]:
        """Return a deferred for the HTTP download"""
        agent = ScrapyAgent(
            session=self.session_handler,
            maxsize=getattr(spider, "download_maxsize", self._default_maxsize),
            warnsize=getattr(spider, "download_warnsize", self._default_warnsize),
            crawler=self._crawler,
            impersonates=self._impersonates,
        )
        return agent.download_request(request)

    def close(self) -> Deferred[None]:
        d = Deferred.fromFuture(asyncio.ensure_future(self.session_handler.close()))
        return d


class ScrapyAgent:
    def __init__(
        self,
        *,
        session: AsyncSession,
        connectTimeout: float = 10,
        maxsize: int = 0,
        warnsize: int = 0,
        fail_on_dataloss: bool = True,
        impersonates: list[str] = [],
        crawler: Crawler,
    ):
        self._connectTimeout: float = connectTimeout
        self._session = session
        self._maxsize: int = maxsize
        self._warnsize: int = warnsize
        self._fail_on_dataloss: bool = fail_on_dataloss
        self._impersonates: list[str] = impersonates
        self._crawler: Crawler = crawler

    async def _download_request(self, request: Request):
        timeout = request.meta.get("download_timeout") or self._connectTimeout

        method = request.method.upper()
        url = urldefrag(request.url)[0]
        body = request.body or None

        response = await self._session.request(
            method=method,  # type:ignore[arg-type]
            url=url,
            impersonate=self._get_impersonate(request),  # type:ignore[arg-type]
            proxy=request.meta.get("_proxy"),
            timeout=timeout,
            headers=request.headers.to_unicode_dict(),
            data=body,
            verify=False,
        )
        return response

    def _get_impersonate(self, request: Request) -> str | None:
        impersonate = request.meta.get("download_impersonate")
        if impersonate is None:
            if self._impersonates:
                impersonate = random.choice(self._impersonates)
        return impersonate

    def download_request(self, request: Request) -> Deferred[Response]:
        # TODO: 处理请求
        # request details
        url = urldefrag(request.url)[0]
        start_time = time()
        # set download latency
        d = Deferred.fromFuture(asyncio.ensure_future(self._download_request(request)))
        d.addCallback(self._cb_latency, request, start_time)
        d3: Deferred[Response] = d.addCallback(self._cb_bodydone, request, url)
        # check download timeout
        return d3

    def _cb_latency(self, result: _T, request: Request, start_time: float) -> _T:
        request.meta["download_latency"] = time() - start_time
        return result

    @staticmethod
    def _headers_from_twisted_response(response: TxResponse) -> Headers:
        headers = Headers()
        headers.update(response.headers)
        return headers

    def _cb_bodydone(
        self, txresponse: TxResponse, request: Request, url: str
    ) -> Response:
        headers = self._headers_from_twisted_response(txresponse)
        respcls = responsetypes.from_args(
            headers=headers, url=url, body=txresponse.content
        )
        print(txresponse.http_version)
        protocol = "http/1.1"
        if txresponse.http_version == 2:
            protocol = "http/2.0"
        ip_address = None
        try:
            ip_address = ipaddress.ip_address(txresponse.primary_ip)
        except ValueError:
            pass

        response = respcls(
            url=url,
            status=int(txresponse.status_code),
            headers=headers,
            body=txresponse.content,
            flags=request.flags,
            certificate=None,
            ip_address=ip_address,
            protocol=protocol,
        )
        return response
