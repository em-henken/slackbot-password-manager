from bs4 import BeautifulSoup
from .webrequest import WebRequest  

class FinalExamScheduleScraper:
    def __init__(self, url: str):
        self.url = url
        self.web_request = WebRequest(self.url)

    def parse_final_schedule(self, response: str) -> str:
        soup = BeautifulSoup(response, 'html.parser')
        schedule = ''

        days = soup.find('article')
        for day in days.find_all("div", {"class": "table"}):
            table = day.find('table')
            # Retrieve exam date within thead
            exam_date = table.find('thead').find('tr').find('th').text.strip()
            schedule = schedule + '\n\n' + f"-- *{exam_date}* --"
            # Retrieve exam times + corresponding course times within tbody
            for time in table.find('tbody').find_all('tr'):
                exam_time = time.find_all('td')[0].text.strip()
                course_time = time.find_all('td')[1].text.strip()

                if "Final Exam Time" in exam_time:
                    continue

                schedule = schedule + '\n' + f"{exam_time:<20} : {course_time}"

        return schedule

    def get_final_schedule(self) -> str:
        html_content = self.web_request.scrape()
        if html_content == 404:
            print(f'404 ERROR - Web Request Failed')
            return html_content
        elif html_content:
            return self.parse_final_schedule(html_content)
        else:
            return None

if __name__ == "__main__":
    url = 'https://www.slu.edu/registrar/calendars/final-exam-schedule.php'
    scraper = FinalExamScheduleScraper(url)
    final_schedule = scraper.get_final_schedule()
    if final_schedule:
        print(final_schedule)
