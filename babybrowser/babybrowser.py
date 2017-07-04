#!/usr/bin/env python3

from .gui import *
from .html_tokenizer import *
from .css_tokenizer import *
from .networking import *
import pickle
import shutil
import os

class BabyBrowser:

    BOOKMARK_FILE = os.path.join("babybrowser", "user", "bookmarks")
    if not os.path.isfile( BOOKMARK_FILE ):
        shutil.copyfile( os.path.join("babybrowser", "default_bookmarks"),
                         os.path.join("babybrowser", "user", "bookmarks") )
    DEFAULT_CSS = os.path.join("babybrowser", "browser.css")

    def __init__(self):
        self.html_tokenizer = Html_Tokenizer()
        self.css_tokenizer = CSS_Tokenizer()
        self.gui = None
        self.previous_pages = []
        self.forward_pages = []
        self.current_url = None
        self.bookmark_write = False

        with open(BabyBrowser.BOOKMARK_FILE, 'rb') as bookmarks_file:
            self.bookmarks = pickle.load(bookmarks_file)
        with open(BabyBrowser.DEFAULT_CSS, 'r') as default_css:
            self.default_css = "".join(list(default_css))

    def fetch_url(self, url, direction=None):
        response = network_get(url)
        if not direction and self.current_url and self.current_url!=url:
            self.previous_pages.append(self.current_url)
        self.current_url = url
        return self.tokenize_html(response)

    def tokenize_html(self, html):
        self.html_tokenizer.tokenize(html)
        dom = self.html_tokenizer.dom
        #Default Browser Styles
        self.css_tokenizer.tokenize(self.default_css, dom)
        #Style in Head
        style_elements = dom.find_children_by_tag("style")
        for element in style_elements:
            self.css_tokenizer.tokenize(element.content, dom)
        print(dom)
        return dom

    def show_gui(self):
        self.gui = Browser_GUI(self)

    def go_back(self):
        if not self.previous_pages:
            return None
        page_url = self.previous_pages.pop()
        self.forward_pages.append(self.current_url)
        print("\n------------------\nPrev:{}\nForward:{}\nGOTO:{}\n-----------------\n".format(self.previous_pages, self.forward_pages, page_url))
        return page_url

    def go_forward(self):
        if not self.forward_pages:
            return None
        page_url = self.forward_pages.pop()
        self.previous_pages.append(self.current_url)
        return page_url

    def has_bookmark(self, url):
        for bookmark in self.bookmarks:
            if bookmark.url == url:
                return True
        return False

    def index_of_bookmark(self, url):
        for index in range(len(self.bookmarks)):
            if self.bookmarks[index].url == url:
                return index
        return None

    def add_bookmark(self, url, title=None, icon=None):
        self.bookmark_write = True
        if not self.has_bookmark(url):
            self.bookmarks.append(MenuWebPage(url, title))

    def remove_bookmark(self, url):
        self.bookmark_write = True
        if self.has_bookmark(url):
            index = self.index_of_bookmark(url)
            self.bookmarks.pop(index)

    def on_close(self):
        if self.bookmark_write:
            with open(BabyBrowser.BOOKMARK_FILE, 'wb') as bookmarks_file:
                pickle.dump(self.bookmarks, bookmarks_file, protocol=pickle.HIGHEST_PROTOCOL)

class MenuWebPage:
    def __init__(self, url, title=None, icon=None):
        self.url = url
        self.icon = icon
        self.title = title
    def __str__(self):
        return "Title:{} Url:{}".format(self.title, self.url)
    def __repr__(self):
        return str(self)



