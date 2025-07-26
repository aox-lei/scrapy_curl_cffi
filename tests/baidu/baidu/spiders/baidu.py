import json
import scrapy


class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]

    def start_requests(self):
        params = {"aaaa": "bbbb"}
        headers = {"Content-Type": "application/json"}
        yield scrapy.Request(
            url="https://www.baidu.com",
            callback=self.parse,
            method="POST",
            body=json.dumps(params),
            headers=headers,
            meta={"_proxy": "http://aaa:bbb@127.0.0.1:8900"},
        )

    def parse(self, response):
        pass
