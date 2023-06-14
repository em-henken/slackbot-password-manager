from bs4 import BeautifulSoup
from .webrequest import WebRequest  

class NewsScraper:
    def __init__(self, url: str):
        self.url = url
        self.web_request = WebRequest(self.url)

    def parse_news(self, response: str) -> str:
        soup = BeautifulSoup(response, 'html.parser')
        news = ''
        # parse for news articles, specifically headlines and descriptions
        for article in soup.find_all('div', {'class': 'card__detail'}):
            title = article.find('span', {'class': 'card__title'}).text.strip()
            description = article.find('p').text.strip()
            news += f"--*{title}*--\n\n\t\t\t\t{description}\n\n"
        return news


    def get_news(self) -> str:
        html_content = self.web_request.scrape()
        if html_content == 404:
            print(f'404 ERROR - Web Request Failed')
            return html_content
        elif html_content:
            return self.parse_news(html_content)
        else:
            return None

if __name__ == "__main__":
    url = 'https://www.slu.edu/news/index.php'
    scraper = NewsScraper(url)
    news = scraper.get_news()
    if news:
        print(news)
