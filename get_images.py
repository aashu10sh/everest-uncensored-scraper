from bs4 import BeautifulSoup
import requests
import lxml
import sys
import os

def get_args():
    """ Returns Link and Directory"""
    if len(sys.argv) == 1 :
        print("pls provide link")
        exit(0)
    link :str = sys.argv[1]
    directory :str = sys.argv[1].split('/')[-1]
    return link,directory
        

def get_html(link:str)->str:
    """Return HTML data"""
    return requests.get(link).text

def get_dom(html)->None:
    """ Return DOM Object """
    image_and_alt :dict = {}
    soup = BeautifulSoup(get_html(link),'html.parser')
    dom = lxml.etree.HTML(str(soup))
    return dom
    

def write_to_file(name,content,directory):
    """Writes to image"""
    with open(directory+"/"+name+".jpg","wb") as binary_writer:
        binary_writer.write(content)
        

def check_combination_1(dom):
    """Check combination 1 """
    image_and_alt = {}
    xpath_1 :str = "/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a/img"
    xpath_2 :str = "/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/a/img"
    images1 = dom.xpath(xpath_1)
    images2 = dom.xpath(xpath_2)
    print("images:",images1,images2)
    for image1 in images1:
        image_and_alt[image1.get('alt')] = image1.get('src')
    for image2 in images2:
        image_and_alt[image2.get('alt')] = image2.get('src')

    return image_and_alt

def check_combination_2(dom):
    """Check Combination 2"""
    image_and_alt = {}
    xpath_1 :str = "/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a/img"
    xpath_2 :str = "/html/body/div/div[2]/div[2]/div/div[2]/table/tbody/tr/td[1]/table/tbody/tr[1]/td/a/img"
    images1 = dom.xpath(xpath_1)
    images2 = dom.xpath(xpath_2)
    for index,image1 in enumerate(images1):
        image_and_alt[f"image1 {image1.get('src').split('/')[-1]}"] = image1.get('src')
    for index,image2 in enumerate(images2):
        image_and_alt[f"image2 {image2.get('src').split('/')[-1]}"] = image2.get('src')

    return image_and_alt


def download_image_and_text(image_and_text:dict,directory):
    for alt,src in image_and_text.items():
        print("Getting {}".format(src))
        data = requests.get(src,stream=True)

        write_to_file(alt,data.content,directory)


if __name__ == "__main__":
    combination = {}
    link,directory = get_args()
    print(link,directory)
    os.mkdir(directory)
    print(link)
    html = get_html(link)
    print(html)
    dom = get_dom(html)
    print(dom)
    combination1 = check_combination_1(dom)
    if len(combination1.keys()) < 10:
        print("Failed with combination 1, moving to combination 2")
    else:
        combination = combination1
    combination2 = check_combination_2(dom)
    if len(combination2.keys()) < 10:
        print("Failed with combination 2, moving to combination 3")
    else:
        combination = combination2
    print(combination2)

    download_image_and_text(combination,directory)
