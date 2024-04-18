import traceback
from RPA.Browser.Selenium import Selenium
from modules.nytimes import logger


class NyTimesBrowser:

    def __init__(self):
        self.browser = Selenium()

    # This method opens provided URL in the available browser
    def open_browser(self, base_url):
        self.browser.open_available_browser(base_url)

    # This method finds the articles from web page
    def find_web_elements(self, path):
        self.browser.wait_until_element_is_visible(path)
        web_element = self.browser.find_elements(path)
        return web_element

    # This method closes term Modal that opens after page load
    def close_terms_modal(self):
        self.browser.wait_until_element_is_visible('//button[contains(text(), "Accept all")]')
        self.browser.click_button('//button[contains(text(), "Accept all")]')

    def accept_cookies(self):
        try:
            self.browser.wait_until_element_is_visible('//button[@data-testid="GDPR-accept"]')
            self.browser.click_button('//button[@data-testid="GDPR-accept"]')
        except Exception as e:
            error = traceback.format_exc()
            logger.info(f"No cookies modal appear")

    # This method enter the provided keyword into search input
    def enter_search_phrase(self, search_phrase):
        self.browser.click_button('//button[@aria-controls="search-input"]')
        self.browser.input_text('//input[@data-testid="search-input"]', search_phrase)
        self.browser.press_keys('//input[@data-testid="search-input"]', "ENTER")

    # This method selects the provided sections/category from section list
    def select_section(self, news_category):
        if news_category:
            self.browser.click_element('//button[@data-testid="search-multiselect-button"]/label[text()="Section"]')
            for category in news_category:
                try:
                    self.browser.click_element(f"//span[contains(text(), '{category}')]")
                except Exception as e:
                    error = traceback.format_exc()
                    logger.info(f"This category not exists {error=}")

            self.browser.click_element('//button[@data-testid="search-multiselect-button"]/label[text()="Section"]')
            self.browser.wait_until_element_does_not_contain("//p[@class='css-nayoou']", "Loading...")

    # This method change sorting to "newest"
    def change_sorting(self):
        self.browser.click_element('//select[@data-testid="SearchForm-sortBy"]/option[@value="newest"]')

    # This method set date range for filtration
    def set_date_range(self, start_date, end_date):
        self.browser.click_element('//button[@data-testid="search-date-dropdown-a"]')
        self.browser.click_element('//button[@value="Specific Dates"]')
        self.browser.input_text('//input[@id="startDate"]', start_date.strftime("%Y-%m-%d"))
        self.browser.input_text('//input[@id="endDate"]', end_date.strftime("%Y-%m-%d"))
        self.browser.press_keys('//input[@id="endDate"]', "ENTER")

    # This method is for clicking show more button if there exist more articles in given date range
    def click_show_more_button(self):
            try:
                self.browser.click_button('//button[@data-testid="search-show-more-button"]')
            except Exception as e:
                error = traceback.format_exc()
                logger.info(f"Image not found {error=}")
