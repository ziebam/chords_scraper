# Chords Scraper

![demo](https://i.imgur.com/4KxQ7WQ.png)

The program finds ukulele notes in a few different websites and provides the user with links to them.

Supported websites:

- [ukutabs.com](https://ukutabs.com/)
- [ukulele-tabs.com](https://www.ukulele-tabs.com/) (very poor search function)
- [e-chords.com](https://www.e-chords.com/)
- [ultimate-guitar.com](https://www.ultimate-guitar.com/) (free version)
- [chords.pl](https://www.chords.pl/)

## Installation and usage

Head over to [releases](https://github.com/ziebam/chords_scraper/releases) and download the `chscrp.exe` file from the latest release. Put it wherever you want and run it. Please note that the scraping might take a while as some of the websites are generated dynamically and hence require using `Selenium` to mock the browser.

The program can be safely renamed.

The `geckodriver.log` file created by the program can be safely deleted.

As with most PyInstaller applications your operating system might complain about the file being potentially unsafe.

## License

[MIT](LICENSE)
