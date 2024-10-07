from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, VANN, XSD
import csv
import os

extontmapping={
"srs.csv":"core.ttl",
"cs.csv":"cs.ttl",
"projections.csv":"projections.ttl"
}

g = Graph()
g.bind("geosrs", "http://www.opengis.net/ont/srs/") 
g.bind("skos","http://www.w3.org/2004/02/skos/core#")

g.add((URIRef("http://www.opengis.net/ont/srs/geosrs"),RDF.type,OWL.Ontology))
g.add((URIRef("http://www.opengis.net/ont/srs/geosrs"),RDFS.label,Literal("SRS Ontology",lang="en")))
g.add((URIRef("http://www.opengis.net/ont/srs/geosrs"),VANN.preferredNamespacePrefix,Literal("geosrs",datatype=XSD.string)))
g.add((URIRef("http://www.opengis.net/ont/srs/geosrs"),VANN.preferredNamespaceUri,Literal("http://www.opengis.net/ont/srs/",datatype=XSD.anyURI)))

geocrsNS="http://www.opengis.net/ont/srs/"

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/class/')



directory = os.fsencode(abspath)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"): 
        with open(abspath+filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if "Concept" in row and row["Concept"]!="":
                    g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),RDF.type,OWL.Class))
                    if "Label" in row and row["Label"]!="":
                        g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                    if "Definition" in row and row["Definition"]!="":
                        g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                    if "SubClass" in row and row["SubClass"]!="":
                        g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),RDFS.subClassOf,URIRef(row["SubClass"].replace("geosrs:",geocrsNS))))
    else:
        continue

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/prop/')
directory = os.fsencode(abspath)
print(abspath)    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"): 
        with open(abspath+filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            objprop=False
            if "obj" in filename:
                objprop=True
            for row in reader:
                if "Concept" in row and row["Concept"]!="":
                    if objprop:
                        g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),RDF.type,OWL.ObjectProperty))
                    else:
                        g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),RDF.type,OWL.DatatypeProperty))
                    if "Label" in row and row["Label"]!="":
                        g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                    if "Definition" in row and row["Definition"]!="":
                        g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                    if "Range" in row and row["Range"]!="":
                        g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),RDFS.range,URIRef(row["Range"].replace("geosrs:",geocrsNS))))
                    if "Domain" in row and row["Domain"]!="":
                        g.add((URIRef(row["Concept"].replace("geosrs:",geocrsNS)),RDFS.domain,URIRef(row["Domain"].replace("geosrs:",geocrsNS))))
    else:
        continue

print(len(g))
g.serialize(destination="index.ttl")
       
g=Graph() 
g.bind("ign","http://data.ign.fr/def/ignf#")      
g.bind("iso19112","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#")   
g.bind("geosrs", "http://www.opengis.net/ont/srs/")  
dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/alignment/')
directory = os.fsencode(abspath)
print(abspath)    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"): 
        with open(abspath+filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            objprop=False
            if "obj" in filename:
                objprop=True
            for row in reader:
                if "Concept source" in row and row["Concept source"]!="" and "Concept target" in row and row["Concept target"]!="" and "Property" in row and row["Property"]!="":
                    g.add((URIRef(row["Concept source"].replace("geosrs:",geocrsNS).replace("ign:","http://data.ign.fr/def/ignf#").replace("iso19112:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#")),URIRef(row["Property"].replace("owl:","http://www.w3.org/2002/07/owl#").replace("rdfs:","http://www.w3.org/2000/01/rdf-schema#")),URIRef(geocrsNS+row["Concept target"].replace("geosrs:",geocrsNS).replace("ign:","http://data.ign.fr/def/ignf#").replace("iso19112:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#"))))
    else:
        continue

g.serialize(destination="alignments.ttl")