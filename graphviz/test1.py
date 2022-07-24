from curses import color_pair
from turtle import fillcolor, filling
from graphviz import Digraph

digraph = Digraph()
# nodes
digraph.node("core", color="blue")
digraph.node("distribution")
digraph.node("access1")
digraph.node("access2", color="red")


# edges
digraph.edge("core", "distribution", label="1Gb")
digraph.edge("distribution", "access1", label="1Gb")
digraph.edge("distribution", "access2", label="100Mb", color="red")

digraph.render("test1_python.gv")