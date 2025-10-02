from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, RDFS, OWL, SKOS, VANN, XSD
import csv
import os
import re
import json

pattern = re.compile(r'(?<!^)(?=[A-Z])')

opentag="{{"
closetag="}}"

reqns="https://opengeospatial.github.io/ontology-crs/"

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

requirementsttl=Graph()

ctesttemplate="""
[abstract_test,identifier="{{testid}}",conformance-class="{{confclass}}"]
====
[%metadata]
target:: {{target}}
test-purpose:: Check conformance with this requirement
test-method:: Verify that queries involving {{entities}} return the correct result on a test dataset.
test-method-type:: Capabilities
reference:: {{entities}}
====
"""

with open('examples.json', 'r') as file:
    examples = json.load(file)

alignmentadoc={"ign":{},"iso19111":{},"ifc":{}}
moduleToRequirements={"06-core.adoc":{},"07-co_module.adoc":{},"08-cs_module.adoc":{},"09-datum_module.adoc":{},"10-srsapplication_module.adoc":{},"11-projections_module.adoc":{},"12-planet_module.adoc":{},"13-instances.adoc":{}}

prefixtoclasses={"geosrs":[]}
requirementsToClasses={}
prefixtoproperties={"geosrs":[],"SRS":[],"CS":[],"CO":[],"DATUM":[],"projection":[]}
classToPrefix={}
prefixToModule={"srs":"06-core.adoc","core":"06-core.adoc","co":"07-co_module.adoc","cs":"08-cs_module.adoc","datum":"09-datum_module.adoc","application":"10-srsapplication_module.adoc","srsapplication":"10-srsapplication_module.adoc","projection":"11-projections_module.adoc","planet":"12-planet_module.adoc","instances":"13-instances.adoc"}
moduleToAdoc={"06-core.adoc":{},"07-co_module.adoc":{},"08-cs_module.adoc":{},"09-datum_module.adoc":{},"10-srsapplication_module.adoc":{},"11-projections_module.adoc":{},"12-planet_module.adoc":{},"13-instances.adoc":{}}

galigns=Graph() 
galigns.bind("ign","http://data.ign.fr/def/ignf#")  
galigns.bind("ifc","https://standards.buildingsmart.org/IFC/DEV/IFC4/ADD2_TC1/OWL/")  
galigns.bind("iso19111","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#")   
galigns.bind("geosrs", "https://w3id.org/geosrs/")  
galigns.add((URIRef("https://w3id.org/geosrs/alignments/"),RDF.type,OWL.Ontology))
galigns.add((URIRef("https://w3id.org/geosrs/alignments/"),RDFS.label,Literal("SRS Ontology Alignments",lang="en")))

gcore = Graph()
gcore.bind("geosrs", "https://w3id.org/geosrs/") 
gcore.bind("skos","http://www.w3.org/2004/02/skos/core#")

gcore.add((URIRef("https://w3id.org/geosrs"),RDF.type,OWL.Ontology))
gcore.add((URIRef("https://w3id.org/geosrs"),RDFS.label,Literal("SRS Ontology",lang="en")))
gcore.add((URIRef("https://w3id.org/geosrs"),VANN.preferredNamespacePrefix,Literal("geosrs",datatype=XSD.string)))
gcore.add((URIRef("https://w3id.org/geosrs"),VANN.preferredNamespaceUri,Literal("https://w3id.org/geosrs/",datatype=XSD.anyURI)))

geocrsNS="https://w3id.org/geosrs/"
coreprefix="geosrs"

