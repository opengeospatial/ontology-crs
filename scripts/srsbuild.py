from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, VANN, XSD
import csv
import os
import re
import json

pattern = re.compile(r'(?<!^)(?=[A-Z])')

def convertCamelToSnake(strr):
 return pattern.sub('_', strr).lower()

exont={}

ldcontext={"@context":{"rdfs":"http://www.w3.org/2000/01/rdf-schema#","rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
                        "om": "http://www.ontology-of-units-of-measure.org/resource/om-2/","geosrs":"https://w3id.org/geosrs#",
                       "skos":"http://www.w3.org/2004/02/skos/core#",
                       "name":"rdfs:label", "value":"rdf:value","method":"geosrs:coordinateOperation",
                       "scope":"skos:scopeNote","direction":"geosrs:axisDirection","abbreviation":"skos:altLabel",
                       "down:":"geosrs:down","down:":"geosrs:up","north:":"geosrs:north","south:":"geosrs:south",
                       "centimetre":"om:centimetre", "millimetre":"om:millimetre","unity":"om:unity",
                       "kilometre":"om:kilometre", "degree":"om:degree","parameters":"geosrs:OperationParameter",
                       "metre":"om:metre","radian":"om:radian","base_crs":"geosrs:baseCRS",
                       "coordinate_system":"geosrs:CoordinateSystem","ellipsoidal":"EllipsoidalCoordinateSystem",
                       "Cartesian":"geosrs:CartesianCoordinateSystem","GeodeticReferenceFrame":"geosrs:GeodeticDatum",
                       "datum_ensemble":"geosrs:datum",
                       "subtype":{"@id":"rdf:type","@type":"@vocab"},
                       "type":{"@id":"rdf:type","@type":"@vocab"},
                       "unit":{"@id":"om:hasUnit","@type":"@vocab"}
            }
}

prefixtoclasses={"geosrs":[]}
prefixtoproperties={"geosrs":[],"CS":[],"CO":[],"DATUM":[],"projection":[]}
classToPrefix={}

gcore = Graph()
gcore.bind("geosrs", "https://w3id.org/geosrs/") 
gcore.bind("skos","http://www.w3.org/2004/02/skos/core#")

gcore.add((URIRef("https://w3id.org/geosrs"),RDF.type,OWL.Ontology))
gcore.add((URIRef("https://w3id.org/geosrs"),RDFS.label,Literal("SRS Ontology",lang="en")))
gcore.add((URIRef("https://w3id.org/geosrs"),VANN.preferredNamespacePrefix,Literal("geosrs",datatype=XSD.string)))
gcore.add((URIRef("https://w3id.org/geosrs"),VANN.preferredNamespaceUri,Literal("https://w3id.org/geosrs#",datatype=XSD.anyURI)))

geocrsNS="https://w3id.org/geosrs/"
coreprefix="geosrs"

def getPrefixForClass(cls,prefixmap):
    if cls in prefixmap:
        return prefixmap[cls]["prefix"]
    return coreprefix

def getNSForClass(cls,prefixmap):
    if cls in prefixmap:
        return prefixmap[cls]["ns"]
    return geocrsNS

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/class/')

