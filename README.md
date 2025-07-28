# scrapy_curl_cffi

scrapy+curl_cffi

### 配置

```python
COMPRESSION_ENABLED = False
DOWNLOAD_HANDLERS = {
    "http": "scrapy_curl_cffi.downloader.HTTPDownloadHandler",
    "https": "scrapy_curl_cffi.downloader.HTTPDownloadHandler",
}
USER_AGENT = None
```

### 设置指定的浏览器

```python
DOWNLOAD_IMPERSONATES = ["chrome133a"]
DOWNLOAD_IMPERSONATE_RANDOM = True # 是否自动随机选择一个模拟浏览器, 如果设置了DOWNLOAD_IMPERSONATES, 则此配置项无效
DOWNLOAD_IMPERSONATE_TYPE = "pc"  # pc, mobile, both 如果设置了DOWNLOAD_IMPERSONATES, 则此配置项无效
```

```python
# Edge
    "edge99",
    "edge101",
    # Chrome
    "chrome99",
    "chrome100",
    "chrome101",
    "chrome104",
    "chrome107",
    "chrome110",
    "chrome116",
    "chrome119",
    "chrome120",
    "chrome123",
    "chrome124",
    "chrome131",
    "chrome133a",
    "chrome136",
    "chrome99_android",
    "chrome131_android",
    # Safari
    "safari153",
    "safari155",
    "safari170",
    "safari172_ios",
    "safari180",
    "safari180_ios",
    "safari184",
    "safari184_ios",
    "safari260",
    "safari260_ios",
    # Firefox
    "firefox133",
    "firefox135",
    "tor145",
    # alias
    "chrome",
    "edge",
    "safari",
    "safari_ios",
    "safari_beta",
    "safari_ios_beta",
    "chrome_android",
    "firefox",
```
