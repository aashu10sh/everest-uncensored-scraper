import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By


class EverestUncensored():

    """ Version 2 of Everest Uncensored Scraper"""

    def __init__(self, driver_path, link_file):
        self.driver_path = driver_path
        self.link_file = link_file
        self.months = ["January", "February", "March", "April", "May", "June",
                       "July", "August", "September", "October", "November", "December"]
        self.years = [x for x in range(2007, 2023)]
        self.driver = None
        self.endpoints = None
        self.link = None

    def create_driver(self) -> None:
        """Method for getting the driver"""
        self.driver: webdriver.firefox.webdriver.WebDriver = webdriver.Firefox(
            executable_path=self.driver_path)

    def read_link(self):
        """returns link present in the file passed"""
        with open(self.link_file, "r") as reader:
            self.link = reader.readline()
        return self.link

    def exit(self):
        """Kills the driver process"""
        self.driver.quit()

    def get_all_links(self) -> list:
        """Get all trip endpoints of all years and hike"""
        all_endpoints: list = []
        for year in self.years:
            for month in self.months:
                # print(year,'?',month)
                all_endpoints.append(f"{self.link}{year}/{month}")
        self.endpoints = all_endpoints
        return all_endpoints

    @staticmethod
    def get_slug_of_url(link: str) -> str:
        """Returns Slug from a link"""
        return link.split('/')[-1]
    
    @staticmethod
    def write_to_json(file_name:str, file_content:dict)->bool:
        """Writes given dict to json in given file name"""
        try:
            with open(file_name,"w") as writer:
                json.dump(file_content,writer)
            return True
        except Exception as error_information:
            print(error_information)
            exit(0)
            return False
        

    def get_hike_links(self, driver) -> dict:
        """Returns Hiking Links from current page."""
        all_hikes = {}
        hike_xpath: str = "/html/body/div/div[2]/div/div/a[1]"
        elements = driver.find_elements(By.XPATH, hike_xpath)
        for element in elements:
            if element == None:
                continue
            all_hikes[EverestUncensored.get_slug_of_url(element.get_attribute("href"))] = {"title":element.text, "link":element.get_attribute("href")}
        return all_hikes

    def get_hike_information(self) -> None:
        """Goes to each individual page"""
        all_links = []
        try:
            for endpoint in self.endpoints:
                self.driver.get(endpoint)
                data  = self.get_hike_links(self.driver)
                if not data:
                    continue
                all_links.append(data)
                
        except AttributeError as error_str:
            print(error_str)
            print("Please use the <class_obj>.create_driver() method first")
            exit(0)
        EverestUncensored.write_to_json("all_links.json",all_links)

        self.exit()
