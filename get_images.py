from bs4 import BeautifulSoup
import requests
import lxml

def get_html(link:str)->str:
    return requests.get(link).text

def beautiful_soup_stuff()->None:
    image_and_alt :dict = {}
    soup = BeautifulSoup(get_html("https://everestuncensored.deerhold.com/d2hawkeye-hiking-budhanilkantha-shivapuri"),'html.parser')
    dom = lxml.etree.HTML(str(soup))
    print(str(soup))
    xpath_1 :str = "/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a/img"
    xpath_2 :str = "/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/a/img"
    images1 = dom.xpath(xpath_1)
    images2 = dom.xpath(xpath_2)
    extentions = []
    for image1 in images1:
        image_and_alt[image1.get('alt')] = image1.get('src')
        extentions.append(image1.get("src").split('.')[-1])
    for image2 in images2:
        image_and_alt[image2.get('alt')] = image2.get('src')
        extentions.append(image2.get("src").split('.')[-1])

    return image_and_alt
    

def write_to_file(name,content):
    with open(name+".jpg","wb") as binary_writer:
        binary_writer.write(content)
        

def download_image_and_text(image_and_text:dict):
    for alt,src in image_and_text.items():
        print("Getting {}".format(src))
        data = requests.get(src,stream=True)

        write_to_file(alt,data.content)


if __name__ == "__main__":
    image_and_text = beautiful_soup_stuff()

    download_image_and_text(image_and_text)
