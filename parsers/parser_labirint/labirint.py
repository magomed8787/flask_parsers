from parsers.base_resource import BaseResource
from bs4 import BeautifulSoup
import csv
import json


class LabirintResource(BaseResource):
    MAIN_URL = 'https://www.labirint.ru'

    def get_books_urls(self, total_pages):
        ret = []
        for i in range(1, total_pages + 1):
            url = f'{self.MAIN_URL}/genres/1850/?page={i}'
            req = self.session.get(url)
            soup = BeautifulSoup(req.text, 'lxml')

            books_cards = (soup.find_all('div', class_='genres-carousel__container products-row')[1].
                           find_all('a', class_='cover'))

            for item in books_cards:
                if item.get('href'):
                    book_url = f'{self.MAIN_URL}' + item.get('href')
                    ret.append(book_url)
                    if len(ret) >= self.args.count:
                        return ret
        return ret

    def parse(self):
        with open(f'./data/labirint/labirint.csv', 'w', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow(
                (
                    'Автор и название книги',
                    'Издательство',
                    'Цена',
                    'Скидка',
                )
            )

        url = f'{self.MAIN_URL}/genres/1850/?page=1'
        r = self.session.get(url)
        soup = BeautifulSoup(r.text, 'lxml')

        pg_count = (soup.find('div', class_='pagination-number__right').
                    find('a', class_='pagination-number__text').text)
        total_pages = int(pg_count)

        books_urls_list = self.get_books_urls(total_pages)

        books_list = []
        for url in books_urls_list:
            req = self.session.get(url)
            soup = BeautifulSoup(req.text, 'lxml')

            try:
                book_author_name = soup.find('div', class_='prodtitle').find('h1').text
            except Exception as e:
                book_author_name = 'Нет автора'
                self.logger.debug(e)

            try:
                book_price = (soup.find('div', class_='buying-price').
                              find('span', class_='buying-price-val-number').text)
            except Exception as e:
                book_price = 'скидка'
                self.logger.debug(e)

            try:
                book_publisher = soup.find('div', class_='publisher').text.replace('Издательство: ', '')

            except Exception as e:
                book_publisher = 'нет издательства'
                self.logger.debug(e)

            try:
                book_new_price = soup.find('div', class_='buying-pricenew-val').find('span').text
                book_old_price = soup.find('div', class_='buying-priceold-val').find('span').text
                book_price = book_new_price + f'. Старая цена: {book_old_price}'
                book_sale = soup.find('span', class_='action-label__text').text
            except Exception as e:
                book_sale = 'нет скидки'
                self.logger.debug(e)

            books_list.append(
                {
                    'Автор и название книги': book_author_name,
                    'Издательство': book_publisher,
                    'Цена': book_price,
                    'Скидка': book_sale,
                }
            )

            with open(f'./data/labirint/labirint.csv', 'a', encoding='utf-8') as file:
                writer = csv.writer(file)

                writer.writerow(
                    (
                        book_author_name,
                        book_publisher,
                        book_price,
                        book_sale
                    )
                )

        with open(f'./data/labirint/books_list_result.json', 'a', encoding='utf-8') as file:
            json.dump(books_list, file, indent=4, ensure_ascii=False)

        return books_list
