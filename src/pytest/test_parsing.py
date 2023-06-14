import pytest
import sys
sys.path.append('../')
from zahmed2.src.parsing.dining import DiningOptionsScraper
from zahmed2.src.parsing.finals import FinalExamScheduleScraper
from zahmed2.src.parsing.news import NewsScraper
from zahmed2.src.parsing.rec import RecCenterHoursScraper
from zahmed2.src.parsing.webrequest import WebRequest

def test_diningResponse():
    dummyscraper = DiningOptionsScraper("https://www.google.com/404")
    assert 404 == dummyscraper.get_dining_options(), "test failed"

    scraper = DiningOptionsScraper('https://dineslu.sodexomyway.com/dining-near-me/hours')
    assert str == type(scraper.get_dining_options()), "test failed"

def test_finalsResponse():
    dummyscraper = FinalExamScheduleScraper('https://www.google.com/404')
    assert 404 == dummyscraper.get_final_schedule(), "test failed"

    scraper = FinalExamScheduleScraper('https://www.slu.edu/registrar/calendars/final-exam-schedule.php')
    assert str == type(scraper.get_final_schedule()), "test failed"

def test_newsResponse():
    dummyscraper = NewsScraper("https://www.google.com/404")
    assert 404 == dummyscraper.get_news(), "test failed"

    scraper = NewsScraper("https://www.slu.edu/news/index.php")
    assert str == type(scraper.get_news()), "test failed"

def test_recResponse():
    dummyscraper = RecCenterHoursScraper("https://www.google.com/404")
    assert 404 == dummyscraper.get_general_hours(), "test failed"

    scraper = RecCenterHoursScraper('https://www.slu.edu/life-at-slu/campus-recreation-wellness/facilities-and-hours.php')
    assert str == type(scraper.get_general_hours()), "test failed"

def test_request():
    dummyrequest = WebRequest("https://www.google.com/404")
    assert None == dummyrequest.fetch_html()
    assert 404 == dummyrequest.scrape()

    request = WebRequest("https://www.slu.edu/")
    assert None != request.fetch_html()
    assert 404 != request.scrape()