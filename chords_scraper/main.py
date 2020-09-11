import pathlib
import sys

import requests
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


def scrape_ukutabs(base_url, params):
    search_page = requests.get(base_url, params=params)
    soup = BeautifulSoup(search_page.content, "html.parser")

    try:
        chords_link = soup.select_one("ul.archivelist li a")["href"]
    except TypeError:
        sys.stderr.write("Didn't get any results from `ukutabs.com`.\n")
        return

    return chords_link


# The search works very poorly on this website.
def scrape_ukuleletabs(base_url, subdirs, params):
    search_page = requests.get(base_url + subdirs, params=params)
    soup = BeautifulSoup(search_page.content, "html.parser")

    try:
        chords_link = soup.select_one("ul.resp_list li a")["href"]
    except TypeError:
        sys.stderr.write("Didn't get any results from `ukulele-tabs.com`.\n")
        return

    return base_url + chords_link[1:]


def scrape_echords(base_url, subdirs):
    search_page = requests.get(base_url + subdirs)
    soup = BeautifulSoup(search_page.content, "html.parser")

    try:
        chords_link = soup.select_one("ul#results p.h1 a")["href"]
    except TypeError:
        sys.stderr.write("Didn't get any results from `e-chords.com`.\n")
        return

    return chords_link


def scrape_ultimateguitar(base_url, subdirs, params):
    search_page = f"{base_url}{subdirs}?search_type=title&value={params}"

    options = Options()
    options.headless = True

    executable_path = pathlib.Path("chords_scraper", "drivers", "geckodriver.exe")

    with Firefox(options=options, executable_path=executable_path) as driver:
        driver.get(search_page)
        soup = BeautifulSoup(driver.page_source, "html.parser")

    chords_links = soup.select("div._3gmWN a._2KJtL._1mes3.kWOod")
    for chords_link in chords_links:
        split = chords_link["href"].split("/")
        if split[3] != "pro" and split[4] != "misc-your-songs":
            return chords_link["href"]

    sys.stderr.write("Didn't get any results from `ultimate-guitar.com`.\n")
    return


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

        wait = WebDriverWait(driver, 5)
        try:
            wait.until(
                lambda driver: driver.find_element_by_class_name("v0") != default_result
            )
        except TimeoutException:
            sys.stderr.write("Didn't get any results from `chords.pl`.\n")
            return

        result = driver.find_element_by_class_name("v0")
        chords_link = result.find_element_by_css_selector(
            "td:nth-of-type(3) a"
        ).get_attribute("href")

        return chords_link


def main():
    artist = sys.argv[1]
    title = sys.argv[2]

    links = [
        scrape_ukutabs("https://ukutabs.com/", {"s": f"{artist} {title}"}),
        scrape_ukuleletabs(
            "https://www.ukulele-tabs.com/",
            "search-uke-chords",
            {"find": title},
        ),
        scrape_echords("https://www.e-chords.com/", f"search-all/{artist} {title}"),
        scrape_ultimateguitar(
            "https://www.ultimate-guitar.com/", "search.php", f"{artist} {title}"
        ),
        scrape_chordspl("https://www.chords.pl/", artist, title),
    ]

    for link in links:
        if link:
            print(link)


if __name__ == "__main__":
    main()
