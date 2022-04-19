#!/usr/local/bin/python
"""Steiner.py

The code that follows is not optimal nor is it well organized but it does work.
It solves the Minimum Steiner Problem in relatively small time with Rectilinear
Space in O(n^3 * logn) and Graphical Space in O(n^4 * logn)

Note to self: Add comments and organization to the functions.
Note to reader: Sorry for the lack of comments and organization. See above.
"""

from tkinter import Canvas, Tk, Frame, Button, RAISED, TOP, StringVar, Label, RIGHT, RIDGE
import math

from fontTools.misc.py23 import range
from UnionFind import UnionFind

tk = Tk()
tk.wm_title("Minimum Spanning Tree (MST) vs Steiner Minimum Tree (SMT)")

global originalpoints
originalpoints = []
global steinerpoints
steinerpoints = []
global mst
mst = []
global smt
smt = []


"""Point Class for Steiner.py
Contains position in x and y values with degree of edges representative of the length of
the list of edges relative to the mst
"""


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.deg = 0
        self.edges = []
        self.mstedges = []

    def update(self, edge):
        self.edges.append(edge)

    def reset(self):
        self.edges = []
        self.deg = 0
        self.mstedges = []

    def mstupdate(self, edge):
        self.deg += 1
        self.mstedges.append(edge)


"""Line Class for Steiner.py
Contains the two end points as well as the weight of the line. 
Supports determining the first or last point as well as the other given one. 
"""


class Line:
    def __init__(self, p1, p2, w):
        self.points = []
        self.points.append(ref(p1))
        self.points.append(ref(p2))
        self.w = w

    def getother(self, pt):
        if pt == self.points[0].get():
            return self.points[1]
        elif pt == self.points[1].get():
            return self.points[0]
        else:
            print("This is an Error. The line does not contain points that make sense.")

    def getfirst(self):
        return self.points[0]

    def getlast(self):
        return self.points[1]


"""ref Class for use in Steiner.py
Satisfies the need for pointers to maintain a constant and updated global list of things. 
"""


class ref:
    def __init__(self, obj):
        self.obj = obj

    def get(self):
        return self.obj

    def set(self, obj):
        self.obj = obj


"""addmousepoint 
Calls addpoint if point is not on canvas edge and not on top of another point. 
"""


def addmousepoint(event):
    addpt = True
    if originalpoints == []:
        if (event.x < 10) and (event.x >= 500) and (event.y < 10) and (event.y >= 500):
            addpt = False
    else:
        for pt in originalpoints:
            dist = math.sqrt(pow((event.x - pt.x), 2) + pow((event.y - pt.y), 2))
            if dist < 11:
                addpt = False
            if (event.x < 10) and (event.x >= 500) and (event.y < 10) and (event.y >= 500):
                addpt = False
    if addpt == True:
        addpoint(event.x, event.y)


"""addpoint 
Adds a point at the specified x and y on the Tkinter canvas.
"""


def addpoint(x, y):
    global mst
    del mst[:]
    global smt
    del smt[:]
    canvas.create_oval(x - 5, y - 5, x + 5, y + 5, outline="red", fill="red", width=1)
    point = Point(x, y)
    global originalpoints
    originalpoints.append(point)


"""kruskal's Algorithm
Sorts edges by weight, and adds them one at a time to the tree while avoiding cycles
Takes any set of Point instances and converts to a dictionary via edge crawling 
Takes the dictionary and iterates through each level to discover neighbors and weights
Takes list of point index pairs and converts to list of Lines then returns
"""


