from scraper import EverestUncensored
import os

if __name__ == "__main__":

    uncensored = EverestUncensored(os.path.join(os.getcwd(),"..","./driver/geckodriver-0.32.2/target/release/geckodriver"),"link_file.txt")
    try:
        uncensored.read_link()
        uncensored.get_all_links()
        uncensored.create_driver()
        uncensored.go_to_individual_page()
    except KeyboardInterrupt:
        print("Exiting Gratefully")
        uncensored.exit()
        exit(1)

