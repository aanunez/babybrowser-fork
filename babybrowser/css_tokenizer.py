#!/usr/bin/env python3

import os
import re
from .css_objects import *

t_RULE = re.compile("\s*(?P<selector>[#\.\w\-\s,_]+)\s*\{\s*(?P<declarations>[^}]+)\}") #Groups the identifier and the css rules
t_DECLARATIONS = re.compile("(?P<property>[\w-]+):\s*(?P<value>[\w-]+);")
t_NUM_UNIT = re.compile("(?P<value>\d+)(?P<unit>pt|px)")
t_SELECTOR_GROUPS = re.compile("\s*(?P<selector>[#\.\w\-\s_]+)\s*")
t_SELECTOR = re.compile("\s*(?P<symbol>\.|#)?(?P<name>[\w-]+)\s*")

CLASS_SELECTOR = "."
ID_SELECTOR = "#"
TAG_SELECTOR = None

class CSS_Tokenizer:

    def __init__(self):
        pass

    def tokenize(self, css_str, dom):
        for css in re.finditer(t_RULE, css_str):
            self.parse(css, dom)

    def parse(self, css, dom):
        #print(css)
        if css:
            selectors = css.group('selector')
            declarations = css.group('declarations')
            for match in re.finditer(t_SELECTOR_GROUPS, selectors):
                elements = self.get_dom_elements(match.group("selector"), dom)
                #print(elements)
                for element in elements:
                    self.add_render_element(element, declarations)

    def add_render_element(self, dom_element, declarations):
        if dom_element:
            if dom_element.css:
                render_object = dom_element.css
            else:
                render_object = RenderObject(BoxStyle.BLOCK)
            #print(dom_element.tag)
            for match in re.finditer(t_DECLARATIONS, declarations):
                css_property =  match.group("property")
                css_value =  match.group("value")
                self.create_style(render_object, css_property, css_value)
            dom_element.css = render_object

    def get_dom_elements(self, selector, dom):
        root = dom.root
        elements = []
        for match in re.finditer(t_SELECTOR, selector):
            symbol = match.group("symbol")
            name = match.group("name")
            if symbol==TAG_SELECTOR:
                elements = dom.find_children_by_tag(name, root)
            elif symbol==CLASS_SELECTOR:
                elements = dom.find_children_by_class(name, root)
            elif symbol==ID_SELECTOR:
                elements = dom.find_child_by_id(name, root)
            if not root:
                return None
        return elements

    def create_style(self, render_object, css_property, css_value):
        for prop in render_object.properties:
            if css_property in prop.properties:
                num_unit = re.match(t_NUM_UNIT, css_value)
                if num_unit:
                    css_unit = CSSUnit(num_unit.group("value"), num_unit.group("unit"))
                    #print("   Adding:",css_property,css_unit)
                    prop.properties[css_property] = css_unit
                else:
                    #print("   Adding:",css_property,css_value)
                    prop.properties[css_property] = css_value


