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
                       "skos":"http://www.w3.org/2004/02/skos/core#","geo":"http://www.opengis.net/ont/geosparql#",
                       "dc":"http://purl.org/dc/elements/1.1/","sf":"http://www.opengis.net/ont/sf#",
                       "name":"rdfs:label", "value":"rdf:value",
                       "scope":"skos:scopeNote","secondDefiningParameter":"geosrs:operationParameter",
                       "abbreviation":"skos:altLabel","alias":"skos:altLabel","geographicElement":"geo:hasBoundingBox","GeographicBoundingBox":"sf:Polygon",
                       "centimetre":"om:centimetre", "millimetre":"om:millimetre","unity":"om:unity",
                       "kilometre":"om:kilometre", "deg":"om:degree","degree":"om:degree","parameters":"geosrs:operationParameter",
                       "m":"om:metre","metre":"om:metre","radian":"om:radian",
                       "identifier":"dc:identifier",
                       "entityType":{"@id":"rdf:type","@type":"@vocab"},
                       "subtype":{"@id":"rdf:type","@type":"@vocab"},
                       "type":{"@id":"rdf:type","@type":"@vocab"},
                       "uom":{"@id":"om:hasUnit","@type":"@vocab"},
                       "axisUnitID":{"@id":"om:hasUnit","@type":"@vocab"},
                       "unit":{"@id":"om:hasUnit","@type":"@vocab"}
            }
}

prefixtoclasses={"geosrs":[]}
prefixtoproperties={"geosrs":[],"CS":[],"CO":[],"DATUM":[],"projection":[]}
classToPrefix={}
prefixToModule={"core":"06-core.adoc","co":"07-co_extension.adoc","cs":"08-cs_extension.adoc","datum":"09-datum_extension.adoc","srsapplication":"10-srsapplication.adoc","projection":"11-projections_extension.adoc","planet":"12-planet_extension.adoc"}
moduleToAdoc={"06-core.adoc":["\n\n"],"07-co_extension.adoc":[],"08-cs_extension.adoc":[],"09-datum_extension.adoc":[],"10-srsapplication.adoc":[],"11-projections_extension.adoc":[],"12-planet_extension.adoc":[]}

gcore = Graph()
gcore.bind("geosrs", "https://w3id.org/geosrs/") 
gcore.bind("skos","http://www.w3.org/2004/02/skos/core#")

gcore.add((URIRef("https://w3id.org/geosrs"),RDF.type,OWL.Ontology))
gcore.add((URIRef("https://w3id.org/geosrs"),RDFS.label,Literal("SRS Ontology",lang="en")))
gcore.add((URIRef("https://w3id.org/geosrs"),VANN.preferredNamespacePrefix,Literal("geosrs",datatype=XSD.string)))
gcore.add((URIRef("https://w3id.org/geosrs"),VANN.preferredNamespaceUri,Literal("https://w3id.org/geosrs/",datatype=XSD.anyURI)))

geocrsNS="https://w3id.org/geosrs/"
coreprefix="geosrs"

def getPrefixForClass(cls,prefixmap):
    if cls in prefixmap:
        return prefixmap[cls]["prefix"]
    return coreprefix

def getNSForClass(cls,prefixmap,g=None):
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

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/instance/')

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
                    if "Module" in row and row["Module"]=="Core Ontology":
                        classToPrefix[row["Concept"]]={"prefix":coreprefix, "ns":geocrsNS}
                    elif "Module" in row:
                        classToPrefix[row["Concept"]]={"prefix":"geosrs_"+str(row["Module"]).lower(), "ns":"https://w3id.org/geosrs/"+str(row["Module"]).lower()+"/"}
                    else:
                        classToPrefix[row["Concept"]]={"prefix":curprefix, "ns":curns}

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/class/')

directory = os.fsencode(abspath)