def kruskal(setofpoints, type):
    global dist
    for i in range(0, len(setofpoints)):
        setofpoints[i].reset()
    for i in range(0, len(setofpoints)):
        for j in range(i, len(setofpoints)):
            if i != j:
                if type == "R":
                    dist = (abs(setofpoints[i].x - setofpoints[j].x)
                            + abs(setofpoints[i].y - setofpoints[j].y))
                elif type == "g":
                    dist = math.sqrt(pow((setofpoints[i].x - setofpoints[j].x), 2) +
                                     pow((setofpoints[i].y - setofpoints[j].y), 2))
                else:
                    "All of the Errors!"
                line = Line(setofpoints[i], setofpoints[j], dist)
                setofpoints[i].update(line)
                setofpoints[j].update(line)
            else:
                dist = 100000
                line = Line(setofpoints[i], setofpoints[j], dist)
                setofpoints[i].update(line)

    g = {}
    for i in range(0, len(setofpoints)):
        off = 0
        subset = {}
        for j in range(0, len(setofpoints[i].edges)):
            subset[j] = setofpoints[i].edges[j].w
        g[i] = subset

    subtrees = UnionFind()
    tree = []
    for W, u, v in sorted((g[u][v], u, v) for u in g for v in g[u]):
        if subtrees[u] != subtrees[v]:
            tree.append([u, v])
            subtrees.union(u, v)

    mst = []
    for i in range(0, len(tree)):
        point1 = setofpoints[tree[i][0]]
        point2 = setofpoints[tree[i][1]]
        for j in range(0, len(point1.edges)):
            if point2 == point1.edges[j].getother(point1).get():
                point1.mstupdate(point1.edges[j])
                point2.mstupdate(point1.edges[j])
                mst.append(point1.edges[j])
    return mst


"""deltamst	
Determines the difference in a mst's total weight after adding a point. 
"""


def deltamst(setofpoints, testpoint, type):
    if type == "R":
        mst = kruskal(setofpoints, "R")
    else:
        mst = kruskal(setofpoints, "g")

    cost1 = 0
    for i in range(0, len(mst)):
        cost1 += mst[i].w
    combo = setofpoints + [testpoint]

    if type == "R":
        mst = kruskal(combo, "R")
    else:
        mst = kruskal(combo, "g")

    cost2 = 0
    for i in range(0, len(mst)):
        cost2 += mst[i].w
    return cost1 - cost2


"""hananpoints
Produces a set of hananpoints of type Points
"""


def hananpoints(setofpoints):
    totalset = setofpoints
    somepoints = []
    for i in range(0, len(totalset)):
        for j in range(i, len(totalset)):
            if i != j:
                somepoints.append(Point(totalset[i].x, totalset[j].y))
                somepoints.append(Point(totalset[j].x, totalset[i].y))
    return somepoints


"""brutepoints
Produces points with spacing 10 between x values and y values between maximal and minimal 
existing points.
This could use some work...
"""


def brutepoints(setofpoints):
    if setofpoints != []:
        somepoints = []
        xmax = (max(setofpoints, key=lambda x: x.x)).x
        xmin = (min(setofpoints, key=lambda x: x.x)).x
        ymax = (max(setofpoints, key=lambda x: x.y)).y
        ymin = (min(setofpoints, key=lambda x: x.y)).y

        rangex = range(xmin, xmax)
        rangey = range(ymin, ymax)
        for i in rangex[::10]:
            for j in rangey[::10]:
                somepoints.append(Point(i, j))
        return somepoints
    else:
        return []


"""computemst
Computes the Euclidean (Graphical) Minimum Spanning Tree
Uses kruskals to determine the mst of some set of global points and prints to canvas
"""


def computemst():
    canvas.delete("all")
    global mst
    if mst == []:
        mst = kruskal(originalpoints, "g")

    mstmindist = 0
    mstrrq = 0
    for i in range(0, len(mst)):
        mstmindist += mst[i].w
        canvas.create_line(mst[i].points[0].get().x, mst[i].points[0].get().y,
                           mst[i].points[1].get().x, mst[i].points[1].get().y, width=2)
        """print("MST edge distance", [i])
        print(math.ceil((mst[i].w)/100))
        print(mst[i].w)"""
        mstrrq += math.ceil(mst[i].w / 100)

    for i in range(0, len(originalpoints)):
        canvas.create_oval(originalpoints[i].x - 5, originalpoints[i].y - 5,
                           originalpoints[i].x + 5, originalpoints[i].y + 5, outline="green", fill="yellow", width=1)

    msttext.set(str(round(mstmindist, 2)))
    """print("Total MST distance", mstmindist)"""
    mstrrqvar = mstrrq - 2
    print("Total number of repair resources required with MST:", mstrrqvar)


