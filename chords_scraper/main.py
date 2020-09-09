import sys

import requests
from bs4 import BeautifulSoup


def scrape_ukutabs(base_url, params):
    search_page = requests.get(base_url, params=params)
    soup = BeautifulSoup(search_page.content, "html.parser")

    chords_link = soup.select_one("ul.archivelist li a")["href"]

    return chords_link


# The search works very poorly on this website.
def scrape_ukuleletabs(base_url, subdirs, params):
    search_page = requests.get(base_url + "/".join(subdirs), params=params)
    soup = BeautifulSoup(search_page.content, "html.parser")

    chords_link = soup.select_one("ul.resp_list li a")["href"]

    return base_url + chords_link[1:]


def main():
    song = " ".join(sys.argv[1:])
    print(scrape_ukutabs("https://ukutabs.com/", {"s": song}))
    print(
        scrape_ukuleletabs(
            "https://www.ukulele-tabs.com/",
            ["search-uke-chords"],
            {"find": song},
        )
    )


if __name__ == "__main__":
    main()
