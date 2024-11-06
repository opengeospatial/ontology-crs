from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, VANN, XSD
import csv
import os

exont={}

gcore = Graph()
gcore.bind("geosrs", "http://www.opengis.net/ont/srs/") 
gcore.bind("skos","http://www.w3.org/2004/02/skos/core#")

gcore.add((URIRef("http://www.opengis.net/ont/srs/geosrs"),RDF.type,OWL.Ontology))
gcore.add((URIRef("http://www.opengis.net/ont/srs/geosrs"),RDFS.label,Literal("SRS Ontology",lang="en")))
gcore.add((URIRef("http://www.opengis.net/ont/srs/geosrs"),VANN.preferredNamespacePrefix,Literal("geosrs",datatype=XSD.string)))
gcore.add((URIRef("http://www.opengis.net/ont/srs/geosrs"),VANN.preferredNamespaceUri,Literal("http://www.opengis.net/ont/srs/",datatype=XSD.anyURI)))



geocrsNS="http://www.opengis.net/ont/srs/"
coreprefix="geosrs"

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/class/')



directory = os.fsencode(abspath)
    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    g = Graph()
    exont[filename.replace(".csv","")]=g
    curprefix="geo"+filename.replace(".csv","")
    curns="http://www.opengis.net/ont/srs/"+filename.replace(".csv","")+"/"
    g.bind(curprefix,curns) 
    g.bind("skos","http://www.w3.org/2004/02/skos/core#")

    g.add((URIRef("http://www.opengis.net/ont/srs/geosrs/"+filename.replace(".csv","")),RDF.type,OWL.Ontology))
    g.add((URIRef("http://www.opengis.net/ont/srs/geosrs/"+filename.replace(".csv","")),RDFS.label,Literal("SRS Ontology: "+curprefix.capitalize(),lang="en")))
    g.add((URIRef("http://www.opengis.net/ont/srs/geosrs/"+filename.replace(".csv","")),VANN.preferredNamespacePrefix,Literal(curprefix,datatype=XSD.string)))
    g.add((URIRef("http://www.opengis.net/ont/srs/geosrs/"+filename.replace(".csv","")),VANN.preferredNamespaceUri,Literal("http://www.opengis.net/ont/srs/"+filename.replace(".csv","")+"/",datatype=XSD.anyURI)))
    if filename.endswith(".csv"): 
        with open(abspath+filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if "Concept" in row and row["Concept"]!="":
                    core=False
                    if "Core Class?" in row and row["Core Class?"]=="Core Ontology":
                        core=True
                        gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.Class))
                        if "Label" in row and row["Label"]!="":
                            gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                        if "Definition" in row and row["Definition"]!="":
                            gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                        if "SuperClass" in row and row["SuperClass"]!="":
                            if " " in row["SuperClass"]:
                                for spl in row["SuperClass"].split(" "):
                                    gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.subClassOf,URIRef(spl.replace("geosrs:",geocrsNS))))
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.subClassOf,URIRef(row["SuperClass"].replace("geosrs:",geocrsNS))))
                    else:
                        g.add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDF.type,OWL.Class))
                        if "Label" in row and row["Label"]!="":
                            g.add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDFS.label,Literal(row["Label"],lang="en")))
                        if "Definition" in row and row["Definition"]!="":
                            g.add((URIRef(row["Concept"].replace(curprefix+":",curns)),SKOS.definition,Literal(row["Definition"],lang="en")))
                        if "SuperClass" in row and row["SuperClass"]!="":
                            if " " in row["SuperClass"]:
                                for spl in row["SuperClass"].split(" "):
                                    g.add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDFS.subClassOf,URIRef(spl.replace(curprefix+":",curns))))
                            else:
                                g.add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDFS.subClassOf,URIRef(row["SuperClass"].replace(curprefix+":",curns))))                     
    else:
        continue
 

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/prop/')
directory = os.fsencode(abspath)
print(abspath)    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    g = Graph()
    curprefix="geo"+filename.replace(".csv","")
    curns="http://www.opengis.net/ont/srs/"+filename.replace(".csv","")+"/"
    g.bind(curprefix, curns) 
    g.bind("skos","http://www.w3.org/2004/02/skos/core#")


    g.add((URIRef("http://www.opengis.net/ont/srs/geosrs/"+filename.replace(".csv","")),RDF.type,OWL.Ontology))
    g.add((URIRef("http://www.opengis.net/ont/srs/geosrs/"+filename.replace(".csv","")),RDFS.label,Literal("SRS Ontology: "+curprefix.capitalize(),lang="en")))
    g.add((URIRef("http://www.opengis.net/ont/srs/geosrs/"+filename.replace(".csv","")),VANN.preferredNamespacePrefix,Literal(curprefix,datatype=XSD.string)))
    g.add((URIRef("http://www.opengis.net/ont/srs/geosrs/"+filename.replace(".csv","")),VANN.preferredNamespaceUri,Literal(curns,datatype=XSD.anyURI)))
    if filename.endswith(".csv"): 
        with open(abspath+filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            objprop=False
            if "obj" in filename:
                objprop=True
            for row in reader:
                print(row)
                if "Concept" in row and row["Concept"]!="":
                    if "Core Property?" in row:
                        if row["Core Property?"]=="Core Ontology":
                            core=True
                            if objprop:
                                gcore.add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDF.type,OWL.ObjectProperty))
                            else:
                                gcore.add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDF.type,OWL.DatatypeProperty))
                            if "Label" in row and row["Label"]!="":
                                gcore.add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDFS.label,Literal(row["Label"],lang="en")))
                            if "Definition" in row and row["Definition"]!="":
                                gcore.add((URIRef(row["Concept"].replace(curprefix+":",curns)),SKOS.definition,Literal(row["Definition"],lang="en")))
                            if "Range" in row and row["Range"]!="":
                                gcore.add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDFS.range,URIRef(row["Range"].replace("geosrs:",geocrsNS))))
                            if "Domain" in row and row["Domain"]!="":
                                gcore.add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDFS.domain,URIRef(row["Domain"].replace("geosrs:",geocrsNS))))
                        else:
                            if row["Core Property?"].lower() in exont:
                                if objprop:
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDF.type,OWL.ObjectProperty))
                                else:
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDF.type,OWL.DatatypeProperty))
                                if "Label" in row and row["Label"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDFS.label,Literal(row["Label"],lang="en")))
                                if "Definition" in row and row["Definition"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(curprefix+":",curns)),SKOS.definition,Literal(row["Definition"],lang="en")))
                                if "Range" in row and row["Range"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDFS.range,URIRef(row["Range"].replace("geosrs:",geocrsNS))))
                                if "Domain" in row and row["Domain"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(curprefix+":",curns)),RDFS.domain,URIRef(row["Domain"].replace("geosrs:",geocrsNS))))
            g.serialize(destination=filename.replace(".csv","")+".ttl") 
    else:
        continue

print(len(g))
for item in exont:
    exont[item].serialize(destination=item+".ttl") 
gcore.serialize(destination="index.ttl")
       
g=Graph() 
g.bind("ign","http://data.ign.fr/def/ignf#")      
g.bind("iso19111","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#")   
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
                    g.add((URIRef(row["Concept source"].replace("geosrs:",geocrsNS).replace("ign:","http://data.ign.fr/def/ignf#").replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#")),
                           URIRef(row["Property"].replace("owl:","http://www.w3.org/2002/07/owl#").replace("rdfs:","http://www.w3.org/2000/01/rdf-schema#")),
                           URIRef(row["Concept target"].replace("geosrs:",geocrsNS).replace("ign:","http://data.ign.fr/def/ignf#").replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#"))))
    else:
        continue

g.serialize(destination="alignments.ttl")
