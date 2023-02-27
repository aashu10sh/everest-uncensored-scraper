from selenium import webdriver
import time


class EverestUncensored():

    """ Version 2 of Everest Uncensored Scraper"""
    def __init__(self,driver_path,link_file):
        self.driver_path = driver_path
        self.link_file = link_file
        self.months = ["January","February","March","April","May","June","July","August","September","October","November","December"]
        self.years = [x for x in range(2007,2023)]
        self.driver = None
        self.endpoints = None
        self.link = None


    def create_driver(self)->None:
        """Method for getting the driver"""
        self.driver :webdriver.firefox.webdriver.WebDriver = webdriver.Firefox(executable_path=self.driver_path)

 
    def read_link(self):
        """returns link present in the file passed"""
        with open(self.link_file,"r") as reader:
            self.link =  reader.readline()
        return self.link
    
    def exit(self):
        """Kills the driver process"""
        self.driver.quit()
        
    def get_all_links(self)->list:
        """Get all trip endpoints of all years and hike"""
        all_endpoints :list= [] 
        for year in self.years:
            for month in self.months:
                # print(year,'?',month)
                all_endpoints.append(f"{self.link}{year}/{month}")
        self.endpoints = all_endpoints
        return all_endpoints
    

    def go_to_individual_page(self)->None:
        """Goes to each individual page"""
        try:
            for endpoint in self.endpoints:
                # print(f"{self.link} to {endpoint}")
                # print(endpoint)
                self.driver.get(endpoint)
                time.sleep(2)
        except AttributeError as error_str:
            print(error_str)
            print("Please use the <class_obj>.create_driver() method first")
            exit(0)

        self.exit()
        


