import requests

""" This class means to pull HTML from websites to provide up-to-date information """

class WebRequest:

    def __init__(self, url) -> None:
        self.url = url

    def fetch_html(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.content
        else:
            return None
    
    def scrape(self):
        html_content = self.fetch_html()
        if html_content:
            return html_content
        else:
            print(f'Request failed')
            return 404