for file in os.listdir(directory):
    filename = os.fsdecode(file)
    g = Graph()
    g.bind("geosrs", "https://w3id.org/geosrs/") 
    exont[filename.replace(".csv","")]=g
    nsprefix=filename.replace(".csv","")
    curprefix="geosrs_"+filename.replace(".csv","")
    curns="https://w3id.org/geosrs/"+filename.replace(".csv","")+"/"
    g.bind(curprefix,curns) 
    ldcontext["@context"][curprefix]=curns
    g.bind("skos","http://www.w3.org/2004/02/skos/core#")
    g.bind(curprefix,curns)

    if curprefix not in prefixtoclasses:
        prefixtoclasses[curprefix]=[]
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")+filename.replace(".csv","")),RDF.type,OWL.Ontology))
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")+filename.replace(".csv","")),RDFS.label,Literal("SRS Ontology: "+curprefix.capitalize(),lang="en")))
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")+filename.replace(".csv","")),VANN.preferredNamespacePrefix,Literal(curprefix,datatype=XSD.string)))
    g.add((URIRef("https://w3id.org/geosrs/"+filename.replace(".csv","")+filename.replace(".csv","")),VANN.preferredNamespaceUri,Literal("https://w3id.org/geosrs/"+filename.replace(".csv","")+"/",datatype=XSD.anyURI)))
    if filename.endswith(".csv"): 
        with open(abspath+filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if "Concept" in row and row["Concept"]!="":
                    core=False
                    if "Core Class?" in row and row["Core Class?"]=="Core Ontology":
                        adocdef="==== Class: "+str(row["Concept"])+"\n\n."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
                        adocdef+="|Type\n|http://www.w3.org/2002/07/owl#Class[owl:Class]\n\n"
                        adocdef+="|URI\n|"+str(row["Concept"].replace(coreprefix+":",curns))+"\n\n"
                        core=True
                        gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.Class))
                        prefixtoclasses[coreprefix].append(row["Concept"].replace(coreprefix+":",geocrsNS))
                        classToPrefix[row["Concept"]]={"prefix":coreprefix, "ns":geocrsNS}
                        if "Label" in row and row["Label"]!="":
                            gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                        if "Definition" in row and row["Definition"]!="":
                            gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                            adocdef+="|Definition\n|"+str(row["Definition"])+"\n"
                        if "PROJJSON" in row and row["PROJJSON"]!="":
                            if " " in row["PROJJSON"].strip():
                                for spl in row["PROJJSON"].strip().split(" "):
                                    ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                            else:
                                ldcontext["@context"][row["PROJJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                        if "OGCJSON" in row and row["OGCJSON"]!="":
                            if " " in row["OGCJSON"].strip():
                                for spl in row["OGCJSON"].strip().split(" "):
                                    ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                            else:
                                ldcontext["@context"][row["OGCJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                        if "SuperClass" in row and row["SuperClass"]!="":
                            adocdef+="|Super-classes\n|"
                            if " " in row["SuperClass"]:
                                for spl in row["SuperClass"].split(" "):
                                    gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.subClassOf,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                                    clsuri=row["Concept"].replace(coreprefix+":",geocrsNS)
                                    adocdef+=clsuri+"["+clsuri[clsuri.rfind("/")+1:]+"] "
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.subClassOf,URIRef(row["SuperClass"].replace("geosrs:", getNSForClass(row["SuperClass"],classToPrefix)))))
                                clsuri=spl.replace("geosrs:", getNSForClass(spl,classToPrefix))
                                adocdef+=clsuri+"["+clsuri[clsuri.rfind("/")+1:]+"] "
                            adocdef+="\n\n"
                        if "DisjointClass" in row and row["DisjointClass"]!="":
                            if " " in row["DisjointClass"]:
                                for spl in row["DisjointClass"].split(" "):
                                    gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),OWL.disjointWith,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),OWL.disjointWith,URIRef(row["DisjointClass"].replace("geosrs:", getNSForClass(row["DisjointClass"],classToPrefix)))))
                        moduleToAdoc["06-core.adoc"].append(adocdef+"|===\n\n")
                    else:
                        g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDF.type,OWL.Class))
                        adocdef="==== Class: "+str(row["Concept"])+"\n\n."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
                        adocdef+="|URI\n|"+str(row["Concept"].replace(coreprefix+":",curns))+"[]\n\n"
                        prefixtoclasses[curprefix].append(row["Concept"].replace(curprefix+":",curns).replace("geosrs:","").replace("geoprojection:",""))
                        classToPrefix[row["Concept"]]={"prefix":curprefix, "ns":curns}
                        if "Label" in row and row["Label"]!="":
                            g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDFS.label,Literal(row["Label"],lang="en")))
                        if "Definition" in row and row["Definition"]!="":
                            g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),SKOS.definition,Literal(row["Definition"],lang="en")))
                            adocdef+="|Definition\n|"+str(row["Definition"])+"\n\n"
                        if "PROJJSON" in row and row["PROJJSON"]!="":
                            if " " in row["PROJJSON"].strip():
                                for spl in row["PROJJSON"].strip().split(" "):
                                    ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                            else:
                                ldcontext["@context"][row["PROJJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                        if "OGCJSON" in row and row["OGCJSON"]!="":
                            if " " in row["OGCJSON"].strip():
                                for spl in row["OGCJSON"].strip().split(" "):
                                    ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                            else:
                                ldcontext["@context"][row["OGCJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                        if "SuperClass" in row and row["SuperClass"]!="":
                            adocdef+="|Super-classes\n|"
                            if " " in row["SuperClass"]:
                                for spl in row["SuperClass"].split(" "):
                                    g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDFS.subClassOf,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                                    clsuri=spl.replace("geosrs:", getNSForClass(spl,classToPrefix))
                                    adocdef+=clsuri+"["+clsuri[clsuri.rfind("/")+1:]+"] "
                            else:
                                g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDFS.subClassOf,URIRef(row["SuperClass"].replace("geosrs:", getNSForClass(row["SuperClass"],classToPrefix)))))
                                clsuri=row["Concept"].replace(coreprefix+":",curns)
                                adocdef+=clsuri+"["+clsuri[clsuri.rfind("/")+1:]+"] "
                            adocdef+="\n\n"
                        if "DisjointClass" in row and row["DisjointClass"]!="":
                            if " " in row["DisjointClass"]:
                                for spl in row["DisjointClass"].split(" "):
                                    g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),OWL.disjointWith,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                            else:
                                g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),OWL.disjointWith,URIRef(row["DisjointClass"].replace("geosrs:", getNSForClass(row["DisjointClass"],classToPrefix)))))                      
                        if nsprefix in prefixToModule: 
                            moduleToAdoc[prefixToModule[nsprefix]].append(adocdef+"|===\n\n")

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
    ldcontext["@context"][curprefix]=curns
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
                            adocdef="==== Property: "+str(row["Concept"])+"\n\n."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
                            adocdef+="|URI\n|"+str(row["Concept"].replace(coreprefix+":",curns))+"\n\n"
                            core=True
                            prefixtoproperties["geosrs"].append(row["Concept"].replace(curprefix+":",curns).replace("geosrs:","").replace("geoprojection:",""))
                            if objprop:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.ObjectProperty))
                                adocdef+="|Type\n|http://www.w3.org/2002/07/owl#ObjectProperty[owl:ObjectProperty]\n\n"
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.DatatypeProperty))
                                adocdef+="|Type\n|http://www.w3.org/2002/07/owl#DatatypeProperty[owl:DatatypeProperty]\n\n"
                            if "Label" in row and row["Label"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                            if "Definition" in row and row["Definition"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                                adocdef+="|Definition\n|"+str(row["Definition"])+"\n\n"
                            if "Range" in row and row["Range"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.range,URIRef(row["Range"].replace("geosrs:", getNSForClass(row["Range"],classToPrefix)))))
                                propref=row["Range"].replace("geosrs:", getNSForClass(row["Range"],classToPrefix))
                                adocdef+="|Range\n|"+propref+"["+propref[propref.rfind("/")+1:]+"]\n\n"
                            if "Domain" in row and row["Domain"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.domain,URIRef(row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix)))))
                                propref=row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix))
                                adocdef+="|Domain\n|"+propref+"["+propref[propref.rfind("/")+1:]+"]\n\n"
                            if "PROJJSON" in row and row["PROJJSON"]!="":
                                if objprop:
                                    if " " in row["PROJJSON"].strip():
                                        for spl in row["PROJJSON"].strip().split(" "):
                                            ldcontext["@context"][spl]={"@id":row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":"),"@type":"@vocab","@context":{"@id":row["Concept"].replace("geosrs:","")}}
                                    else:
                                       ldcontext["@context"][row["PROJJSON"]]={"@id":row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":"),"@type":"@vocab","@context":{"@id":row["Concept"].replace("geosrs:","")}}                                                                       
                                else:                                   
                                    if " " in row["PROJJSON"].strip():
                                        for spl in row["PROJJSON"].strip().split(" "):
                                            ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":") 
                                    else:
                                       ldcontext["@context"][row["PROJJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")                                    
                            if "OGCJSON" in row and row["OGCJSON"]!="":
                                if objprop:
                                    if " " in row["OGCJSON"].strip():
                                        for spl in row["OGCJSON"].strip().split(" "):
                                            ldcontext["@context"][spl]={"@id":row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":"),"@type":"@vocab","@context":{"@id":row["Concept"].replace("geosrs:","")}}
                                    else:
                                       ldcontext["@context"][row["OGCJSON"]]={"@id":row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":"),"@type":"@vocab","@context":{"@id":row["Concept"].replace("geosrs:","")}}  
                                else:
                                    if " " in row["OGCJSON"].strip():
                                        for spl in row["OGCJSON"].strip().split(" "):
                                            ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":") 
                                    else:
                                       ldcontext["@context"][row["OGCJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")  
                            moduleToAdoc["06-core.adoc"].append(adocdef+"|===\n\n")
                        else:
                            if row["Core Property?"].lower() in exont:
                                adocdef="==== Property: "+str(row["Concept"])+"\n\n."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
                                adocdef+="|URI\n|"+row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")+"\n\n"
                                if row["Core Property?"]!="":
                                    prefixtoproperties[row["Core Property?"]].append(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/").replace("geosrs:","").replace("geoprojection:",""))
                                if objprop:
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDF.type,OWL.ObjectProperty))
                                    adocdef+="|Type\n|http://www.w3.org/2002/07/owl#ObjectProperty[owl:ObjectProperty]\n\n"
                                else:
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDF.type,OWL.DatatypeProperty))
                                    adocdef+="|Type\n|http://www.w3.org/2002/07/owl#DatatypeProperty[owl:DatatypeProperty]\n\n"
                                if "Label" in row and row["Label"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDFS.label,Literal(row["Label"],lang="en")))
                                if "Definition" in row and row["Definition"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),SKOS.definition,Literal(row["Definition"],lang="en")))
                                    adocdef+="|Definition\n|"+str(row["Definition"])+"\n\n"
                                if "Range" in row and row["Range"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDFS.range,URIRef(row["Range"].replace("geosrs:",getNSForClass(row["Range"],classToPrefix)))))
                                    propref=row["Range"].replace("geosrs:", getNSForClass(row["Range"],classToPrefix))
                                    adocdef+="|Range\n|"+propref+"["+propref[propref.rfind("/")+1:]+"]\n\n"
                                if "Domain" in row and row["Domain"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDFS.domain,URIRef(row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix)))))
                                    propref=row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix))
                                    adocdef+="|Domain\n|"+propref+"["+propref[propref.rfind("/")+1:]+"]\n\n"
                                if "PROJJSON" in row and row["PROJJSON"]!="":
                                    if objprop:
                                        if " " in row["PROJJSON"].strip():
                                            for spl in row["PROJJSON"].strip().split(" "):
                                                ldcontext["@context"][spl]={"@id":row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":"),"@type":"@vocab","@context":{"@id":row["Concept"].replace("geosrs:","")}}
                                        else:
                                           ldcontext["@context"][row["PROJJSON"]]={"@id":row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":"),"@type":"@vocab","@context":{"@id":row["Concept"].replace("geosrs:","")}}                                                                       
                                    else:                                   
                                        if " " in row["PROJJSON"].strip():
                                            for spl in row["PROJJSON"].strip().split(" "):
                                                ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":") 
                                        else:
                                           ldcontext["@context"][row["PROJJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")                                    
                                if "OGCJSON" in row and row["OGCJSON"]!="":
                                    if objprop:
                                        if " " in row["OGCJSON"].strip():
                                            for spl in row["OGCJSON"].strip().split(" "):
                                                ldcontext["@context"][spl]={"@id":row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":"),"@type":"@vocab","@context":{"@id":row["Concept"].replace("geosrs:","")}}
                                        else:
                                           ldcontext["@context"][row["OGCJSON"]]={"@id":row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":"),"@type":"@vocab","@context":{"@id":row["Concept"].replace("geosrs:","")}}   
                                    else:
                                        if " " in row["OGCJSON"].strip():
                                            for spl in row["OGCJSON"].strip().split(" "):
                                                ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":") 
                                        else:
                                           ldcontext["@context"][row["OGCJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")  
                                if row["Core Property?"].lower() in prefixToModule: 
                                    moduleToAdoc[prefixToModule[row["Core Property?"].lower()]].append(adocdef+"|===\n\n")
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
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.NamedIndividual))
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.NamedIndividual))
                            if "Label" in row and row["Label"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                            if "Definition" in row and row["Definition"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                            if "PROJJSON" in row and row["PROJJSON"]!="":
                                if " " in row["PROJJSON"].strip():
                                    for spl in row["PROJJSON"].strip().split(" "):
                                        ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                                else:
                                    ldcontext["@context"][row["PROJJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                            if "OGCJSON" in row and row["OGCJSON"]!="":
                                if " " in row["OGCJSON"].strip():
                                    for spl in row["OGCJSON"].strip().split(" "):
                                        ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                                else:
                                    ldcontext["@context"][row["OGCJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                        else:
                            if row["Module"].lower() in exont:
                                if row["Module"]!="":
                                    prefixtoproperties[row["Module"]].append(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/").replace("geosrs:","").replace("geoprojection:",""))
                                if "Type" in row and row["Type"]!="":
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDF.type,URIRef(row["Type"].replace("geosrs:",getNSForClass(row["Type"],classToPrefix)))))
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDF.type,OWL.NamedIndividual))
                                else:
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDF.type,OWL.NamedIndividual))
                                if "Label" in row and row["Label"]!="":
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDFS.label,Literal(row["Label"],lang="en")))
                                if "Definition" in row and row["Definition"]!="":
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),SKOS.definition,Literal(row["Definition"],lang="en")))
                                if "PROJJSON" in row and row["PROJJSON"]!="":
                                    if " " in row["PROJJSON"].strip():
                                        for spl in row["PROJJSON"].strip().split(" "):
                                            ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                                    else:
                                        ldcontext["@context"][row["PROJJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                                if "OGCJSON" in row and row["OGCJSON"]!="":
                                    if " " in row["OGCJSON"].strip():
                                        for spl in row["OGCJSON"].strip().split(" "):
                                            ldcontext["@context"][spl]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
                                    else:
                                        ldcontext["@context"][row["OGCJSON"]]=row["Concept"].replace("geosrs:", getPrefixForClass(row["Concept"],classToPrefix)+":")
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
alignmentadoc={"ign":[],"iso19111":[],"ifc":[]}
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
                    csourceuri=row["Concept source"].replace("geosrs:",geocrsNS).replace("ign:","http://data.ign.fr/def/ignf#").replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#").replace("ifc:","https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2_TC1/OWL/")
                    ctargeturi=row["Concept target"].replace("geosrs:",geocrsNS).replace("ign:","http://data.ign.fr/def/ignf#").replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#").replace("ifc:","https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2_TC1/OWL/")
                    cpropuri=row["Property"].replace("owl:","http://www.w3.org/2002/07/owl#").replace("rdfs:","http://www.w3.org/2000/01/rdf-schema#")
                    targetprefix=row["Concept target"][0:row["Concept target"].rfind(":")]
                    g.add((URIRef(csourceuri),
                           URIRef(cpropuri),
                           URIRef(ctargeturi)))
                    if targetprefix in alignmentadoc:
                        comment=row["Comment"]
                        if comment==None:
                            comment=" "
                        alignmentadoc[targetprefix].append("|"+str(csourceuri)+"["+row["Concept source"]+"]\n|"+str(cpropuri)+"["+row["Property"]+"]\n|"+str(ctargeturi)+"["+row["Concept source"]+"]\n|"+row["Comment"]+"\n\n")
    else:
        continue

alignments=""
for prefix in alignmentadoc:
    alignments+="=== "+str(prefix).upper()+" Ontology\n\n.Alignment: "+str(prefix).upper()+" Ontology\n[%autowidth]\n|===\n| From Element | Mapping relation | To Element | Notes\n\n"
    for aligns in alignmentadoc[prefix]:
        alignments+=aligns
    alignments+="|===\n\n"

with open("spec/sections/aa-alignments.adoc", 'r',encoding="utf-8") as f:
    alignmentdoc=f.read()

with open("spec/sections/aa-alignments.adoc", 'w',encoding="utf-8") as f:
    f.write(alignmentdoc[0:alignmentdoc.find("=== IGN CRS Ontology")]+alignments)

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

print(moduleToAdoc)

for ad in moduleToAdoc:
    with open("spec/sections/"+ad.replace(".adoc","_classes.adoc"), 'w',encoding="utf-8") as f:
        for part in moduleToAdoc[ad]:
            f.write(part)
doc=""
with open("spec/document.adoc", 'r',encoding="utf-8") as f:
    doc=f.read()

for ad in moduleToAdoc:
    doc=doc.replace("include::sections/"+str(ad)+"[]","include::sections/"+str(ad)+"[]\n\ninclude::sections/"+str(ad.replace(".adoc","_classes.adoc"))+"[]\n")
with open("spec/document.adoc", 'w',encoding="utf-8") as f:
    f.write(doc)

