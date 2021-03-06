#!/usr/bin/env python3

import sys
import functools
import os
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from .html_tokenizer import *
from .qt_html_renderer import *
#Address bar for inserting a URI
#Back and forward buttons
#Bookmarking options
#Refresh and stop buttons for refreshing or stopping the loading of current documents
#Home button that takes you to your home page
#Among those are the address bar, status bar and tool bar

class Browser_Widget(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #color background white

        self.title = None

        #Scoll Area Properites
        scrollArea = QScrollArea()
        scrollArea.setWidgetResizable(True)
        self.widget = QWidget()
        widget_layout = QVBoxLayout(self)
        widget_layout.setAlignment(Qt.AlignTop)
        self.widget.setLayout(widget_layout)
        scrollArea.setWidget(self.widget)

        #Scroll Area Layout
        scroll_layout = QVBoxLayout(self)
        scroll_layout.addWidget(scrollArea)
        self.setLayout(scroll_layout)
        scroll_layout.setSizeConstraint(QLayout.SetMinimumSize)
        scroll_layout.setAlignment(Qt.AlignTop)

    def center(self):
        geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        geometry.moveCenter(center_point)
        self.move(geometry.topLeft())

class Browser_Main_Widget(QMainWindow):

    def __init__(self, browser=None):
        super().__init__()
        self.browser = browser
        self.initUI()

    def initUI(self):
        icon_path =  os.path.join("babybrowser", "images", "crib_background.png")
        self.setWindowIcon(QIcon(icon_path))
        self.page_icon = QIcon(os.path.join("babybrowser", "images", "page.png"))

        #Tabs
        self.tabBar = QTabWidget()
        self.tabBar.tabCloseRequested.connect(self.removeTab)
        close_icon_path = "babybrowser/images/close.png"
        self.setStyleSheet("QTabBar::close-button { image: url("+close_icon_path+"); }")
        self.tabBar.setTabsClosable(True)
        self.tabBar.setMovable(True)
        self.setCentralWidget(self.tabBar)

        new_tab_button = QPushButton()
        tab_icon_path =  os.path.join("babybrowser", "images", "new folder black.png")
        new_tab_button.setToolTip('New Tab')
        new_tab_button.setIcon(QIcon(tab_icon_path))
        button_font = new_tab_button.font()
        button_font.setBold(True)
        new_tab_button.setIconSize(QSize(50, 50))
        self.tabBar.setCornerWidget(new_tab_button)
        new_tab_button.clicked.connect(self.addDefaultTab)

        #status bar
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        #toolbar
        toolbar = self.addToolBar("Tool Bar")
        toolbar.setMovable(False)
        #Url Bar
        self.urlBar = QLineEdit()
        self.urlBar.returnPressed.connect(self.fetch_url)
        submit_button = QPushButton()
        submit_button.setIcon(QIcon(os.path.join("babybrowser", "images", "search.png")))
        submit_button.clicked.connect(self.fetch_url)
        submit_button.setToolTip('Sumbit Url')
        #Back/Forward Buttons
        back_button = QPushButton()
        back_button.setIcon(QIcon(os.path.join("babybrowser", "images", "back.png")))
        back_button.setToolTip('Back')
        back_button.clicked.connect(self.go_back)
        forward_button = QPushButton()
        forward_button.setIcon(QIcon(os.path.join("babybrowser", "images", "forward.png")))
        forward_button.setToolTip('Forward')
        forward_button.clicked.connect(self.go_forward)
        #Favorites Button
        self.favorite_button = QPushButton()
        self.fav_border_icon = QIcon(os.path.join("babybrowser", "images", "fav-border.png"))
        self.fav_full_icon = QIcon(os.path.join("babybrowser", "images", "fav-full.png"))

        self.favorite_button.setIcon(self.fav_border_icon)
        self.favorite_button.setToolTip('Bookmark')
        self.favorite_button.clicked.connect(self.toggle_bookmark)

        toolbar.addWidget(back_button)
        toolbar.addWidget(forward_button)
        toolbar.addSeparator()
        toolbar.addWidget(self.favorite_button)
        toolbar.addWidget(self.urlBar)
        toolbar.addSeparator()
        toolbar.addWidget(submit_button)

        #Menu Bar
        mainMenu = self.menuBar()
        self.favMenu = mainMenu.addMenu('Bookmarks')
        self.favMenu.setStyleSheet("QMenu { menu-scrollable: 1; }")
        for bookmark in self.browser.bookmarks:
            action = self.create_bookmark(bookmark.url, bookmark.title)
            action.triggered.connect(functools.partial(self.fetch_url, bookmark.url))
            self.favMenu.addAction(action)

        self.addDefaultTab()

        self.setGeometry(100, 100, 1200, 1200)
        self.setWindowTitle('BabyBrowser')

    def removeTab(self, index, no_add=False):
        if self.tabBar.count()==1 and not no_add:
            self.addDefaultTab()
        widget = self.tabBar.widget(index)
        widget.deleteLater()
        self.tabBar.removeTab(index)

    def addDefaultTab(self):
        self.addTab("New Tab", Browser_Widget())

    def addTab(self, tabName, widget):
        self.tabBar.addTab(widget, tabName)
        self.tabBar.setCurrentWidget(widget)
        index = self.tabBar.currentIndex()
        self.tabBar.setTabIcon(index, self.page_icon)

    def fetch_url(self, url=None, direction=None):
        if not url:
            url = self.urlBar.text()
        else:
            print("URL:", url)
            self.urlBar.setText(url)
        if self.browser:
            if self.browser.has_bookmark(url):
                self.favorite_button.setIcon(self.fav_full_icon)
            else:
                self.favorite_button.setIcon(self.fav_border_icon)

            self.statusBar.showMessage("Fetching Url")
            if direction:
                dom = self.browser.fetch_url(url, True)
            else:
                dom = self.browser.fetch_url(url)
            index = self.tabBar.currentIndex()
            self.removeTab(index, True)

            widget = Browser_Widget()
            self.statusBar.showMessage("Rendering Webpage")
            Browser_GUI.render_dom(dom, widget)
            self.addTab(widget.title, widget)
            self.statusBar.showMessage("")

    def go_back(self):
        url = self.browser.go_back()
        if url:
            self.fetch_url(url, True)

    def go_forward(self):
        url = self.browser.go_forward()
        if url:
            self.fetch_url(url)

    def toggle_bookmark(self):
        if not self.browser.has_bookmark(self.browser.current_url):
            self.add_bookmark()
        else:
            self.remove_bookmark()

    def add_bookmark(self):
        url = self.browser.current_url
        tab_index = self.tabBar.currentIndex()
        title = self.tabBar.tabText(tab_index)
        self.browser.add_bookmark(url, title)
        self.favorite_button.setIcon(self.fav_full_icon)
        action = self.create_bookmark(url, title)
        action.triggered.connect(lambda: self.fetch_url(url))
        self.favMenu.addAction(action)

    def create_bookmark(self, url, title=None, icon=None):
        if title:
            action = QAction(title, self)
            action.setStatusTip(title+"\n"+url)
        else:
            action = QAction(url, self)
            action.setStatusTip(url)
        if icon:
            action.setIcon(icon)
        else:
            action.setIcon(self.page_icon)
        return action

    def remove_bookmark(self):
        url = self.browser.current_url
        tab_index = self.tabBar.currentIndex()
        title = self.tabBar.tabText(tab_index)
        self.browser.remove_bookmark(url)
        self.favorite_button.setIcon(self.fav_border_icon)
        for action in self.favMenu.actions():
            print("Action:", action.text())
            if action.text()==url or action.text()==title:
                self.favMenu.removeAction(action)
                break

    def closeEvent(self, event):
        self.browser.on_close()

class Browser_GUI:

    HTML_RENDER = QT_HTML_Renderer()

    def __init__(self, browser=None):
        self.app = QApplication(sys.argv)
        self.browser = browser
        # Load the default fonts
        font_path_regular =  os.path.join("babybrowser", "fonts", "raleway", "Raleway-Regular.ttf")
        font_path_bold =  os.path.join("babybrowser", "fonts", "raleway", "Raleway-Bold.ttf")
        font_path_italic =  os.path.join("babybrowser", "fonts", "raleway", "Raleway-Italic.ttf")
        font_db = QFontDatabase()
        font_db.addApplicationFont(font_path_regular)
        font_db.addApplicationFont(font_path_bold)
        font_db.addApplicationFont(font_path_italic)
        ttf_font = QFont("Raleway")
        #ttf_font.setItalic(True)
        #ttf_font.setBold(True)
        self.app.setFont(ttf_font)

        #self.widget = Browser_Widget()
        #self.widget.center()
        self.inside_body = False
        self.widget = Browser_Main_Widget(browser)
        self.widget.show()
        sys.exit(self.app.exec_())

    def render_dom(dom, htmlWidget):
        Browser_GUI.HTML_RENDER.render_dom(dom.root, htmlWidget, htmlWidget.widget.layout())

