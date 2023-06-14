from bs4 import BeautifulSoup
from .webrequest import WebRequest 

class DiningOptionsScraper:
    def __init__(self, url: str):
        self.url = url
        self.web_request = WebRequest(self.url)

    def parse_dining_options(self, response: str) -> str:
        soup = BeautifulSoup(response, 'html.parser')
        options = ''
        # parse for dining options within dining groups
        dining = soup.find('div', {'class': 'hours-of-operation'}).find_all('div', {'class': 'dining-group'})
        for group in dining:
            for restaurant in group.find_all('div', {'class': 'dining-block'}):

                title = restaurant.find('h3').find('a').text.strip()
                restaurant_text = title + '\n'

                has_hours = False
                for day in restaurant.find_all('div', {'class': 'reghours'}):
                    for time in day.find_all('div'):
                        days = time.find('p', {'class': 'dining-block-days'})
                        hours = time.find('p', {'class': 'dining-block-hours'})
                        if days and hours and days['data-arrayregdays'] and hours.text.strip() != "Closed":
                            restaurant_text += days['data-arrayregdays'] + " : " + hours.text.strip() + '\n'
                            has_hours = True

                if has_hours:
                    options += restaurant_text

        return options


    def get_dining_options(self) -> str:
        html_content = self.web_request.scrape()
        if html_content == 404:
            print(f'404 ERROR - Web Request Failed')
            return html_content
        elif html_content:
            return self.parse_dining_options(html_content)
        else:
            return None

if __name__ == "__main__":
    url = 'https://dineslu.sodexomyway.com/dining-near-me/hours'
    scraper = DiningOptionsScraper(url)
    dining_options = scraper.get_dining_options()
    if dining_options:
        print(dining_options)
