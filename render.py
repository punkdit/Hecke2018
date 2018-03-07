#!/usr/bin/env python3

"""
Convert transcrypt html5 canvas code into PyX calls
and generate svg files in output directory.
"""

import sys, os
from math import *

import pyx 
from pyx import path, deco, trafo, style, text, color, deformer
from pyx.color import rgb, cmyk


text.set(mode="latex") 
#text.set(docopt="12pt") # broken
text.preamble(r"\usepackage{amsmath,amsfonts,amssymb}")


black = rgb(0., 0., 0.) 
blue = rgb(0., 0., 0.8)
lred = rgb(1., 0.4, 0.4)
white = rgb(1., 1., 1.) 

#shade = rgb(0.75, 0.55, 0)

grey = rgb(0.75, 0.75, 0.75)
shade = grey
shade0 = rgb(0.75, 0.75, 0.75)
shade1 = rgb(0.80, 0.80, 0.80)
shade2 = rgb(0.85, 0.85, 0.85)

light_shade = rgb(0.85, 0.65, 0.1)
light_shade = rgb(0.9, 0.75, 0.4)


north = [text.halign.boxcenter, text.valign.top]
northeast = [text.halign.boxright, text.valign.top]
northwest = [text.halign.boxleft, text.valign.top]
south = [text.halign.boxcenter, text.valign.bottom]
southeast = [text.halign.boxright, text.valign.bottom]
southwest = [text.halign.boxleft, text.valign.bottom]
east = [text.halign.boxright, text.valign.middle]
west = [text.halign.boxleft, text.valign.middle]
center = [text.halign.boxcenter, text.valign.middle]


st_dashed = [style.linestyle.dashed]
st_dotted = [style.linestyle.dotted]
st_round = [style.linecap.round]
#st_mitre = [style.linecap.square]

st_thick = [style.linewidth.thick]
st_Thick = [style.linewidth.Thick]
st_THick = [style.linewidth.THick]
st_THIck = [style.linewidth.THIck]
st_THICk = [style.linewidth.THICk]
st_THICK = [style.linewidth.THICK]


# -----------------------------------------------------------------------------

c = pyx.canvas.canvas()


W = 2.
H = 2.
r = 0.2
dx = 0.4

x, y = 0., 0.

c.text(x, y, "structure", north)
c.stroke(path.line(x-dx, y+r, x, y+H))
c.stroke(path.line(x+dx, y+r, x, y+H))
c.stroke(path.line(x-dx, y+r, x+dx, y+r))

x += W
c.text(x, y, "symmetry", north)
c.stroke(path.line(x, y+r, x-dx, y+H))
c.stroke(path.line(x, y+r, x+dx, y+H))
c.stroke(path.line(x-dx, y+H, x+dx, y+H))


c.writePDFfile("pic-structure")


# -----------------------------------------------------------------------------


def triangle(x, y, r, deco=[]):

    theta = 0.
    ps = [path.moveto(x + r*sin(theta), y + r*cos(theta))]
    theta += 2*pi/3
    ps.append(path.lineto(x + r*sin(theta), y + r*cos(theta)))
    theta += 2*pi/3
    ps.append(path.lineto(x + r*sin(theta), y + r*cos(theta)))
    ps.append(path.closepath())
    c.stroke(path.path(*ps), deco)


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 1.
triangle(x, y, r, st_THick)

c.writePDFfile("pic-triangle")



# -----------------------------------------------------------------------------


def numbered(x, y, r, nums):

    triangle(x, y, 0.8*r, st_THick)
    theta = 0.
    c.text(x + r*sin(theta), y + r*cos(theta), nums[0], south)
    theta -= 2*pi/3
    c.text(x + r*sin(theta), y + r*cos(theta), nums[1], northeast)
    theta -= 2*pi/3
    c.text(x + r*sin(theta), y + r*cos(theta), nums[2], northwest)


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.7
R = 2.

numbered(x, y, r, "123")
x += R
numbered(x, y, r, "132")
x += R
numbered(x, y, r, "321")
x += R
numbered(x, y, r, "213")
x += R
numbered(x, y, r, "312")
x += R
numbered(x, y, r, "231")
x += R

c.writePDFfile("pic-triangle-numbered")


# -----------------------------------------------------------------------------


def flaged(x, y, r, flags):

    for (i, a) in flags:
        assert i in [0, 1, 2]
        assert a in [0, 1]
    
        theta = 2*pi*i/3
        x0, y0 = (x, y)
        x1, y1 = (x + r*sin(theta), y + r*cos(theta))
        theta += 2*pi/6 if a else -2*pi/6
        x2, y2 = (x + 0.5*r*sin(theta), y + 0.5*r*cos(theta))
    
        p = path.path(
            path.moveto(x0, y0),
            path.lineto(x1, y1),
            path.lineto(x2, y2),
            path.closepath())
        c.stroke(p, [grey])
        c.fill(p, [grey])

    triangle(x, y, r, st_THick)


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.8
R = 2.

flags = [ (0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0)]
for flag in flags:
    flaged(x, y, r, [flag]); x += R

c.writePDFfile("pic-triangle-frames")


# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.8
R = 2.

for i in range(3):
    st = [(i, 0), (i, 1)]
    flaged(x, y, r, st); x += R

c.writePDFfile("pic-triangle-points")


# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.8
R = 2.


flaged(x, y, r, [(i, 0) for i in range(3)]); x += R
flaged(x, y, r, [(i, 1) for i in range(3)]); x += R

c.writePDFfile("pic-triangle-orientations")


# -----------------------------------------------------------------------------


c = pyx.canvas.canvas()

x, y = 0., 0.
r = 0.5
R = r*2./0.8

tabs = [0., 5*r, 10*r, 10*r+6*R]

def dorow():
    c.stroke(path.rect(tabs[0]-r, y-r, tabs[3]-tabs[0], R))

dorow()
c.text(x, y, "structure", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "subgroup", [pyx.text.size.large])
x = tabs[2]
c.text(x-r, y, "orbit", [pyx.text.size.large])
y -= R; x = tabs[0]
y -= 0.1

dorow()
c.text(x, y, "nothing", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$A$", [pyx.text.size.large])
x = tabs[2]
flaged(x, y, r, []); x += R
y -= R; x = tabs[0]

dorow()
c.text(x, y, "orientation", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$B$", [pyx.text.size.large])
x = tabs[2]
flaged(x, y, r, [(i, 0) for i in range(3)]); x += R
flaged(x, y, r, [(i, 1) for i in range(3)]); x += R
#c.writePDFfile("pic-triangle-orientations")
y -= R; x = tabs[0]


dorow()
c.text(x, y, "point", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$C$", [pyx.text.size.large])
x = tabs[2]
for i in range(3):
    st = [(i, 0), (i, 1)]
    flaged(x, y, r, st); x += R
#c.writePDFfile("pic-triangle-points")
y -= R; x = tabs[0]


dorow()
c.text(x, y, "frame", [pyx.text.size.large])
x = tabs[1]
c.text(x, y, "$D$", [pyx.text.size.large])
x = tabs[2]
flags = [ (0, 0), (0, 1), (1, 1), (2, 1), (2, 0), (1, 0)]
for flag in flags:
    flaged(x, y, r, [flag]); x += R
#c.writePDFfile("pic-triangle-frames")
y -= R; x = tabs[0]

#c.stroke(path.line(tabs[1], 0, tabs[1], y))

c.writePDFfile("pic-triangle-structures")

# -----------------------------------------------------------------------------












