from parsers.base_resource import BaseResource
from bs4 import BeautifulSoup
import json
import re


class RosCarServisResource(BaseResource):
    MAIN_URL = 'https://roscarservis.ru'

    def get_tires_urls(self):
        url = (f'{self.MAIN_URL}/catalog/legkovye/?arCatalogFilter_458_1500340406=Y&'
               f'set_filter=Y&sort%5Brecommendations%5D=asc&PAGEN_1=67')
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        pg_count = soup.find("form", class_="form").get("action").split("=")

        count = int(pg_count[-1])

        tires_urls_list = []
        for i in range(1, count + 1):
            url = (f"{self.MAIN_URL}/catalog/legkovye/?arCatalogFilter_458_1500340406=Y&"
                   f"set_filter=Y&sort%5Brecommendations%5D=asc&PAGEN_1={i}")
            req = self.session.get(url)

            soup = BeautifulSoup(req.text, "lxml")
            tires_cards = soup.find_all("a", class_="product__name")

            for item in tires_cards:
                if item.get('href'):
                    tires_url = f'{self.MAIN_URL}{item.get("href")}'
                    tires_urls_list.append(tires_url)
                    if len(tires_urls_list) >= self.args.count:
                        return tires_urls_list
        return tires_urls_list

    def parse(self):
        tires_urls_list = self.get_tires_urls()
        tires_list_result = []
        for url in tires_urls_list:
            req = self.session.get(url)

            try:
                soup = BeautifulSoup(req.text, "lxml")
                tires_name = soup.find("div", class_="product-screen__name").find("p").text
                tires_img = self.MAIN_URL + soup.find("div", class_="swiper-slide").find("img").get("src")
                tires_price = ''
                t = re.search(r'PRICE&quot;:&quot;(\d+.\d+)&quot;,&quot;PRICE_ID', req.text)
                if t:
                    tires_price = t.group(1)

                tires_about = soup.find("div", class_="product-desc__item fadeInUp").text
                tires_about = " ".join(tires_about.split()).replace(".", ":")

                tires_list_result.append(
                    {
                        "Название шин": tires_name,
                        "Цена за одну": tires_price,
                        "Характеристики": tires_about,
                        "Изображение": tires_img,
                    }
                )

            except Exception as e:
                self.logger.error(e)
                self.logger.error(e)("Damn...There was some error...")

        with open("./data/roscarservis/tires_list_result.json", "a", encoding="utf-8") as file:
            json.dump(tires_list_result, file, indent=4, ensure_ascii=False)
        return tires_list_result
