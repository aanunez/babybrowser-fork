#!/usr/bin/env python3

class RenderObject:

    def __init__(self, display):
        self.box_style = BoxStyle(display)
        self.font = Font()
        self.properties = [self.box_style, self.font]

    def get_set_properties(self):
        result = {}
        for prop in self.properties:
            prop_result = prop.get_set_properties()
            result.update(prop_result)
        return result

    def __repr__(self):
        return str(self.properties)

class CSSUnit:

    PIXEL = "px"
    POINT = "pt"
    PERCENT = "%"
    TYPES = [PIXEL, POINT, PERCENT]

    def __init__(self, value, unit):
        self.unit = unit
        self.value = int(value)

    def __repr__(self):
        return "{}{}".format(self.value, self.unit)

class Text:

    CENTER = "center"
    LEFT = "left"
    RIGHT = "right"
    JUSTIFY = "justify"
    ALIGNS = [CENTER, LEFT, RIGHT, JUSTIFY]
    NONE = "none"
    OVERLINE = "overline"
    LINE_THROUGH = "line-through"
    UNDERLINE = "underline"
    DECORATIONS = [NONE, OVERLINE, LINE_THROUGH, UNDERLINE]
    UPPERCASE = "uppercase"
    LOWERCASE = "lowercase"
    CAPITALIZE = "capitalize"
    TRANSFORMS = [UPPERCASE, LOWERCASE, CAPITALIZE]

    def __init__(self, color=None, align=None, decoration=None, transform=None):
        self.color = color
        self.align = align
        self.decoration = decoration
        self.transform = transform

class CSS_Style:

    def get_set_properties(self):
        return {k: v for k,v in self.properties if v}

    def __repr__(self):
        return str([k+":"+str(v) for k,v in self.properties if v])

class Font(CSS_Style):

    #Property Names
    p_FONT_FAMILY = "font-family"
    p_FONT_STYLE = "font-style"
    p_FONT_SIZE = "font-size"
    p_FONT_WEIGHT = "font-weight"
    #Font Constants
    FONT_STYLE_NORMAL = "normal"
    FONT_STYLE_ITALIC = "italic"
    FONT_STYLES = [FONT_STYLE_NORMAL, FONT_STYLE_ITALIC]
    FONT_WEIGHT_NORMAL = "normal"
    FONT_WEIGHT_BOLD = "bold"
    FONT_WEIGHTS = [FONT_WEIGHT_NORMAL, FONT_WEIGHT_BOLD]

    def __init__(self):
        super().__init__()
        self.properties = {Font.p_FONT_FAMILY:None, Font.p_FONT_STYLE:None,
            Font.p_FONT_SIZE:None, Font.p_FONT_WEIGHT:None}

class BoxStyleAttribute:

    def __init__(self, top=None, right=None, bottom=None, left=None):
        self.top = top
        self.right = right
        self.bottom = bottom
        self.left = left

class Border:

    def __init__(self, top_border=None, right_border=None, bottom_border=None, left_border=None):
        self.style_top = top_border
        self.style_right = right_border
        self.style_bottom = bottom_border
        self.style_left = left_border

class BorderStyle(BoxStyleAttribute):

    def __init__(self, top=None, right=None, bottom=None, left=None, style=None, color=None):
        super().__init__(top, right, bottom, left)
        self.style = style
        self.color = color

class BoxStyle(CSS_Style):

    BLOCK = "block"
    INLINE = "inline"
    INLINE_BLOCK = "inline-block"
    NONE = "none"
    HIDDEN = "hidden"
    VISIBLE = "visible"
    #Properties
    p_BACKGROUND_COLOR = "background-color"
    p_COLOR = "color"
    p_WIDTH = "width"
    p_HEIGHT = "height"
    p_DISPLAY = "display"
    p_VISIBILITY = "visibility"
    p_MAX_WIDTH = "max_width"
    p_MAX_HEIGHT = "max_height"
    p_MIN_WIDTH = "min_width"
    p_MIN_HEIGHT = "min_height"

    def __init__(self, display):
        super().__init__()
        self.properties = {BoxStyle.p_DISPLAY:display, BoxStyle.p_HEIGHT:None,
            BoxStyle.p_WIDTH:None,  BoxStyle.p_BACKGROUND_COLOR:None,
            BoxStyle.p_COLOR:None,  BoxStyle.p_VISIBILITY:BoxStyle.VISIBLE,
            BoxStyle.p_MIN_HEIGHT:None,   BoxStyle.p_MIN_WIDTH:None,
            BoxStyle.p_MAX_HEIGHT:None,   BoxStyle.p_MAX_WIDTH:None}
        #self.margin = BoxStyleAttribute()
        #self.padding = BoxStyleAttribute()
        #self.border = Border()

class Position:

    STATIC = "static"
    RELATIVE = "relative"
    FIXED = "fixed"
    ABSOLUTE = "absolute"
    TYPES = [STATIC, RELATIVE, FIXED, ABSOLUTE]

    def __init__(self, position, top=None, right=None, left=None, bottom=None):
        self.position = position if position in Position.TYPES else None
        self.top = top
        self.right = right
        self.left = left
        self.bottom = bottom