def convertCSVToSHACLAndADoc():
    adocdef=""
    shaclres=Graph()
    shaclres.bind("geosrs", "https://w3id.org/geosrs/") 
    shaclres.bind("sh","http://www.w3.org/ns/shacl#")
    shaclres.bind("rdf","<http://www.w3.org/1999/02/22-rdf-syntax-ns#")

    dirname = os.path.dirname(__file__)
    abspath = os.path.join(dirname, '../csv/shacl/')

    directory = os.fsencode(abspath)

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        shapecounter=1
        if filename.endswith(".csv"):
            with open(abspath+filename, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                adocdef+="===== SHACL Shapes: "+str(filename).replace(".csv","").capitalize()+"\n\n"
                adocdef+="."+str(filename).replace(".csv","").capitalize()+"\n[cols=\"7*\"]\n|===\n"
                adocdef+="|Label|TargetNode|Property|Class|MinCount|MaxCount|Comment\n\n"
                for row in reader:
                    if "Concept" in row and row["Concept"]!="":
                        shapeuri=row["Concept"].replace("geosrs:","https://w3id.org/geosrs/")+"Shape"
                        shapepropuri=row["Concept"].replace("geosrs:","https://w3id.org/geosrs/")+"Shape_Property"
                        shaclres.add((URIRef(shapeuri),URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),URIRef("http://www.w3.org/ns/shacl#NodeShape")))
                        shaclres.add((URIRef(shapeuri),URIRef("http://www.w3.org/2000/01/rdf-schema#label"),Literal("CRS Ontology Shape S"+str(shapecounter),lang="en")))
                        shaclres.add((URIRef(shapeuri),URIRef("http://www.w3.org/ns/shacl#targetNode"),URIRef(row["Concept"].replace("geosrs:","https://w3id.org/geosrs/"))))
                        shaclres.add((URIRef(shapeuri),URIRef("http://www.w3.org/ns/shacl#property"),URIRef(shapepropuri)))
                        adocdef+="|Shape S"+str(shapecounter)+" "
                        adocdef+="|"+str(row["Concept"])+" "
                        adocdef+="|"+str(row["Property"])+" "
                        if "Class" in row and row["Class"]!="":
                            adocdef+="|"+str(row["Class"])+" "
                            shaclres.add((URIRef(shapepropuri),URIRef("http://www.w3.org/ns/shacl#class"),URIRef(str(row["Class"]).replace("geosrs:","https://w3id.org/geosrs/"))))
                        else:
                            adocdef+="| - "
                        if "MinCount" in row and row["MinCount"]!="":
                            adocdef+="|"+str(row["MinCount"])+" "
                            shaclres.add((URIRef(shapepropuri),URIRef("http://www.w3.org/ns/shacl#minCount"),Literal(int(str(row["MinCount"])),datatype=XSD.integer)))
                        else:
                            adocdef+="| - "
                        if "MaxCount" in row and row["MaxCount"]!="":
                            adocdef+="|"+str(row["MaxCount"])+" "
                            shaclres.add((URIRef(shapepropuri),URIRef("http://www.w3.org/ns/shacl#maxCount"),Literal(int(str(row["MaxCount"])),datatype=XSD.integer)))
                        else:
                            adocdef+="| - "
                        if "Comment" in row and row["Comment"]!="":
                            adocdef+="|"+str(row["Comment"])+" "
                            shaclres.add((URIRef(shapepropuri),URIRef("http://www.w3.org/ns/shacl#message"),Literal(str(row["Comment"]),lang="en")))
                        else:
                            adocdef+="| - "
                        adocdef+="\n\n"
                    shapecounter+=1
                adocdef+="|===\n\n"
    with open("spec/sections/ac-shacl_shapes.adoc", 'r',encoding="utf-8") as f:
        ashaclshapes=f.read()
    with open("spec/sections/ac-shacl_shapes.adoc", 'w',encoding="utf-8") as f:
        f.write(ashaclshapes)
        f.write(adocdef)
    
    shaclres.serialize("rules.ttl",format="ttl")


def generateAlignments():
    alignments=""
    for prefix in alignmentadoc:
        alignments+="=== "+str(prefix).upper()+" Ontology\n\n.Alignment: "+str(prefix).upper()+" Ontology\n[%autowidth]\n|===\n| From Element | Mapping relation | To Element | Notes\n\n"
        prefixdict=alignmentadoc[prefix]
        for aligns in sorted(prefixdict.keys()):
            alignments+=prefixdict[aligns]
        alignments+="|===\n\n"

    with open("spec/sections/ab-alignments.adoc", 'r',encoding="utf-8") as f:
        alignmentdoc=f.read()

    with open("spec/sections/ab-alignments.adoc", 'w',encoding="utf-8") as f:
        f.write(alignmentdoc[0:alignmentdoc.find("=== IGN CRS Ontology")]+alignments)

    galigns.serialize(destination="alignments.ttl")

    for pref in prefixtoclasses:
        if pref!="geosrs_srs":
            ldcontext["@context"][pref]=geocrsNS[:-1]+"/"+pref.replace("geosrs_","")+"/"
        for cls in prefixtoclasses[pref]:
            ldcontext["@context"][cls[cls.rfind('/')+1:]]=pref.replace("geosrs_srs","geosrs")+":"+cls[cls.rfind('/')+1:]
        if pref in prefixtoproperties:
            for cls in prefixtoproperties[pref]:
                ldcontext["@context"][convertCamelToSnake(cls[cls.rfind('/')+1:])]=pref.replace("geosrs_srs","geosrs")+":"+cls[cls.rfind('/')+1:]
    #print(prefixtoproperties)
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