"""computesmt
Computes the Euclidean Graphical Steiner Minimum Spanning Tree
Uses brutepoints as a candidate set of points for possible steiner points. (Approximation factor of <= 2)
deltamst is used to determine which points are beneficial to the final tree.
Any point with less than two degree value (two or fewer edges) is not helpful and is removed.
All final points are printed to the canvas.
"""


def computesmt():
    canvas.delete("all")
    global smt
    if smt == []:
        global steinerpoints
        del steinerpoints[:]
        candidate_set = [0]

        while candidate_set != []:
            maxpoint = Point(0, 0)
            candidate_set = [x for x in brutepoints(originalpoints + steinerpoints) if
                             deltamst(originalpoints + steinerpoints, x, "g") > 0]
            cost = 0
            for pt in candidate_set:
                deltacost = deltamst(originalpoints + steinerpoints, pt, "g")
                if deltacost > cost:
                    maxpoint = pt
                    cost = deltacost

            if maxpoint.x != 0 and maxpoint.y != 0:
                steinerpoints.append(maxpoint)
            for pt in steinerpoints:
                if pt.deg <= 2:
                    steinerpoints.remove(pt)
                else:
                    pass

        smt = kruskal(originalpoints + steinerpoints, "g")

    smtmindist = 0
    smtrrq = 0
    for i in range(0, len(smt)):
        smtmindist += smt[i].w
        canvas.create_line(smt[i].points[0].get().x, smt[i].points[0].get().y,
                           smt[i].points[1].get().x, smt[i].points[1].get().y, width=2)
        """print("SMT edge distance", [i])
        print(smt[i].w)
        print("ceil(UV/R)", [i])
        print(math.ceil((smt[i].w)/100))"""
        smtrrq += math.ceil((smt[i].w)/100)

    for i in range(0, len(steinerpoints)):
        canvas.create_oval(steinerpoints[i].x - 5, steinerpoints[i].y - 5,
                           steinerpoints[i].x + 5, steinerpoints[i].y + 5, outline="black", fill="black", width=3)

    for i in range(0, len(originalpoints)):
        canvas.create_oval(originalpoints[i].x - 5, originalpoints[i].y - 5,
                           originalpoints[i].x + 5, originalpoints[i].y + 5, outline="green", fill="green", width=1)

    smttext.set(str(round(smtmindist, 2)))
    """print("Total SMT distance", smtmindist)"""
    smtrrq = smtrrq - 2
    print("Total number of repair resources required with SMT:", smtrrq)


"""clear
Cleans the global lists and canvas points and text.
"""


def clear():
    global originalpoints
    del originalpoints[:]
    global steinerpoints
    del steinerpoints[:]
    global mst
    del mst[:]
    global smt
    del smt[:]
    msttext.set("-----")
    smttext.set("-----")
    canvas.delete("all")


master = Canvas(tk)
but_frame = Frame(master)
button1 = Button(but_frame, text="MST", command=computemst)
button1.configure(width=9, activebackground="yellow", relief=RAISED)
button1.pack(side=TOP)
var = StringVar()
var.set("Distance:")
Label(but_frame, textvariable=var).pack()
msttext = StringVar()
Label1 = Label(but_frame, textvariable=msttext)
Label1.pack()
print("Range = 100")

Label(but_frame, textvariable="").pack()
button2 = Button(but_frame, text="SMT", command=computesmt)
button2.configure(width=9, activebackground="green", relief=RAISED)
button2.pack(side=TOP)
Label(but_frame, textvariable=var).pack()
smttext = StringVar()
label2 = Label(but_frame, textvariable=smttext)
label2.pack()

Label(but_frame, textvariable="").pack()
button3 = Button(but_frame, text="Reset", command=clear)
button3.configure(width=9, activebackground="black", relief=RAISED)
button3.pack(side=TOP)
but_frame.pack(side=RIGHT, expand=0)
canvas = Canvas(master, width=500, height=500, bd=2, relief=RIDGE, bg="white")
canvas.bind("<Button-1>", addmousepoint)
canvas.pack(expand=0)
master.pack(expand=0)

msttext.set("-----")
smttext.set("-----")

# Testing Points

# addpoint(161, 88)
# addpoint(103, 222)
# addpoint(310, 143)
# addpoint(256, 282)

# End of testing

tk.mainloop()
