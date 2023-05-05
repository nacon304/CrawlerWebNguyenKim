import json
import math
import scrapy
from quotes_js_scraper.items import QuoteItem
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlencode
import requests

class WebCrawlerSpider(scrapy.Spider):
    name = 'PhongVuCrawler'

    def start_requests(self):
        crawler_search_url = 'https://phongvu.vn/sitemap_seller_categories_NH01.xml'
        yield SeleniumRequest(url=crawler_search_url, callback=self.parse_search_results, wait_time=10)

    def parse_search_results(self, response):
        url_products  = response.css('div.folder > div.opened > div:nth-child(2) > span:nth-child(2)::text').getall()
        if url_products is not None:
            lenn = 1600
            maxx = lenn * 0
            for i in range(1, len(url_products), 2):
                url = url_products[i]
                if i >= maxx and i < maxx + lenn:
                    # print(url)
                    yield SeleniumRequest(url=url, callback=self.parse_product_data, wait_time=10, wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '#__NEXT_DATA__')), meta={'url': url})

            # yield SeleniumRequest(url=crawler_product_url, callback=self.parse_product_data, wait_time=10, wait_until=EC.presence_of_element_located((By.CSS_SELECTOR, '#root > script:nth-child(4)')), meta={'url': crawler_product_url})

            # # Request Next Page
            # if page == 1:
            #     max_pages = json_blob["props"]["initialState"]["catalog"]["paging"]["last_page"]
            #     # if max_pages > 10:
            #     #     max_pages = 10
            #     for p in range(2, 5):
            #         payload = {'sort': 'newest', 'page': p}
            #         crawler_search_url = 'https://tiki.vn/' + keyword + '?' + urlencode(payload)
            #         yield SeleniumRequest(url=crawler_search_url, callback=self.parse_search_results, wait_time=0.5, meta={'keyword': keyword, 'page': p})

    def parse_product_data(self, response):
        detail_product = json.loads(response.css('#__NEXT_DATA__::text').get())
        # print(detail_product['additionalProperty'][8]['value'])
        data = {
            'Url': response.meta['url'],
            'Name': detail_product['props']['pageProps']['serverProduct']['product']['productInfo']['displayName'],
            'Price': detail_product['props']['pageProps']['serverProduct']['priceAndPromotions']['price'],
            'Original_Price': detail_product['props']['pageProps']['serverProduct']['priceAndPromotions']['supplierRetailPrice'],
            'Type': 'Laptop',
            'Imgs': [sub['url'] for sub in detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['images']],
            'Desc': [
                {
                    'CPU': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][8]['value'],
                    'OCung': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][12]['value'],
                    'RAM': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][10]['value'],
                    'Card': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][9]['value'],
                    'ManHinh': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][11]['value'],
                    'HDH': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][19]['value'],
                    'KT&KL': detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][20]['value'] + ', ' + detail_product['props']['pageProps']['serverProduct']['product']['productDetail']['attributeGroups'][22]['value']
                }
            ]
        }
        # upload caterogy
        record = data.copy()
        record['Name'] = record['Name'].split(' (')[0].replace("Laptop ", "")
        record['Desc'] = record['Desc'][0]
        record['Price'] = json.dumps(record['Price'])
        record.pop('Original_Price')
        response = requests.post('https://mmt-main-dbserver.vercel.app/api/category', json=record)
        print(record)
        print(response)
        print(response.content)
         
        # upload product
        record1 = data.copy()
        record1['NameCategory'] = record1['Name'].split(' (')[0]
        record1['Price'] = json.dumps(record1['Price'])
        record1['OriginalPrice'] = json.dumps(record1['Original_Price'])
        record1.pop('Desc')
        record1.pop('Original_Price')
        response = requests.post('https://mmt-main-dbserver.vercel.app/api/product', json=record1)
        print(record1)
        print(response)
        print(response.content)
        return 

# scrapy crawl PhongVuCrawler -o outputFull.json