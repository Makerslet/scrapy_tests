import scrapy
from selenium import webdriver

class MainpageSpider(scrapy.Spider):
    name = "mainpage"
    start_urls = ['https://auto.ru/sankt-peterburg/cars/all/']

    def __init__(self):
        self.driver = webdriver.Firefox()

    def __del__(self):
        self.driver.quit()

    def click_expand_brands(self, response):
        self.driver.get(response.url)
        element = self.driver.find_element_by_css_selector('span.ListingPopularMMM-module__expandLink')
        element.click()
        return self.driver.page_source

    def parse(self, response):
        new_selector = scrapy.Selector(text=self.click_expand_brands(response))
        print("lkl", new_selector)
