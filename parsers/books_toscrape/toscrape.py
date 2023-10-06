import requests
import json
from parsers.base_resource import BaseResource
from bs4 import BeautifulSoup


class ToScrapeResource(BaseResource):
    MAIN_URL = 'http://books.toscrape.com'

    def parse(self):
        project_data_list = []
        q = requests.get(self.MAIN_URL)
        soup = BeautifulSoup(q.text, 'lxml')
        count = soup.find('ul', class_="pager").find("li", class_="current").text.split()
        count = int(count[-1]) #Количество страниц пагинации

        for i in range(self.args.pages_count):
            self.logger.info(f'Parsing page {i+1}')
            url = f'{self.MAIN_URL}/catalogue/page-{i+1}.html'
            req = self.session.get(url)
            soup = BeautifulSoup(req.text, "lxml")
            articles = soup.find_all("article", class_="product_pod")
            count -= 1
            if count == -1:
                break

            project_urls = []
            for article in articles:  # Формирую список ссылок
                project_url = self.MAIN_URL + '/catalogue/' + article.find("h3").find("a").get("href")
                project_urls.append(project_url)

            for project_url in project_urls:
                req = self.session.get(project_url)
                soup = BeautifulSoup(req.text, "lxml")
                project_data = soup.find("div", class_="container-fluid page")

                try:
                    project_logo = url + project_data.find("div", class_="item active").find("img").get("src")
                except Exception as e:
                    project_logo = "No project logo"
                    self.logger.debug(e)
                #
                try:
                    project_name = project_data.find("div", class_="col-sm-6 product_main").find("h1").text
                except Exception as e:
                    project_name = "No project name"
                    self.logger.debug(e)
                #
                try:
                    product_price = (project_data.find("div", class_="col-sm-6 product_main").
                                     find("p", class_="price_color").text)
                except Exception as e:
                    product_price = "No price"
                    self.logger.debug(e)
                #
                try:
                    product_stock = (project_data.find("div", class_="col-sm-6 product_main").
                                     find("p", class_="instock availability").text.strip())
                except Exception as e:
                    product_stock = "No stock"
                    self.logger.debug(e)
                #
                try:
                    product_description = project_data.find(text="Product Description").find_next().text
                except Exception as e:
                    product_description = "No Description"
                    self.logger.debug(e)

                #
                project_data_list.append(
                    {
                        "Название книги": project_name,
                        "Обложка книги": project_logo,
                        "Стоимость книги": product_price,
                        "Книг в наличии": product_stock,
                        "Описание книги": product_description.strip(),
                    }
                )
        with open(f"./data/toscrape/books_list_result.json", "a", encoding="utf-8") as file:
            json.dump(project_data_list, file, indent=4, ensure_ascii=False)

        return project_data_list
