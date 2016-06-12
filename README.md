# viaf-to-turtle
Script for converting the Viaf dump in Turtle
<br/>
Assuming a one-RDF-per-line Viaf dump, the script will generate a Turtle with basic info about each person.
<br/>
Minor issue: the script will print prefixes multiple times on the output file. Afterwards, remove the prefixes, e.g. by using using a bash script.