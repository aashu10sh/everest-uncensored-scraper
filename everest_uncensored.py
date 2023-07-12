import os
from bs4 import BeautifulSoup
import requests



class Scraper():
    """ Web Scraper for the Everest Uncensored Website"""

    def __init__(self, url: str):
        self.url: str = url
        self.allowed_extensions = ["jpg", "png"]
        self.download_path = os.path.join(os.getcwd(),self.url.split("/")[-1])

    def get_html(self) -> str:
        """Returns HTML Content of the required page."""
        return requests.get(self.url, timeout=30).text

    def soup(self, html_content) -> BeautifulSoup:
        """Returns the BeautifulSoup Object based on raw html provided of the website"""
        return BeautifulSoup(html_content, "lxml")

    def get_links(self, soup: BeautifulSoup) -> list:
        """Returns all images """
        links = []
        for link in soup.findAll("img"):
            if "amazonaws" in link.get("src"):
                links.append(link.get("src"))

        return links

    def create_new_directory(self) -> None:

        """Creates a new directory to store the images"""
        try:
            os.mkdir(self.download_path)
        except FileExistsError:
            print("Folder Already exists, formatting and re-populating!")
            os.rmdir(self.download_path)
            os.mkdir(self.download_path)

    def download_images(self,links:list)->None:
        """Downloads the image and sends the obtained binary data to write to file function """
        for link in links:
            data = requests.get(link,stream=True,timeout=30)
            print(f"[x] Got Image from Link {link}")
            self.write_to_file(data,link.split("/")[-1])

    def write_to_file(self,data:bytes,name:str)->None:
        """Writes Image Binary Data to File"""
        with open(os.path.join(self.download_path,name),"wb") as writer:
            writer.write(data.content)

    def scrape(self):
        """Main Method, Run to Scrape"""
        html_content = self.get_html()
        links = self.get_links(self.soup(html_content))
        self.create_new_directory()
        self.download_images(links)

