from parsers.base_resource import BaseResource
from bs4 import BeautifulSoup
import json

class BundesResource(BaseResource):
    MAIN_URL = 'https://www.bundestag.de'

    def get_persons(self):
        persons_urls = []
        for i in range(0, 749, 12):
            if len(persons_urls) >= self.args.count:
                break
            url = f'{self.MAIN_URL}/ajax/filterlist/en/members/863330-863330?limit=12&noFilterSet=true&offset={i}'

            q = self.session.get(url)
            result = q.content

            soup = BeautifulSoup(result, 'lxml')
            divs = soup.find_all('div', class_='bt-slide-content')

            for div in divs:
                persons_urls.append(div.find('a')['href'])
        return persons_urls[:self.args.count]

    def parse(self):
        data = []
        persons = self.get_persons()

        for person_data in persons:
            q = self.session.get(person_data)
            result = q.content

            soup = BeautifulSoup(result, 'lxml')

            person = soup.find('div', class_='col-xs-8 col-md-9 bt-biografie-name').find('h3').text

            person_name_company = person.strip().split(',')
            person_name = person_name_company[0]
            person_company = person_name_company[1].strip()
            social_networks = soup.find_all(class_='bt-link-extern')

            social_networks_urls = []
            for item in social_networks:
                social_networks_urls.append(item.get('href'))

            person_data = {
                'person_name': person_name,
                'company_name': person_company,
                'social_networks': social_networks_urls
            }

            data.append(person_data)

        with open(f'./data/bundes/list_result.json', 'a', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return data
