import sys

import requests
from bs4 import BeautifulSoup


def scrape_ukutabs(base_url, params):
    search_page = requests.get(base_url, params=params)
    soup = BeautifulSoup(search_page.content, "html.parser")

    chords_link = soup.select_one("ul.archivelist li a")["href"]

    return chords_link


def main():
    song = " ".join(sys.argv[1:])
    print(scrape_ukutabs("https://ukutabs.com/", {"s": song}))


if __name__ == "__main__":
    main()
