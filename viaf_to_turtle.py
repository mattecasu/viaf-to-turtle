#!/usr/bin/env python

import logging
import urllib.parse

from rdflib import *
from rdflib.term import Node

logging.basicConfig(level=logging.ERROR)

viaf_file = 'example.txt'

SKOS = Namespace('http://www.w3.org/2004/02/skos/core#')
SCHEMA = Namespace('http://schema.org/')
OWL = Namespace("http://www.w3.org/2002/07/owl#")
XSD = Namespace("http://www.w3.org/2001/XMLSchema#")

invalid_chars = ["<", ">", '"', ' ', "{", "}", "|", "\\", "^", "`"]


def percent_iri(iri):
    for char in invalid_chars:
        iri = iri.replace(char, urllib.parse.quote(char))
    return iri


def year_or_date(d: Node):
    return Literal(d, datatype=XSD.gYear if d.strip('-').isdigit() else XSD.date)


with open(viaf_file, 'r') as opened_file:
    for line in opened_file:
        if not line.strip():
            continue
        g = Graph()
        newG = Graph()
        newG.bind('skos', SKOS)
        newG.bind('schema', SCHEMA)
        newG.bind('owl', OWL)
        newG.bind('xsd', XSD)
        id = line.split('\t')[0].strip()
        content = line.split('\t')[1]
        g.parse(data=content)
        uri = "http://viaf.org/viaf/" + id
        names = {obj for obj in g.objects(subject=URIRef(uri), predicate=SCHEMA.name) if
                 isinstance(obj, Literal) and obj.language == "en"}
        if not names:
            continue
        name = names.pop()
        prefLabels = {obj for obj in g.objects(None, SKOS.prefLabel)}
        altLabels = {obj for obj in g.objects(None, SKOS.altLabel)}.union(prefLabels)
        birthDate = {obj for obj in g.objects(None, SCHEMA.birthDate)}
        deathDate = {obj for obj in g.objects(None, SCHEMA.deathDate)}
        sameAses = {same for same in g.objects(None, SCHEMA.sameAs)}
        newG.add((URIRef(uri), SKOS.prefLabel, name))
        for altLabel in altLabels:
            newG.add((URIRef(uri), SKOS.altLabel, altLabel))
        if len(birthDate) > 0:
            bd = birthDate.pop()
            newG.add((URIRef(uri), SCHEMA.birthDate, year_or_date(bd)))
        if len(deathDate) > 0:
            dd = deathDate.pop()
            newG.add((URIRef(uri), SCHEMA.deathDate, year_or_date(dd)))
        for sameAs in sameAses:
            newG.add((URIRef(uri), OWL.sameAs, URIRef(percent_iri(sameAs))))
        out_file = f'VIAF_out/{id}.ttl'
        newG.serialize(out_file)
