from django import template
from colour import Color

register = template.Library()

@register.filter()
def color_filter(w,l):
    if w==l==0:
        return '#bfbf00'
    green = Color("green")
    red = Color("red")
    colors = list(green.range_to(red, w+l+1))
    return colors[l]

    # green = Color("green")
    # red = Color("red")
    # white = Color("white")
    # green_range = list(green.range_to(white, w+l+1))
    # red_range = list(white.range_to(red, w+l+1))
    # colors = green_range + red_range[1:]
    # return colors[l*2]