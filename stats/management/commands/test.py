from colour import Color

def color_filter(w,l):
    total = w+l
    green = Color("green")
    red = Color("red")
    colors = list(green.range_to(red, total+1))
    return colors[l]

