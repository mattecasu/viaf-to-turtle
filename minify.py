import os

from rdflib import Graph

viaf_file = os.path.expanduser('~') + '/Desktop/example.xml'
out = os.path.expanduser('~') + '/Desktop/example.nt'

g = Graph()
g.parse(viaf_file)
g.serialize(out, format='nt')

# cat example.nt | tr -d '\n' > example.txt
