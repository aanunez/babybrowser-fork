#!/usr/bin/env python3

import re
from .html_objects import *

t_OPENTAG = re.compile("\s*<(?P<tag>\w+)\s*(?P<attrs>[^>]+)?>")
t_ATTRIBUTES = re.compile("(?P<attr_name>\w+)=\"(?P<attr_value>[^\"]+)\s*")
t_CLOSETAG = re.compile("</(\w+)>")
t_DATA = re.compile("[^<>]+")
t_WHITESPACE = re.compile("\s+")

#States
BEFORE_HTML = "before html"
BEFORE_HEAD = "before head"
IN_HEAD = "in head"
AFTER_HEAD = "after head"
IN_BODY = "in body"
AFTER_BODY = "after body"
AFTER_AFTER_BODY = "after after body"

#Special HTML Tags
BODY = "body"
HTML = "html"
HEAD = "head"
STYLE = "style"

class Html_Tokenizer:

    def handle_opentag(self, tag_str, attrs):
        #print("Found start tag:", tag_str, attrs)
        tag = Tag(tag_str)
        tag.parse_state = self.current_state
        if attrs:
            self.p_opentag_attrs(tag, attrs)
        self.dom.add_child(tag)
        if tag.is_self_closing:
            self.handle_closetag(tag)

    def handle_closetag(self, tag):
        #print("Found end tag:", tag)
        self.dom.close_child()

    def handle_data(self, display_data, original_data):
        #print("Found data:", display_data)
        if self.current_state==IN_BODY:
            data = Text(display_data, original_data)
            data.parse_state = self.current_state
            self.dom.add_text(data)
        else:
            self.dom.add_content(display_data)

    def p_opentag(self, match):
        tag = match.group("tag")
        attrs = match.group("attrs")
        self.set_opentag_state(tag)
        return tag, attrs, len(match.group(0))

    def p_opentag_attrs(self, tag, attrs):
        for match in re.finditer(t_ATTRIBUTES, attrs):
            attr_name = match.group("attr_name")
            attr_value = match.group("attr_value")
            tag.add_attr(attr_name, attr_value)

    def set_opentag_state(self, tag):
        if tag.lower()==HTML:
            self.current_state = BEFORE_HEAD
        elif tag.lower()==HEAD:
            self.current_state = IN_HEAD
        elif tag.lower()==BODY:
            self.current_state = IN_BODY

    def p_closetag(self, match):
        tag = match.group(1)
        if tag.lower()==HTML:
            self.current_state = AFTER_AFTER_BODY
        elif tag.lower()==HEAD:
            self.current_state = AFTER_HEAD
        elif tag.lower()==BODY:
            self.current_state = AFTER_BODY
        return tag, None, len(tag)

    def tokenize(self, html):
        index = 0
        self.dom = DOM()
        self.current_state = BEFORE_HTML
        while index<len(html):
            index = self.parse(html, index)

    def parse(self, html, index):
        add_to_index = 0
        opentag =  t_OPENTAG.match(html[index:])
        closetag =  t_CLOSETAG.match(html[index:])
        whitespace = t_WHITESPACE.match(html[index:])
        data = t_DATA.match(html[index:])
        if opentag:
            tag, attrs, tag_len = self.p_opentag(opentag)
            self.handle_opentag(tag, attrs)
            add_to_index = tag_len
        elif closetag:
            tag, attrs, tag_len = self.p_closetag(closetag)
            self.handle_closetag(tag)
            add_to_index = tag_len+2
        elif whitespace:
            add_to_index = len(whitespace.group(0))
        elif data:
            data_result = self.p_data(data.group(0))
            self.handle_data(data_result, data.group(0))
            add_to_index = len(data.group(0))
        else:
            add_to_index = 1
        return add_to_index+index

    def p_data(self, data):
        return self.remove_excess_whitespace(data)

    def remove_excess_whitespace(self, data):
        return " ".join( filter(lambda x: x, re.split("\s", data)) )


