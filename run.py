from sys import argv
from everest_uncensored import Scraper

if len(argv) != 2:
    raise Exception("Need a link! \nUsage : python run.py {link}\nExample:\npython run.py https://everestuncensored.deerhold.com/jamacho-hike-2005")

if(argv[1][:5] != "https"):
    raise Exception("Passed Argument must be a link")

print(argv)
scraper = Scraper(argv[1])
scraper.scrape()