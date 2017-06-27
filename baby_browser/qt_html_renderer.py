from PyQt5.QtWidgets import * 
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from baby_browser.css_objects import *

class QT_HTML_Renderer:
    HEADERS = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
    def __init__(self):
        pass
    def set_page_title(self, title, page):
        page.setWindowTitle(title)
        page.title = title
    def render_in_body_content(self, element, layout):
        widget = self.render_tag(element)
        layout.addWidget(widget)
    def render_tag(self, element):
        tag = element.tag.lower()
        if tag in QT_HTML_Renderer.HEADERS:
            return self.render_text(tag, element)
        else:
            return self.render_text(tag, element)
    def render_text(self, tag, element):
        text = QLabel(element.content)
        text.setWordWrap(True)
        text.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum);
        css = element.css
        if css:
            prop_dict = css.get_set_properties()
            font = QFont()
            for key in prop_dict:
                if key == Font.p_FONT_WEIGHT:
                    weight = prop_dict[key]
                    self.set_font_weight(font, weight)
                if key == Font.p_FONT_SIZE:
                    size = prop_dict[key]
                    print(size)
                    self.set_font_point_size(font, size)
            text.setFont(font)
        return text

    def set_font_weight(self, font, weight):
        if weight==Font.FONT_WEIGHT_BOLD:
            font.setBold(True)
        elif weight==Font.FONT_WEIGHT_NORMAL:
            fold.setBold(False)
    def set_font_point_size(self, font, size):
        font.setPointSize(size.value)

        

            


       # font = QFont("Raleway")