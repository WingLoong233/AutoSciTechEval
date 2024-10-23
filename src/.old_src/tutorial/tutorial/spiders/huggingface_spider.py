import scrapy
from scrapy.crawler import CrawlerProcess

class HuggingFaceModel(scrapy.Item):
    model_id = scrapy.Field()
    name = scrapy.Field()
    likes = scrapy.Field()

class HuggingFaceSpider(scrapy.Spider):
    name = 'huggingface'
    
    def __init__(self, pipeline_tag='text-generation', sort_by='likes', pages=1, *args, **kwargs):
        super(HuggingFaceSpider, self).__init__(*args, **kwargs)
        self.pipeline_tag = pipeline_tag
        self.sort_by = sort_by
        self.pages = int(pages)
        self.start_urls = [f'https://huggingface.co/models?pipeline_tag={self.pipeline_tag}&sort={self.sort_by}&p={p}' for p in range(self.pages)]

    def parse(self, response):
        for article in response.css('article.overview-card-wrapper'):
            model_id = article.css('a::attr(href)').get().strip('/')
            model_url = f'https://huggingface.co/{model_id}'
            
            yield scrapy.Request(model_url, callback=self.parse_model_details, meta={'model_id': model_id})

    def parse_model_details(self, response):
        model = HuggingFaceModel()
        model['model_id'] = response.meta['model_id']
        
        # 提取模型名称
        name_parts = response.css('h1 a.font-mono::text').getall()
        model['name'] = '/'.join(name_parts).strip()
        
        # 提取点赞数
        # likes = response.css('button.flex.items-center.border-l::text').get()
        likes = response.css('h1 button.flex.items-center.border-l::text').get()
        model['likes'] = likes.strip() if likes else 'N/A'
        
        yield model

if __name__ == '__main__':
    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'huggingface_models_detailed.csv',
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    })

    process.crawl(HuggingFaceSpider)
    process.start()
