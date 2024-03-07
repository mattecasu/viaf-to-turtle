# viaf-to-turtle

Script for converting the Viaf dump (http://viaf.org/viaf/data) in smaller Turtle files.

Assuming a one-RDF-per-line Viaf dump, the script will generate a Turtle file with basic info
for each person, using `rdflib` (https://github.com/RDFLib/rdflib).
