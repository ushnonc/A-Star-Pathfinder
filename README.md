# A* Search / Pathfinder
### **A\* Search algorithm background**
The A* Search algorithm is a search algorithm used to find the shortest path between two nodes 
in a graph traversal or path search setting. A* is similar to other path-finding algorithms like Djikstra's.
The efficiency of A* search is highly dependent on how many nodes the algorithm's heuristic function is able to remove 
from the list of expandable nodes. Presently, the A* search algorithm has diverse use cases from video games to
artificial intelligence.

### How the algorithm works
The algorithm is an *informed search algorithm*, so the algorithm works by processing the
weighted edges between search nodes. The algorithm itself is defined by the function:

#### ***F(n)* = *G(n)* + *H(n)***

In the above formula, *F(n)* and *G(n)* refer to the F-score and G-score, respectively.

*H(n)*, or the heuristic function, is a function that estimates the lowest cost (or distance) of traversing
to the endpoint node. By using a valid heuristic function, A* search returns 
the most efficient path.

The G-score refers to the distance from the start node to the current node, and when summed with the 
result of the heuristic function, returns the F-score. That value determines the
shortest path.

### A* Search in this demo
In my implementation of the A* algorithm, the algorithm uses a priority queue data structure to hold
expandable nodes, and an empty array to store the traversal path. The specific algorithm is commented
on in main.py.

The algorithm is visualized by PyGame.

### How to use the demo
The script is written in Python version 3.9. In order to run the script, you may need to install the pygame module
from pip. I recommended creating a virtual environment to run the script as well.

In the demo, red represents nodes in the closed set, green denotes those in the open set, and the purple path
is the shortest path as found by the A* search algorithm.

Left click to place the start end nodes and then draw the barrier blocks. Right click will clear that
node, however, if the start or end node are deleted, they can be replaced with left click. Press
space to start the search and 'c' to clear the board.

Thank you for checking out my project!

Python 3.9
