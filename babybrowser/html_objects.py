#!/usr/bin/env python3

from .css_objects import *

CLASS = "class"
ID = "id"

class Html_Object:

    def __init__(self, parent, children, css=None):
        self.parent = parent
        if children==None:
            self.children = []
        else:
            self.children = children
        self.attrs = {CLASS:None, ID:None}
        self.parse_state = None
        if css:
            self.css = css
        else:
            self.css = RenderObject(BoxStyle.BLOCK)

    def get_property_dict(self, prop_name):
        for prop in self.css.properties:
            if prop_name in prop.properties:
                return prop.properties

    def get_css_property(self, prop_name, prop_type=None):
        prop_dict = self.get_property_dict(prop_name)
        if prop_dict[prop_name]:
            return prop_dict[prop_name]
        if self.parent:
            prop_value = self.parent.get_css_property(prop_name)
            if prop_value and not prop_dict[prop_name]:
                prop_dict[prop_name] = prop_value
            return prop_value
        return None
        #return self.css.get(key) or self.parent.get_css_property(key)

class Text(Html_Object):

    def __init__(self, content, original_text=None, parent=None):
        super().__init__(parent, None)
        self.content = content
        self.original_text = original_text

    def __repr__(self):
        return self.content

class Tag(Html_Object):

    SELF_CLOSING = ['br','img', 'hr']

    def __init__(self, tag, content=None, parent=None, children=None):
        super().__init__(parent, children)
        self.tag = tag
        self.content = content
        if tag in Tag.SELF_CLOSING:
            self.is_self_closing = True
        else:
            self.is_self_closing = False

    def add_attr(self, attr_name, attr_value):
        if attr_name.lower()==CLASS:
            self.attrs[CLASS] = attr_value.split()
        elif attr_name.lower()==ID:
            self.attrs[ID] = attr_value
        else:
            self.attrs[attr_name] = attr_value

    def __str__(self):
        return self.tag

    def __repr__(self):
        return self.__str__()

class DOM:

    FIND_BY_TAG = "tag"
    FIND_BY_ID = "id"
    FIND_BY_CLASS = "class"

    def __init__(self, root=None):
        self.root = root
        self.current_level = None

    def add_text(self, text_object):
        if self.root:
           self.current_level.children.append(text_object)
           text_object.parent = self.current_level
        else:
            raise ValueError("text is the only element in html given")

    def add_child(self, html_object):
        if self.root:
           self.current_level.children.append(html_object)
           html_object.parent = self.current_level
           self.current_level = html_object
        else:
            self.root = html_object
            self.current_level = self.root

    def close_child(self):
        self.current_level = self.current_level.parent

    def add_content(self, content):
        self.current_level.content = content

    def find_children_by_class(self, child_name, root=None):
       if root:
            return self._find_children_helper(root, child_name.lower(), DOM.FIND_BY_CLASS, [])
       return self._find_children_helper(self.root, child_name.lower(), DOM.FIND_BY_CLASS, [])

    def find_child_by_id(self, child_name, root=None):
       if root:
            results, result_root = self._find_children_helper(root, child_name.lower(), DOM.FIND_BY_ID, [])
       else:
            results, result_root = self._find_children_helper(self.root, child_name.lower(), DOM.FIND_BY_ID, [])
       if results:
            return results[0]
       else:
            return None

    def find_children_by_tag(self, child_name, root=None):
       if root:
            return self._find_children_helper(root, child_name.lower(), DOM.FIND_BY_TAG, [])
       return self._find_children_helper(self.root, child_name.lower(), DOM.FIND_BY_TAG, [])

    def _find_children_helper(self, root, child_name, find_by, results=[]):
        #print("Root:{}, Name:{}, Find:{}, Results:{}".format(root, child_name, find_by, results))
        if root and isinstance(root, Tag):
            if find_by==DOM.FIND_BY_TAG and root.tag==child_name:
                results.append(root)
            elif find_by==DOM.FIND_BY_CLASS and root.attrs[CLASS] and child_name in root.attrs[CLASS]:
                results.append(root)
            elif find_by==DOM.FIND_BY_ID and root.attrs[ID]==child_name:
                results.append(root)
                return results
            for child in root.children:
                child_results = self._find_children_helper(child, child_name, find_by, results)
            return results

    def __str__(self):
        return self.str_traverse(self.root, 0)

    def str_css(self):
        return self.str_traverse(self.root, 0, True)

    def str_traverse(self, root, level, css=False):
        if isinstance(root, Tag):
            lst_root = "  "*level+str(root)
            if root.content and not css:
                lst_root += "\n"+("  "*(level+1))+str(root.content)
        else:
            lst_root = "  "*level+"data:"+str(root)
        if root.css and css:
            lst_root += "\n"+("  "*(level+1))+str(root.css)
        for child in root.children:
            lst_root+= "\n"+self.str_traverse(child, level+1, css)
        return lst_root

    def __repr__(self):
        return self.__str__()