def convertCamelToSnake(strr):
 return pattern.sub('_', strr).lower()

def formatListAsLinks(thelist,classOrProperty):
    reslist=""
    for item in thelist:
        if classOrProperty:
            reslist+="<<Class: "+str(item)+",`"+str(item)+"`>> "
        else:
            reslist+="<<Property: "+str(item)+",`"+str(item)+"`>> "
    return reslist

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
abspath = os.path.join(dirname, '../csv/reqToDescription.csv')

reqToDesc={}
with open(abspath, mode ='r')as file:
  csvFile = csv.reader(file)
  for lines in csvFile:
    reqToDesc[lines[0]]=lines[1]

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
                        adocdef="===== Class: "+str(row["Concept"])+"\n\n"
                        if "Description" in row and row["Description"]!="":
                            adocdef+=row["Description"]+"\n\n"
                        adocdef+="."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
                        adocdef+="|Type\n|http://www.w3.org/2002/07/owl#Class[owl:Class]\n\n"
                        adocdef+="|URI\n|"+str(row["Concept"].replace(coreprefix+":",curns))+"\n\n"
                        core=True
                        gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.Class))
                        prefixtoclasses[coreprefix].append(row["Concept"].replace(coreprefix+":",geocrsNS))
                        classToPrefix[row["Concept"]]={"prefix":coreprefix, "ns":geocrsNS}
                        if "Label" in row and row["Label"]!="":
                            gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                        if "Requirement" in row and row["Requirement"]!="":
                            if row["Requirement"] not in moduleToRequirements[prefixToModule[nsprefix]]:
                                moduleToRequirements[prefixToModule[nsprefix]][row["Requirement"]]=[]
                            moduleToRequirements[prefixToModule[nsprefix]][row["Requirement"]].append(row["Concept"])
                        if "Definition" in row and row["Definition"]!="":
                            gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                            adocdef+="|Definition\n|"+str(row["Definition"])+"\n"
                        if "ISO 2019" in row and row["ISO 2019"]!="":
                            alignmentadoc["iso19111"][row["Concept"].replace(coreprefix+":",curns)]="|"+str(row["Concept"].replace(coreprefix+":",curns))+"["+row["Concept"]+"]\n|http://www.w3.org/2002/07/owl#equivalentClass[owl:equivalentClass]\n|"+str(row["ISO 2019"].replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#"))+"["+row["ISO 2019"]+"]\n| - \n\n"
                            galigns.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),URIRef("http://www.w3.org/2002/07/owl#equivalentClass"),URIRef(str(row["ISO 2019"].replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#")))))
                        if "IGN 2019" in row and row["IGN 2019"]!="":
                            alignmentadoc["ign"][row["Concept"].replace(coreprefix+":",curns)]="|"+str(row["Concept"].replace(coreprefix+":",curns))+"["+row["Concept"]+"]\n|http://www.w3.org/2002/07/owl#equivalentClass[owl:equivalentClass]\n|"+str(row["IGN 2019"].replace("ign:","http://data.ign.fr/def/ignf#"))+"["+row["IGN 2019"]+"]\n| - \n\n"
                            galigns.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),URIRef("http://www.w3.org/2002/07/owl#equivalentClass"),URIRef(str(row["IGN 2019"].replace("ign:","http://data.ign.fr/def/ignf#")))))
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
                                    clsuri=spl.replace("geosrs:", getNSForClass(spl,classToPrefix))
                                    adocdef+=clsuri+"["+clsuri[clsuri.rfind("/")+1:]+"] "
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.subClassOf,URIRef(row["SuperClass"].replace("geosrs:", getNSForClass(row["SuperClass"],classToPrefix)))))
                                clsuri=row["SuperClass"].replace("geosrs:", getNSForClass(row["SuperClass"],classToPrefix))
                                adocdef+=clsuri+"["+clsuri[clsuri.rfind("/")+1:]+"] "
                            adocdef+="\n\n"
                        if row["Concept"] in examples:
                            adocdef+="|Example\n|"+examples[row["Concept"]]+"["+row["Concept"]+",window=_blank]\n\n"
                        if "DisjointClass" in row and row["DisjointClass"]!="":
                            if " " in row["DisjointClass"]:
                                for spl in row["DisjointClass"].split(" "):
                                    gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),OWL.disjointWith,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),OWL.disjointWith,URIRef(row["DisjointClass"].replace("geosrs:", getNSForClass(row["DisjointClass"],classToPrefix)))))
                        moduleToAdoc["06-core.adoc"][row["Concept"].replace(coreprefix+":",geocrsNS)]=adocdef+"|===\n\n"
                    else:
                        g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDF.type,OWL.Class))
                        adocdef="===== Class: "+str(row["Concept"])+"\n\n"
                        if "Description" in row and row["Description"]!="":
                            adocdef+=row["Description"]+"\n\n"
                        adocdef+="."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
                        adocdef+="|URI\n|"+str(row["Concept"].replace(coreprefix+":",curns))+"[]\n\n"
                        prefixtoclasses[curprefix].append(row["Concept"].replace(curprefix+":",curns).replace("geosrs:","").replace("geoprojection:",""))
                        classToPrefix[row["Concept"]]={"prefix":curprefix, "ns":curns}
                        if "Requirement" in row and row["Requirement"]!="":
                            if row["Requirement"] not in moduleToRequirements[prefixToModule[nsprefix]]:
                                moduleToRequirements[prefixToModule[nsprefix]][row["Requirement"]]=[]
                            moduleToRequirements[prefixToModule[nsprefix]][row["Requirement"]].append(row["Concept"])
                        if "Label" in row and row["Label"]!="":
                            g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),RDFS.label,Literal(row["Label"],lang="en")))
                        if "Definition" in row and row["Definition"]!="":
                            g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),SKOS.definition,Literal(row["Definition"],lang="en")))
                            adocdef+="|Definition\n|"+str(row["Definition"])+"\n\n"
                        if "ISO 2019" in row and row["ISO 2019"]!="":
                            alignmentadoc["iso19111"][row["Concept"].replace(coreprefix+":",curns)]="|"+str(row["Concept"].replace(coreprefix+":",curns))+"["+row["Concept"]+"]\n|http://www.w3.org/2002/07/owl#equivalentClass[owl:equivalentClass]\n|"+str(row["ISO 2019"].replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#"))+"["+row["ISO 2019"]+"]\n| - \n\n"
                            galigns.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),URIRef("http://www.w3.org/2002/07/owl#equivalentClass"),URIRef(str(row["ISO 2019"].replace("iso19111:","http://def.isotc211.org/iso19112/2019/SpatialReferencingByGeographicIdentifier#")))))
                        if "IGN 2019" in row and row["IGN 2019"]!="":
                            alignmentadoc["ign"][row["Concept"].replace(coreprefix+":",curns)]="|"+str(row["Concept"].replace(coreprefix+":",curns))+"["+row["Concept"]+"]\n|http://www.w3.org/2002/07/owl#equivalentClass[owl:equivalentClass]\n|"+str(row["IGN 2019"].replace("ign:","http://data.ign.fr/def/ignf#"))+"["+row["IGN 2019"]+"]\n| - \n\n"
                            galigns.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),URIRef("http://www.w3.org/2002/07/owl#equivalentClass"),URIRef(str(row["IGN 2019"].replace("ign:","http://data.ign.fr/def/ignf#")))))
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
                                clsuri=row["SuperClass"].replace("geosrs:", getNSForClass(row["SuperClass"],classToPrefix))
                                adocdef+=clsuri+"["+clsuri[clsuri.rfind("/")+1:]+"] "
                            adocdef+="\n\n"
                        if row["Concept"] in examples:
                            adocdef+="|Example\n|"+examples[row["Concept"]]+"["+row["Concept"]+",window=_blank]\n\n"
                        if "DisjointClass" in row and row["DisjointClass"]!="":
                            if " " in row["DisjointClass"]:
                                for spl in row["DisjointClass"].split(" "):
                                    g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),OWL.disjointWith,URIRef(spl.replace("geosrs:", getNSForClass(spl,classToPrefix)))))
                            else:
                                g.add((URIRef(row["Concept"].replace(coreprefix+":",curns)),OWL.disjointWith,URIRef(row["DisjointClass"].replace("geosrs:", getNSForClass(row["DisjointClass"],classToPrefix)))))                      
                        if nsprefix in prefixToModule: 
                            moduleToAdoc[prefixToModule[nsprefix]][row["Concept"].replace(curprefix+":",curns).replace("geosrs:","").replace("geoprojection:","")]=adocdef+"|===\n\n"

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
                #print(row)
                if "Concept" in row and row["Concept"]!="":
                    if "Core Property?" in row:
                        if row["Core Property?"]=="Core Ontology" or row["Core Property?"]=="SRS":
                            adocdef="===== Property: "+str(row["Concept"])+"\n\n"
                            if "Description" in row and row["Description"]!="":
                                adocdef+=row["Description"]+"\n\n"
                            adocdef+="."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
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
                            if "Requirement" in row and row["Requirement"]!="" and str(row["Core Property?"]).lower() in prefixToModule:
                                if row["Requirement"] not in moduleToRequirements[prefixToModule[nsprefix]] :
                                    moduleToRequirements[prefixToModule[str(row["Core Property?"]).lower()]][row["Requirement"]]=[]
                                moduleToRequirements[prefixToModule[str(row["Core Property?"]).lower()]][row["Requirement"]].append(row["Concept"])
                            if "Definition" in row and row["Definition"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                                adocdef+="|Definition\n|"+str(row["Definition"])+"\n\n"
                            if "Range" in row and row["Range"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.range,URIRef(row["Range"].replace("geosrs:", getNSForClass(row["Range"],classToPrefix)))))
                                propref=row["Range"].replace("geosrs:", getNSForClass(row["Range"],classToPrefix))
                                adocdef+="|Range\n|"+propref.replace("xsd:","http://www.w3.org/2001/XMLSchema#")+"["+propref[propref.rfind("/")+1:]+"]\n\n"
                            if "Domain" in row and row["Domain"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.domain,URIRef(row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix)))))
                                propref=row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix))
                                adocdef+="|Domain\n|"+propref+"["+propref[propref.rfind("/")+1:]+"]\n\n"
                            if row["Concept"] in examples:
                                adocdef+="|Example\n|"+examples[row["Concept"]]+"["+row["Concept"]+",window=_blank]\n\n"
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
                            moduleToAdoc["06-core.adoc"][row["Concept"].replace(coreprefix+":","")]=adocdef+"|===\n\n"
                        else:
                            if row["Core Property?"].lower() in exont:
                                adocdef="===== Property: "+str(row["Concept"])+"\n\n"
                                if "Description" in row and row["Description"]!="":
                                    adocdef+=row["Description"]+"\n\n"
                                adocdef+="."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
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
                                if "Requirement" in row and row["Requirement"]!="" and str(row["Core Property?"]).lower() in prefixToModule:
                                    if row["Requirement"] not in moduleToRequirements[prefixToModule[str(row["Core Property?"]).lower()]]:
                                        moduleToRequirements[prefixToModule[str(row["Core Property?"]).lower()]][row["Requirement"]]=[]
                                    moduleToRequirements[prefixToModule[str(row["Core Property?"]).lower()]][row["Requirement"]].append(row["Concept"])
                                if "Definition" in row and row["Definition"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),SKOS.definition,Literal(row["Definition"],lang="en")))
                                    adocdef+="|Definition\n|"+str(row["Definition"])+"\n\n"
                                if "Range" in row and row["Range"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDFS.range,URIRef(row["Range"].replace("geosrs:",getNSForClass(row["Range"],classToPrefix)))))
                                    propref=row["Range"].replace("geosrs:", getNSForClass(row["Range"],classToPrefix))
                                    adocdef+="|Range\n|"+propref.replace("xsd:","http://www.w3.org/2001/XMLSchema#")+"["+propref[propref.rfind("/")+1:]+"]\n\n"
                                if "Domain" in row and row["Domain"]!="":
                                    exont[row["Core Property?"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Core Property?"]).lower()+"/")),RDFS.domain,URIRef(row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix)))))
                                    propref=row["Domain"].replace("geosrs:",getNSForClass(row["Domain"],classToPrefix))
                                    adocdef+="|Domain\n|"+propref+"["+propref[propref.rfind("/")+1:]+"]\n\n"
                                if row["Concept"] in examples:
                                    adocdef+="|Example\n|"+examples[row["Concept"]]+"["+row["Concept"]+",window=_blank]\n\n"
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
                                    moduleToAdoc[prefixToModule[row["Core Property?"].lower()]][row["Concept"].replace("geosrs:", "")]=adocdef+"|===\n\n"
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
                #print(row)
                if "Concept" in row and row["Concept"]!="":
                    if "Module" in row:
                        if row["Module"]=="Core Ontology":
                            adocdef="===== Instance: "+str(row["Concept"])+"\n\n"
                            if "Description" in row and row["Description"]!="":
                                adocdef+=row["Description"]+"\n\n"
                            adocdef+="."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
                            adocdef+="|URI\n|"+str(row["Concept"].replace(coreprefix+":",curns))+"\n\n"
                            core=True
                            prefixtoproperties["geosrs"].append(row["Concept"].replace(coreprefix+":",geocrsNS).replace("geoprojection:",""))
                            if "Type" in row and row["Type"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,URIRef(row["Type"].replace(coreprefix+":",geocrsNS))))
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.NamedIndividual))
                                adocdef+="|Type\n|"+row["Type"].replace(coreprefix+":",geocrsNS)+"["+str(row["Type"])+"]\n\n"
                            else:
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDF.type,OWL.NamedIndividual))
                                adocdef+="|Type\n|http://www.w3.org/2002/07/owl#NamedIndividual[owl:NamedIndividual]\n\n"
                            if "Label" in row and row["Label"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),RDFS.label,Literal(row["Label"],lang="en")))
                            if "Definition" in row and row["Definition"]!="":
                                gcore.add((URIRef(row["Concept"].replace(coreprefix+":",geocrsNS)),SKOS.definition,Literal(row["Definition"],lang="en")))
                                adocdef+="|Definition\n|"+str(row["Definition"])+"\n\n"
                            if "Requirement" in row and row["Requirement"]!="":
                                if row["Requirement"] not in moduleToRequirements[prefixToModule["instances"]]:
                                    moduleToRequirements[prefixToModule["instances"]][row["Requirement"]]=[]
                                moduleToRequirements[prefixToModule["instances"]][row["Requirement"]].append(row["Concept"])
                            if row["Concept"] in examples:
                                    adocdef+="|Example\n|"+examples[row["Concept"]]+"["+row["Concept"]+",window=_blank]\n\n"
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
                            moduleToAdoc["13-instances.adoc"][row["Concept"].replace(coreprefix+":","")]=adocdef+"|===\n\n"
                        else:
                            adocdef="===== Instance: "+str(row["Concept"])+"\n\n"
                            if "Description" in row and row["Description"]!="":
                                adocdef+=row["Description"]+"\n\n"
                            adocdef+="."+str(row["Concept"])+"\n[cols=\"1,1\"]\n|===\n"
                            adocdef+="|URI\n|"+str(row["Concept"].replace(coreprefix+":",curns))+"\n\n"
                            if row["Module"].lower() in exont:
                                if row["Module"]!="":
                                    prefixtoproperties[row["Module"]].append(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/").replace("geosrs:","").replace("geoprojection:",""))
                                if "Type" in row and row["Type"]!="":
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDF.type,URIRef(row["Type"].replace("geosrs:",getNSForClass(row["Type"],classToPrefix)))))
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDF.type,OWL.NamedIndividual))
                                    adocdef+="|Type\n|"+row["Type"].replace(coreprefix+":",geocrsNS)+"["+str(row["Type"])+"]\n\n"
                                else:
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDF.type,OWL.NamedIndividual))
                                    adocdef+="|Type\n|http://www.w3.org/2002/07/owl#NamedIndividual[owl:NamedIndividual]\n\n"
                                if "Label" in row and row["Label"]!="":
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),RDFS.label,Literal(row["Label"],lang="en")))
                                if "Definition" in row and row["Definition"]!="":
                                    exont[row["Module"].lower()].add((URIRef(row["Concept"].replace(coreprefix+":",curns+str(row["Module"]).lower()+"/")),SKOS.definition,Literal(row["Definition"],lang="en")))
                                    adocdef+="|Definition\n|"+str(row["Definition"])+"\n\n"
                                if "Requirement" in row and row["Requirement"]!="":
                                    if row["Requirement"] not in moduleToRequirements[prefixToModule["instances"]]:
                                        moduleToRequirements[prefixToModule["instances"]][row["Requirement"]]=[]
                                    moduleToRequirements[prefixToModule["instances"]][row["Requirement"]].append(row["Concept"])
                                if row["Concept"] in examples:
                                    adocdef+="|Example\n|"+examples[row["Concept"]]+"["+row["Concept"]+",window=_blank]\n\n"
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
                                moduleToAdoc["13-instances.adoc"][row["Concept"].replace(coreprefix+":","")]=adocdef+"|===\n\n"
            g.serialize(destination=filename.replace(".csv","")+".ttl") 
    else:
        continue


