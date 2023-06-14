from bs4 import BeautifulSoup
from .webrequest import WebRequest

class RecCenterHoursScraper:
    def __init__(self, url: str):
        self.url = url
        self.web_request = WebRequest(self.url)

    def parse_general_hours(self, response: str) -> str:
        soup = BeautifulSoup(response, 'html.parser')
        hours = ''
        # parse for general facility hours in tbody divs
        tbody = soup.find('tbody')
        for tr in tbody.find_all('tr'):
            td = tr.find('td')
            text = td.text.strip()
            
            hours = hours + td.text.strip() + '\n'

        hours = "--*General Facility Hours*--" + '\n' + '\n' + hours
        return hours

    def get_general_hours(self) -> str:
        html_content = self.web_request.scrape()
        if html_content == 404:
            print(f'404 ERROR - Web Request Failed')
            return html_content
        elif html_content:
            return self.parse_general_hours(html_content)
        else:
            return None
        

if __name__ == "__main__":
    url = 'https://www.slu.edu/life-at-slu/campus-recreation-wellness/facilities-and-hours.php'
    scraper = RecCenterHoursScraper(url)
    general_hours = scraper.get_general_hours()
    if general_hours:
        print(general_hours)
