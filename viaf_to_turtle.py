#!/usr/bin/env python

import rdflib, logging, urllib
from rdflib import *

logging.basicConfig(level=logging.ERROR)

viaf_file = open('viaf_persons', 'r')

newFile = open('viaf_to_turtle.ttl', 'w')

SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SCHEMA = Namespace('http://schema.org/')
OWL = Namespace("http://www.w3.org/2002/07/owl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

invalid_chars = ["<", ">", '"', ' ', "{", "}", "|", "\\", "^", "`"]

def percentIri(iri):
  for char in invalid_chars:
    iri = iri.replace(char, urllib.quote(char))
  return iri

for line in viaf_file:
  g = Graph()
  newG = Graph()
  newG.bind('skos', SKOS)
  newG.bind('schema', SCHEMA)
  newG.bind('owl', OWL)
  newG.bind('xsd', XSD)
  id = line.split('\t')[0].strip()
  content = line.split('\t')[1]
  g.parse(data = content)
  uri = "http://viaf.org/viaf/" + id
  names = {obj for obj in g.objects(subject=URIRef(uri), predicate=SCHEMA.name) if obj.language=="en"}
  if len(names) == 0:
    continue
  name = Literal(names.pop().strip())
  prefLabels = {obj for obj in g.objects(None, SKOS.prefLabel)}
  altLabels = {obj for obj in g.objects(None, SKOS.altLabel)}.union(prefLabels)
  birthDate = {obj for obj in g.objects(None, SCHEMA.birthDate)}
  deathDate = {obj for obj in g.objects(None, SCHEMA.deathDate)}
  sameAses = {same.strip() for same in g.objects(None, SCHEMA.sameAs)}
  newG.add((URIRef(uri), SKOS.prefLabel, name))
  for altLabel in altLabels:
    newG.add((URIRef(uri), SKOS.altLabel, altLabel))
  if len(birthDate)>0:
    bd = birthDate.pop()
    type = XSD.gYear if bd.strip('-').isdigit() else XSD.date
    newG.add((URIRef(uri), SCHEMA.birthDate, Literal(bd, datatype=type)))
  if len(deathDate)>0:
    dd = deathDate.pop()
    type = XSD.gYear if dd.strip('-').isdigit() else XSD.date
    newG.add((URIRef(uri), SCHEMA.deathDate, Literal(dd, datatype=type)))
  for sameAs in sameAses:
    newG.add((URIRef(uri), OWL.sameAs, URIRef(percentIri(sameAs))))
  newG.serialize(newFile, format='turtle')
    
viaf_file.close()
newFile.close()