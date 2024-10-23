@echo off
cd /d %~dp0
scrapy crawl huggingface -L DEBUG -o huggingface_models_detailed.csv
pause