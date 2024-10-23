import requests
from bs4 import BeautifulSoup
import csv
import time

class HuggingFaceModel:
    def __init__(self, name, likes, downloads, size, tensor_type):
        self.name = name
        self.likes = likes
        self.downloads = downloads
        self.size = size
        self.tensor_type = tensor_type

    def to_dict(self):
        return {
            'Name': self.name,
            'Likes': self.likes,
            'Downloads': self.downloads,
            'Size': self.size,
            'Tensor Type': self.tensor_type
        }

    @classmethod
    def from_article(cls, article):
        name = article.find('h4').text.strip() if article.find('h4') else 'N/A'
        
        stats = article.find_all('span', class_='font-semibold')
        likes = stats[0].text.strip() if len(stats) > 0 else 'N/A'
        downloads = stats[1].text.strip() if len(stats) > 1 else 'N/A'
        
        details = article.find_all('div', class_='truncate')
        size = details[0].text.strip() if len(details) > 0 else 'N/A'
        tensor_type = details[1].text.strip() if len(details) > 1 else 'N/A'
        
        return cls(name, likes, downloads, size, tensor_type)

def scrape_huggingface_models(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    models = []
    
    for article in soup.find_all('article', class_='overview-card-wrapper'):
        try:
            model = HuggingFaceModel.from_article(article)
            models.append(model)
        except Exception as e:
            print(f"处理模型时出错: {e}")
            continue
    
    return models

def save_to_csv(models, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Likes', 'Downloads', 'Size', 'Tensor Type'])
        writer.writeheader()
        writer.writerows(model.to_dict() for model in models)

if __name__ == '__main__':
    sort_by = 'likes'
    pipeline_tag = 'text-generation'
    base_url = f'https://huggingface.co/models?pipeline_tag={pipeline_tag}&sort={sort_by}&p='
    all_models = []
    
    for page in range(5):
        url = base_url + str(page)
        print(f'正在爬取第 {page+1} 页...')
        try:
            models = scrape_huggingface_models(url)
            all_models.extend(models)
            print(f'成功从第 {page+1} 页爬取了 {len(models)} 个模型')
            time.sleep(2)
        except Exception as e:
            print(f"爬取第 {page+1} 页时出错: {e}")
    
    if all_models:
        save_to_csv(all_models, 'huggingface_text_generation_models.csv')
        print(f'已成功爬取 {len(all_models)} 个模型的数据并保存到 CSV 文件中。')
    else:
        print('未能成功爬取任何模型数据。')