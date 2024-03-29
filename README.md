# PyTanja
PyTanja is a graphic simulation of searching algorithms written in Python programming language. The main application window contains two-dimensional map which consists of different kinds of fields and an agent who is moving through the map using a beforehand defined searching algorithm. The final cost of the path depends on the cost of different kinds of fields. The goal is to lead the agent from start to finish.

## Running the application
The program is run from terminal using command:
.\main.py map agent

where
* .\main.py - path to main Python file with source code
* map - relative path to text file with map configuration
* agent - name of the agent class

Before running, it is necessary to install pygame
package within the Python interpreter.

Pressing the SPACE key resumes and pauses the agent
moving through the map. Pressing the ENTER key shows
the final path from start to finish. Pressing the ESC key 
terminates the app and closes the main application window.

## Agents

*Aki* - Agent uses the depth first searching strategy and
gives the advantage to the fields with lower cost, and in
case of two or more fields with the same cost, he chooses 
the field on the certain side of the world (north, east,
south, west).

![Aki](screenshots/Aki.jpg)

*Jocke* - Agent uses the breadth first searching strategy and
gives the advantage to the fields with lower cost of 
his neighbors collectively, and in case of two or more fields
with the same collective cost, he chooses the field
on the certain side of the world (north, east, south, west).

![Jocke](screenshots/Jocke.jpg)

*Draza* - Agent uses branch and bound searching strategy,
and in case of two paths with the same cost, he chooses the
one with less fields in the path, that is any of them in case of 
two or more paths with same number of fields.

![Draza](screenshots/Draza.jpg)

*Bole* - Agent uses A* searching strategy, with heuristic which 
simulates the air distance.

![Bole](screenshots/Bole.jpg)
