import pathlib
import sys

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait


def scrape_ukutabs(base_url, params):
    search_page = requests.get(base_url, params=params)
    soup = BeautifulSoup(search_page.content, "html.parser")

    chords_link = soup.select_one("ul.archivelist li a")["href"]

    return chords_link


# The search works very poorly on this website.
def scrape_ukuleletabs(base_url, subdirs, params):
    search_page = requests.get(base_url + subdirs, params=params)
    soup = BeautifulSoup(search_page.content, "html.parser")

    chords_link = soup.select_one("ul.resp_list li a")["href"]

    return base_url + chords_link[1:]


def scrape_echords(base_url, subdirs):
    search_page = requests.get(base_url + subdirs)
    soup = BeautifulSoup(search_page.content, "html.parser")

    chords_link = soup.select_one("ul#results a")["href"]

    return chords_link


def scrape_ultimateguitar(base_url, subdirs, params):
    search_page = f"{base_url}{subdirs}?search_type=title&value={params}"

    options = Options()
    options.headless = True

    executable_path = pathlib.Path("chords_scraper", "drivers", "geckodriver.exe")

    with Firefox(options=options, executable_path=executable_path) as driver:
        driver.get(search_page)
        soup = BeautifulSoup(driver.page_source, "html.parser")

    chords_links = soup.select("a._2KJtL._1mes3.kWOod")
    for chord_link in chords_links:
        split = chord_link["href"].split("/")
        if split[3] != "pro":
            return chord_link["href"]


def scrape_chordspl(base_url, artist, title):

    options = Options()
    options.headless = True

    executable_path = pathlib.Path("chords_scraper", "drivers", "geckodriver.exe")

    with Firefox(options=options, executable_path=executable_path) as driver:
        driver.get(base_url)

        default_result = driver.find_element_by_class_name("v0")

        form = driver.find_element_by_id("fs_band_name")
        form.send_keys(artist)
        form = driver.find_element_by_id("fs_title")
        form.send_keys(title)
        form.submit()

        wait = WebDriverWait(driver, 10)
        wait.until(
            lambda driver: driver.find_element_by_class_name("v0") != default_result
        )

        result = driver.find_element_by_class_name("v0")
        chords_link = result.find_element_by_css_selector(
            "td:nth-of-type(3) a"
        ).get_attribute("href")

        return chords_link


def main():
    artist = sys.argv[1]
    title = sys.argv[2]
    print(scrape_ukutabs("https://ukutabs.com/", {"s": song}))
    print(
        scrape_ukuleletabs(
            "https://www.ukulele-tabs.com/",
            "search-uke-chords",
            {"find": song},
        )
    )
    print(scrape_echords("https://www.e-chords.com/", f"search-all/{song}"))
    print(scrape_ultimateguitar("https://www.ultimate-guitar.com/", "search.php", song))
    print(scrape_chordspl("https://www.chords.pl/", artist, title))


if __name__ == "__main__":
    main()
