import json
import scrapy


class BaiduSpider(scrapy.Spider):
    name = "baidu"

    async def start(self):
        headers = {
            "Referer": "https://www.amazon.com",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36"
        }
        yield scrapy.Request(
            url="https://www.amazon.com",
            callback=self.parse,
            headers=headers,
            meta={"_proxy": "http://aaa:bbb@127.0.0.1:8900"},
        )

    def parse(self, response):
        pass
