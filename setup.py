from setuptools import setup, find_packages

setup(
    name="scrapy_curl_cffi",  # 库的名称
    version="0.1.2",  # 版本号
    author="Spencer",
    author_email="aox.kei@gmail.com",
    description="A Downloader for Scrapy",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/aox-lei/scrapy_curl_cffi",  # 项目主页
    packages=find_packages(),  # 自动查找所有包
    install_requires=[
        # 列出依赖，例如 "numpy>=1.18.0"
        "curl-cffi>=0.12.0",
        "scrapy>=2.13.3",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",  # 指定支持的 Python 版本
)
