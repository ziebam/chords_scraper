import pathlib
import tkinter as tk
import webbrowser

from .scrapers import (
    scrape_ukutabs,
    scrape_ukuleletabs,
    scrape_echords,
    scrape_ultimateguitar,
    scrape_chordspl,
)


def callback(url):
    webbrowser.open_new(url)


class GUI(tk.Tk):
    width = 600
    height = 450

    def __init__(self):
        super().__init__()

        self.init_main_window()
        self.init_results_frame()
        self.init_input_frame()

    def init_main_window(self):
        self.iconbitmap(pathlib.Path("chords_scraper", "assets", "ukulele.ico"))
        self.title("Chords Scraper")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)
        self.configure(bg="#121212")

    def init_input_frame(self):
        self.input_frame = tk.Frame(master=self, padx=50, pady=50, bg="#121212")

        self.artist_label = tk.Label(
            master=self.input_frame,
            text="Artist",
            fg="#ffffff",
            bg="#121212",
            font=("Roboto", 16),
        )
        self.title_label = tk.Label(
            master=self.input_frame,
            text="Title",
            fg="#ffffff",
            bg="#121212",
            font=("Roboto", 16),
        )
        self.artist_entry = tk.Entry(master=self.input_frame, width=20)
        self.title_entry = tk.Entry(master=self.input_frame, width=20)

        self.search_button = tk.Button(
            master=self.input_frame,
            text="Search",
            width=10,
            command=lambda: self.display_links(
                self.artist_entry.get(), self.title_entry.get()
            ),
        )

        self.input_frame.columnconfigure(0, weight=1, minsize=self.width / 4)
        self.input_frame.columnconfigure(1, weight=1, minsize=self.width / 4)

        self.input_frame.place(relx=0.5, rely=0.2, anchor="center")

        self.artist_label.grid(row=0, column=0, sticky="nsew")
        self.title_label.grid(row=0, column=1, sticky="nsew")
        self.artist_entry.grid(row=1, column=0)
        self.title_entry.grid(row=1, column=1)

        self.search_button.grid(
            row=2,
            column=0,
            columnspan=2,
            pady=20,
        )

    def init_results_frame(self):
        self.results_frame = tk.Frame(master=self, padx=50, pady=50, bg="#121212")

        self.results_frame.columnconfigure(0, weight=1, minsize=self.width / 4)
        self.results_frame.columnconfigure(1, weight=1, minsize=self.width / 4)

        self.results_frame.place(relx=0.5, rely=0.6, anchor="center")

        self.results_label = tk.Label(
            master=self.results_frame,
            text="Results: ",
            fg="#ffffff",
            bg="#121212",
            font=("Roboto", 20),
        )
        self.ukutabs_label = tk.Label(
            master=self.results_frame,
            text="ukutabs.com:",
            fg="#ffffff",
            bg="#121212",
            font=("Roboto", 10),
        )
        self.ukutabs_result = tk.Label(
            master=self.results_frame,
            text="",
            fg="blue",
            bg="#121212",
            font=("Roboto", 10),
            cursor="hand2",
        )
        self.ukuleletabs_label = tk.Label(
            master=self.results_frame,
            text="ukulele-tabs.com:",
            fg="#ffffff",
            bg="#121212",
            font=("Roboto", 10),
        )
        self.ukuleletabs_result = tk.Label(
            master=self.results_frame,
            text="",
            fg="blue",
            bg="#121212",
            font=("Roboto", 10),
            cursor="hand2",
        )
        self.echords_label = tk.Label(
            master=self.results_frame,
            text="e-chords.com:",
            fg="#ffffff",
            bg="#121212",
            font=("Roboto", 10),
        )
        self.echords_result = tk.Label(
            master=self.results_frame,
            text="",
            fg="blue",
            bg="#121212",
            font=("Roboto", 10),
            cursor="hand2",
        )
        self.ultimateguitar_label = tk.Label(
            master=self.results_frame,
            text="ultimate-guitar.com:",
            fg="#ffffff",
            bg="#121212",
            font=("Roboto", 10),
        )
        self.ultimateguitar_result = tk.Label(
            master=self.results_frame,
            text="",
            fg="blue",
            bg="#121212",
            font=("Roboto", 10),
            cursor="hand2",
        )
        self.chordspl_label = tk.Label(
            master=self.results_frame,
            text="chords.pl:",
            fg="#ffffff",
            bg="#121212",
            font=("Roboto", 10),
        )
        self.chordspl_result = tk.Label(
            master=self.results_frame,
            text="",
            fg="blue",
            bg="#121212",
            font=("Roboto", 10),
            cursor="hand2",
        )

        self.results_label.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.ukutabs_label.grid(row=1, column=0, sticky="nsew")
        self.ukutabs_result.grid(row=1, column=1, sticky="nsew")
        self.ukuleletabs_label.grid(row=2, column=0, sticky="nsew")
        self.ukuleletabs_result.grid(row=2, column=1, sticky="nsew")
        self.echords_label.grid(row=3, column=0, sticky="nsew")
        self.echords_result.grid(row=3, column=1, sticky="nsew")
        self.ultimateguitar_label.grid(row=4, column=0, sticky="nsew")
        self.ultimateguitar_result.grid(row=4, column=1, sticky="nsew")
        self.chordspl_label.grid(row=5, column=0, sticky="nsew")
        self.chordspl_result.grid(row=5, column=1, sticky="nsew")

    def display_links(self, artist, title):
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

        result_labels = self.results_frame.winfo_children()[2::2]
        for link, result_label in zip(links, result_labels):
            if link:
                # For some reason it doesn't work with just a `link` argument.
                result_label.bind("<Button-1>", lambda _, link=link: callback(link))
                result_label["text"] = "click!"
            else:
                result_label["fg"] = "#ffffff"
                result_label["text"] = "no results from that website"
