import re
import traceback
from selenium.webdriver.common.by import By
from modules.nytimes.browser import NyTimesBrowser
from modules import ExcelGenerator
from datetime import datetime, date
from RPA import FileSystem
from RPA.HTTP import HTTP
from modules.nytimes import logger
from RPA.Archive import Archive
from dateutil import parser


# This class will Scrap data from the given URL.
class DataExtractor:
    article_with_in_range = []
    archive = Archive()

    def __init__(self):
        self.base_url = "https://www.nytimes.com"
        self.browser = NyTimesBrowser()
        self.excel_generator = ExcelGenerator()
        self.fs = FileSystem
        self.file_sys = FileSystem.FileSystem()
        self.http_req = HTTP()

    """ This method will call other methods in the process. it will accept 
    search phrase, news category and num months as params provided by user """
    def run(self, search_phrase, news_category, num_months):
        end_date = datetime.now()
        num_months = 1 if num_months == 0 else num_months
        start_date = end_date.replace(day=1).replace(month=date.today().month - (num_months - 1)).date()
        logger.info("Opening browser...")
        self.browser.open_browser(self.base_url)
        logger.info("Handling terms modal...")
        self.browser.close_terms_modal()
        logger.info(f"Entering {search_phrase=}...")
        self.browser.accept_cookies()
        self.browser.enter_search_phrase(search_phrase)
        logger.info(f"Selecting sorting to newest...")
        self.browser.change_sorting()
        logger.info(f"Applying date range {start_date=} and {end_date=}...")
        self.browser.set_date_range(start_date, end_date)
        logger.info(f"Selecting section category={news_category}...")
        self.browser.select_section(news_category)
        logger.info(f"Filter out articles in date range...")
        self.get_articles_within_date_range(start_date)
        logger.info(f"Scraping data...")
        self.get_article_data(self.article_with_in_range, search_phrase)
        logger.info(f"Data scrapped successfully...")

    """ This method extracts the articles from web page and filter out articles that are within the
    provided date range. If provided range is 1 then the scraped articles will be from current month,
    if 2 then current month and previous month, if 3 then current and previous 2 months.
    Filtered articles will append to article_with_in_range list. """
    def get_articles_within_date_range(self, start_date):
        try:
            articles = self.browser.find_web_elements("//li[@data-testid='search-bodega-result']")
            for article in articles:
                date_element = article.find_element(By.TAG_NAME, "span")
                date_str = date_element.get_attribute("innerHTML")
                article_date = parser.parse(date_str).date()
                if article_date >= start_date:
                    self.article_with_in_range.append(article)
                else:
                   return
            self.browser.click_show_more_button()
            self.article_with_in_range.clear()
            self.get_articles_within_date_range(start_date)
        except Exception as e:
            error = traceback.format_exc()
            logger.info(f"No article found {error=}")

    """ This method extract required data such as title, description, date, picture etc
     from each article present in article_with_in_range list. """
    def get_article_data(self, articles, search_phrase):
        news_data = []
        for article in articles:
            title_element = article.find_element(By.TAG_NAME, "h4")
            title = title_element.get_attribute("innerText")
            date_element = article.find_element(By.TAG_NAME, "span")
            date_str = date_element.get_attribute("innerHTML")
            date = parser.parse(date_str).date()
            description_element = article.find_element(By.CLASS_NAME, "css-16nhkrn")
            description = description_element.get_attribute('innerText')
            picture_element = article.find_element(By.TAG_NAME, "img")
            picture_url = picture_element.get_attribute('src')
            picture_filename = picture_url.split("/")[-1].split("?")[0]
            search_phrase_count = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(search_phrase), title, re.IGNORECASE))
            search_phrase_count += sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(search_phrase), description, re.IGNORECASE))
            money_in_title = bool(re.search(r'\$\d+(\.\d{2})?', title))
            money_in_description = bool(re.search(r'\$\d+(\.\d{2})?', description))
            news_data.append({
                "Title": title,
                "Date": date,
                "Description": description,
                "Picture filename": picture_filename,
                "Search Phrase Count": search_phrase_count,
                "Money in Title or Money in Description": True if money_in_title and money_in_description else False,
            })
            try:
                self.http_req.download(picture_url, f"output/pictures/{picture_filename}")
            except Exception as e:
                error = traceback.format_exc()
                logger.info(f"Image not found {error=}")
        self.archive.archive_folder_with_tar('./output/pictures', 'output/pictures.tar', recursive=True)
        self.excel_generator.write_to_excel(news_data)