directory = os.fsencode(abspath)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    curprefix="geosrs_"+filename.replace(".csv","")
    curns="https://w3id.org/geosrs/"+filename.replace(".csv","")+"/"
    if filename.endswith(".csv"):
        with open(abspath+filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if "Concept" in row and row["Concept"]!="":
                    if "Core Class?" in row and row["Core Class?"]=="Core Ontology":
                        classToPrefix[row["Concept"]]={"prefix":coreprefix, "ns":geocrsNS}
                    else:
                        classToPrefix[row["Concept"]]={"prefix":curprefix, "ns":curns}

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    g = Graph()
    g.bind("geosrs", "https://w3id.org/geosrs/") 
    exont[filename.replace(".csv","")]=g
    curprefix="geosrs_"+filename.replace(".csv","")
    curns="https://w3id.org/geosrs/"+filename.replace(".csv","")+"/"
    g.bind(curprefix,curns) 
    g.bind("skos","http://www.w3.org/2004/02/skos/core#")
    g.bind(curprefix,curns)

    if curprefix not in prefixtoclasses:
        prefixtoclasses[curprefix]=[]
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")),RDF.type,OWL.Ontology))
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")),RDFS.label,Literal("SRS Ontology: "+curprefix.capitalize(),lang="en")))
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")),VANN.preferredNamespacePrefix,Literal(curprefix,datatype=XSD.string)))
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")),VANN.preferredNamespaceUri,Literal("https://w3id.org/geosrs/"+filename.replace(".csv","")+"/",datatype=XSD.anyURI)))
    if filename.endswith(".csv"): 
        with open(abspath+filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if "Concept" in row and row["Concept"]!="":
                    core=False
                    if "Core Class?" in row and row["Core Class?"]=="Core Ontology":
                        core=True
                        gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.Class))
                        prefixtoclasses[coreprefix].append(row["Concept"].replace(coreprefix+":",geocrsNS))
                        classToPrefix[row["Concept"]]={"prefix":coreprefix, "ns":geocrsNS}
                        if "Label" in row and row["Label"]!="":
                            gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                        if "Definition" in row and row["Definition"]!="":
                            gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                        if "SuperClass" in row and row["SuperClass"]!="":
                            if " " in row["SuperClass"]:
                                for spl in row["SuperClass"].split(" "):
                                    gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.subClassOf,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.subClassOf,URIRef(row["SuperClass"].replace("geosrs:", getNSForClass(row["SuperClass"],classToPrefix)))))
                        if "DisjointClass" in row and row["DisjointClass"]!="":
                            if " " in row["DisjointClass"]:
                                for spl in row["DisjointClass"].split(" "):
                                    gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.subClassOf,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.subClassOf,URIRef(row["DisjointClass"].replace("geosrs:", getNSForClass(row["DisjointClass"],classToPrefix)))))
                    else:
                        g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDF.type,OWL.Class))
                        prefixtoclasses[curprefix].append(row["Concept"].replace(curprefix+":",curns).replace("geosrs:","").replace("geoprojection:",""))
                        classToPrefix[row["Concept"]]={"prefix":curprefix, "ns":curns}
                        if "Label" in row and row["Label"]!="":
                            g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDFS.label,Literal(row["Label"],lang="en")))
                        if "Definition" in row and row["Definition"]!="":
                            g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),SKOS.definition,Literal(row["Definition"],lang="en")))
                        if "SuperClass" in row and row["SuperClass"]!="":
                            if " " in row["SuperClass"]:
                                for spl in row["SuperClass"].split(" "):
                                    g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDFS.subClassOf,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                            else:
                                g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDFS.subClassOf,URIRef(row["SuperClass"].replace("geosrs:", getNSForClass(row["SuperClass"],classToPrefix)))))
                        if "DisjointClass" in row and row["DisjointClass"]!="":
                            if " " in row["DisjointClass"]:
                                for spl in row["DisjointClass"].split(" "):
                                    g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),OWL.disjointWith,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                            else:
                                g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),OWL.disjointWith,URIRef(row["DisjointClass"].replace("geosrs:", getNSForClass(row["DisjointClass"],classToPrefix)))))                      
    else:
        continue
 
#print(prefixtoclasses)
#print(classToPrefix)
dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/prop/')
directory = os.fsencode(abspath)
#print(abspath)    
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    g = Graph()
    curprefix="geosrs_"+filename.replace(".csv","")
    curns="https://w3id.org/geosrs/"
    g.bind(curprefix, curns) 
    g.bind("geosrs", "https://w3id.org/geosrs/") 
    g.bind("skos","http://www.w3.org/2004/02/skos/core#")


    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")),RDF.type,OWL.Ontology))
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")),RDFS.label,Literal("SRS Ontology: "+curprefix.capitalize(),lang="en")))
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")),VANN.preferredNamespacePrefix,Literal(curprefix,datatype=XSD.string)))
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")),VANN.preferredNamespaceUri,Literal(curns,datatype=XSD.anyURI)))
    print(filename)
    if filename.endswith(".csv"): 
        with open(abspath+filename, newline='',encoding="utf-8") as csvfile:
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
                            prefixtoproperties["geosrs"].append(row["Concept"].replace(curprefix+":",curns).replace("geosrs:","").replace("geoprojection:",""))
                            if objprop:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.ObjectProperty))
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.DatatypeProperty))
                            if "Label" in row and row["Label"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                            if "Definition" in row and row["Definition"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                            if "Range" in row and row["Range"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.range,URIRef(row["Range"].replace("geosrs:", getNSForClass(row["Range"],classToPrefix)))))
                            if "Domain" in row and row["Domain"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.domain,URIRef(row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix)))))
                        else:
                            if row["Core Property?"].lower() in exont:
                                if row["Core Property?"]!="":
                                    prefixtoproperties[row["Core Property?"]].append(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/").replace("geosrs:","").replace("geoprojection:",""))
                                if objprop:
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDF.type,OWL.ObjectProperty))
                                else:
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDF.type,OWL.DatatypeProperty))
                                if "Label" in row and row["Label"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDFS.label,Literal(row["Label"],lang="en")))
                                if "Definition" in row and row["Definition"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),SKOS.definition,Literal(row["Definition"],lang="en")))
                                if "Range" in row and row["Range"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDFS.range,URIRef(row["Range"].replace("geosrs:",getNSForClass(row["Range"],classToPrefix)))))
                                if "Domain" in row and row["Domain"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDFS.domain,URIRef(row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix)))))
            g.serialize(destination=filename.replace(".csv","")+".ttl") 
    else:
        continue


dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/instance/')
directory = os.fsencode(abspath)
print(abspath)    
curprefix="geosrs_"+filename.replace(".csv","")
curns="https://w3id.org/geosrs/"
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".csv"): 
        with open(abspath+filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                if "Concept" in row and row["Concept"]!="":
                    if "Module" in row:
                        if row["Module"]=="Core Ontology":
                            core=True
                            prefixtoproperties["geosrs"].append(row["Concept"].replace(coreprefix+":",geocrsNS).replace("geoprojection:",""))
                            if "Type" in row and row["Type"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,URIRef(row["Type"].replace(coreprefix+":",geocrsNS))))
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.NamedIndividual))
                            if "Label" in row and row["Label"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                            if "Definition" in row and row["Definition"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                        else:
                            if row["Module"].lower() in exont:
                                if row["Module"]!="":
                                    prefixtoproperties[row["Module"]].append(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/").replace("geosrs:","").replace("geoprojection:",""))
                                if "Type" in row and row["Type"]!="":
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDF.type,URIRef(row["Type"].replace("geosrs:",getNSForClass(row["Type"],classToPrefix)))))
                                else:
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDF.type,OWL.NamedIndividual))
                                if "Label" in row and row["Label"]!="":
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDFS.label,Literal(row["Label"],lang="en")))
                                if "Definition" in row and row["Definition"]!="":
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),SKOS.definition,Literal(row["Definition"],lang="en")))
            g.serialize(destination=filename.replace(".csv","")+".ttl") 
    else:
        continue


print(len(g))
for item in exont:
    exont[item].serialize(destination=item+".ttl") 
gcore.serialize(destination="index.ttl")
       
g=Graph() 
g.bind("ign","http://data.ign.fr/def/ignf#")  
g.bind("ifc","https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2_TC1/OWL/")  
g.bind("iso19111","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#")   
g.bind("geosrs", "https://w3id.org/geosrs/")  
g.add((URIRef("https://w3id.org/geosrs/alignments/"),RDF.type,OWL.Ontology))
g.add((URIRef("https://w3id.org/geosrs/alignments/"),RDFS.label,Literal("SRS Ontology Alignments",lang="en")))
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
                    g.add((URIRef(row["Concept source"].replace("geosrs:",geocrsNS).replace("ign:","http://data.ign.fr/def/ignf#").replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#").replace("ifc:","https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2_TC1/OWL/")),
                           URIRef(row["Property"].replace("owl:","http://www.w3.org/2002/07/owl#").replace("rdfs:","http://www.w3.org/2000/01/rdf-schema#")),
                           URIRef(row["Concept target"].replace("geosrs:",geocrsNS).replace("ign:","http://data.ign.fr/def/ignf#").replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#").replace("ifc:","https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2_TC1/OWL/"))))
    else:
        continue

g.serialize(destination="alignments.ttl")

for pref in prefixtoclasses:
    if pref!="geosrs_srs":
        ldcontext["@context"][pref]=geocrsNS[:-1]+"/"+pref.replace("geosrs_","")+"/"
    for cls in prefixtoclasses[pref]:
        ldcontext["@context"][cls[cls.rfind('/')+1:]]=pref.replace("geosrs_srs","geosrs")+":"+cls[cls.rfind('/')+1:]
    if pref in prefixtoproperties:
        for cls in prefixtoproperties[pref]:
            ldcontext["@context"][convertCamelToSnake(cls[cls.rfind('/')+1:])]=pref.replace("geosrs_srs","geosrs")+":"+cls[cls.rfind('/')+1:]
print(prefixtoproperties)
os.mkdir("context")
with open('context/geosrs-context.json', 'w',encoding="utf-8") as f:
    json.dump(ldcontext, f,indent=2,sort_keys=True)

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../examples/')
directory = os.fsencode(abspath)  
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".json"):
       gr = Graph()
       gr.parse(location=abspath+filename, format='json-ld')
       gr.serialize(destination=abspath+filename.replace(".json",".ttl"), format='turtle')