print(len(g))
for item in exont:
    exont[item].serialize(destination=item+".ttl") 
gcore.serialize(destination="index.ttl")
       

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../csv/alignment/')
directory = os.fsencode(abspath)
print(abspath)      
#alignmentadoc={"ign":[],"iso19111":[],"ifc":[]}
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
                    galigns.add((URIRef(csourceuri),
                           URIRef(cpropuri),
                           URIRef(ctargeturi)))
                    if targetprefix in alignmentadoc:
                        comment=row["Comment"]
                        if comment==None or str(comment).strip()=="":
                            comment=" - "
                        alignmentadoc[targetprefix][csourceuri]="|"+str(csourceuri)+"["+row["Concept source"]+"]\n|"+str(cpropuri)+"["+row["Property"]+"]\n|"+str(ctargeturi)+"["+row["Concept target"]+"]\n|"+str(comment)+"\n\n"
    else:
        continue

#Generate Conformance Classes

with open("spec/sections/aa-abstract_test_suite.adoc", 'r',encoding="utf-8") as f:
    atestsuitedoc=f.read()

for mod in moduleToRequirements:
    rqid=str(mod)[str(mod).find("-")+1:].replace(".adoc","").replace("_module","")
    requirementsttl.add((URIRef(reqns+str(rqid)),URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),URIRef("http://www.opengis.net/def/spec-element/ConformanceClass")))
    requirementsttl.add((URIRef(reqns+str(rqid)),URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),URIRef("http://www.w3.org/2004/02/skos/core#Collection")))
    atestsuitedoc+="=== Conformance Class: "+str(mod[mod.rfind("-")+1:].replace(".adoc","").replace("_module","")).capitalize()+"\n\n"
    atestsuitedoc+="[conformance_class,identifier=/conf/"+str(rqid)+"]\n"
    atestsuitedoc+="."+str(mod)+"\n\n====\n\n[%metadata]\n\n"
    atestsuitedoc+="target:: /req/"+str(rqid)+"\n\n"
    for req in moduleToRequirements[mod]:
        atestsuitedoc+="abstract-test:: /conf/"+str(rqid)+"/"+str(req).replace(" ","_")+"\n\n"
        requirementsttl.add((URIRef(reqns+mod),URIRef("http://www.w3.org/2004/02/skos/member"),URIRef(reqns+"/conf/"+str(mod)+"/"+str(req).replace(" ","_"))))
    atestsuitedoc+="====\n\n"
    for req in moduleToRequirements[mod]:
        atestsuitedoc+="==== "+str(req)+"\n\n"
        requirementsttl.add((URIRef(reqns+"/req/"+str(rqid)+"/"+str(req).replace(" ","_")),URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),URIRef("http://www.opengis.net/def/spec-element/Requirement")))
        requirementsttl.add((URIRef(reqns+"/req/"+str(rqid)+"/"+str(req).replace(" ","_")),URIRef("http://www.w3.org/2004/02/skos/prefLabel"),Literal(str(req))))
        requirementsttl.add((URIRef(reqns+"/conf/"+str(rqid)+"/"+str(req).replace(" ","_")),URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type"),URIRef("http://www.opengis.net/def/spec-element/ConformanceTest")))
        requirementsttl.add((URIRef(reqns+"/conf/"+str(rqid)+"/"+str(req).replace(" ","_")),URIRef("http://www.opengis.net/def/spec-element/testType"),URIRef("http://www.opengis.net/def/spec-element/Capabilities")))
        requirementsttl.add((URIRef(reqns+"/conf/"+str(rqid)+"/"+str(req).replace(" ","_")),URIRef("http://www.w3.org/2000/01/rdf-schema#seeAlso"),URIRef(reqns+"/req/"+str(rqid)+"/"+str(req).replace(" ","_"))))
        requirementsttl.add((URIRef(reqns+"/conf/"+str(rqid)+"/"+str(req).replace(" ","_")),URIRef("http://www.w3.org/2004/02/skos/prefLabel"),Literal(str(req))))
        requirementsttl.add((URIRef(reqns+"/conf/"+str(rqid)+"/"+str(req).replace(" ","_")),URIRef("http://www.w3.org/2004/02/skos/definition"),Literal("check conformance with this requirement")))
        requirementsttl.add((URIRef(reqns+"/conf/"+str(rqid)+"/"+str(req).replace(" ","_")),URIRef("http://www.w3.org/2004/02/skos/prefLabel"),Literal(str(req))))
        atestsuitedoc+=ctesttemplate.replace("{{entities}}",formatListAsLinks(moduleToRequirements[mod][req],"Propert" not in mod)).replace("{{target}}","/req/"+str(rqid)+"/"+req.replace(" ","_")).replace("{{testid}}","/conf/"+str(rqid)+"/"+req.replace(" ","_")).replace("{{confclass}}","/conf/"+str(rqid))+"\n\n"

with open("spec/sections/aa-abstract_test_suite.adoc", 'w',encoding="utf-8") as f:
    f.write(atestsuitedoc)

requirementsttl.serialize("requirements.ttl",format="ttl")




# Generate alignments
generateAlignments()

convertCSVToSHACLAndADoc()

# Generate modspec elements

for ad in moduleToAdoc:
	content=""
	with open("spec/sections/"+ad,"r") as file:
		content=file.read()
	for tag in re.findall(opentag+"(.+?)"+closetag,content): 
		if tag in moduleToAdoc[ad]:
			content.replace(tag,moduleToAdoc[ad][tag])
	with open("spec/sections/"+ad,"w") as file:
		file.write(content)             
	with open("spec/sections/"+ad.replace(".adoc","_classes.adoc"), 'w',encoding="utf-8") as f:
		print(ad)
		#print(moduleToRequirements[ad])
		reqs=moduleToRequirements[ad]
		#print(reqs)
		if len(reqs)>0:
			rqid=str(ad)[str(ad).find("-")+1:].replace(".adoc","").replace("_module","")
			f.write("[requirements_class,identifier=\"/req/"+str(rqid)+"\",subject=\"Implementation Specification\"]\n."+str(ad)+" Extension\n\n====\n")
			for req in moduleToRequirements[ad]:
				f.write("requirement:: /req/"+str(rqid)+"/"+str(req).replace(" ","_")+"\n")
			f.write("====\n")
			for req in sorted(moduleToRequirements[ad].keys()):
				if "Property" in req or "Properties" in req:
					reqtext="Implementations shall allow the RDFS properties "
					last=None
					for cls in moduleToRequirements[ad][req]:
						reqtext+="<<Property: "+str(cls)+",`"+str(cls)+"`>>, "
						last=cls
				elif "instance" in ad:
					reqtext="Implementations shall allow the RDFS instances "
					last=None
					for cls in moduleToRequirements[ad][req]:
						reqtext+="<<Instance: "+str(cls)+",`"+str(cls)+"`>>, "
						last=cls
				else:
					reqtext="Implementations shall allow the RDFS classes "
					last=None
					for cls in moduleToRequirements[ad][req]:
						reqtext+="<<Class: "+str(cls)+",`"+str(cls)+"`>>, "
						last=cls
				reqtext=reqtext[0:-2]
				if len(moduleToRequirements[ad][req])>0:
					reqtext=reqtext.replace(", <<"+str(last), " and <<"+str(last))
				reqtext+=" to be used in SPARQL graph patterns."
				f.write("==== "+str(req)+"\n\n[requirement,identifier=\"/req/"+str(rqid)+"/"+str(req).replace(" ","_")+"\"]\n\n."+str(req)+"\n====\n"+str(reqtext)+"\n====\n\n")
				print(str(ad)+" - "+str(req))
				print(moduleToRequirements[ad][req])
				if req in reqToDesc:
					f.write(reqToDesc[req]+"\n\n")
				for cls in moduleToRequirements[ad][req]:
					print(str(req)+" - "+str(cls)+" "+cls.replace("geosrs:","")+" "+str(cls.replace("geosrs:","") in moduleToAdoc[ad]))
					if cls.replace("geosrs:","") in moduleToAdoc[ad]:
						f.write(moduleToAdoc[ad][cls.replace("geosrs:","")]) 
doc=""
with open("spec/document.adoc", 'r',encoding="utf-8") as f:
    doc=f.read()

for ad in moduleToAdoc:
    doc=doc.replace("include::sections/"+str(ad)+"[]","include::sections/"+str(ad)+"[]\n\ninclude::sections/"+str(ad.replace(".adoc","_classes.adoc"))+"[]\n")
with open("spec/document.adoc", 'w',encoding="utf-8") as f:
    f.write(doc)
