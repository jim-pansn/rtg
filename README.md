# rtg
A Recursive Realistic Graph Generator using Random Typing

## What does this code?
This code can be used to generate random graphs, that obey a bunch of properties which can be observed in real graphs.
These properties are:

## How are the graphs generated?
The general idea is to create character sequences by rondomly typing on a keyboard (base set of characters). These sequence are created in tupels and form the set of edges of the graph.


## Usage
Main function of this package is the `rtg(num_edges, num_chars, beta, q, num_timeticks, bipartite=False, self_loop=False)` function. It takes all needed parameters and outputs the generated graph as an edge list. The edege list can directly be used by the [`add_edges_from`](https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.DiGraph.add_edges_from.html) function of the [networx](https://networkx.github.io/) package.

#### Parameters 

 - `num_edges`: The number of edges that should be generated
 - `num_chars`: The number of characters used in the keyboard
 - `beta`: The bias factor that penalizes adding different charactes to the sequences. See the [paper](http://www3.cs.stonybrook.edu/~leman/pubs/RTG_GraphGenerator.pdf) for further information
 - `q`: probability of the *delimeter key*
 - `num_timeticks`: The number of timeticks in which edges were created
 - `bibartite`: Boolean flag that defines weather the generated graph should be bepartite or not
 - `self_loop`: Boolean flag that defines weather the graph can contain self loops or not



## Installation


## Credits
The code is based on the paper [RTG: A Recursive Realistic Graph Generator using Random Typing](http://www3.cs.stonybrook.edu/~leman/pubs/RTG_GraphGenerator.pdf) by [Leman Akoglu](http://www3.cs.stonybrook.edu/~leman/) and works similar to its [MATLAB implementation](http://www3.cs.stonybrook.edu/~leman/pubs.html#code)