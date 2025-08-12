import argparse
import os
import re
import json
import pyproj
import csv
from rdflib import Graph
from pyproj import CRS
import urllib.request
from shapely.geometry import box

examples={}
examplefile=open("examples.json","w")
websitens="https://opengeospatial.github.io/ontology-crs/data/def/crs/EPSG/0/"
websitensshort="https://opengeospatial.github.io/ontology-crs/data/ont/crs/"
projectionscoll={}
spheroidscoll={}
crstypescoll={}
scopescoll={}


def csAsSVG(csdef):
    svgstr= """<svg width=\"400\" height=\"250\" viewbox=\"0 0 375 220\"><defs><marker id=\"arrowhead\" markerWidth=\"10\" markerHeight=\"7\" refX=\"0\" refY=\"2\" orient=\"auto\"><polygon points=\"0 0, 4 2, 0 4\" /></marker></defs>"""
    if len(csdef.axis_list)>0:
        if csdef.axis_list[0].unit_name in units:
            svgstr+="""<line x1=\"20\" y1=\"200\" x2=\"200\" y2=\"200\" stroke=\"red\" stroke-width=\"5\" marker-end=\"url(#arrowhead)\"></line><text x=\"110\" y=\"220\" class=\"small\">"""+str(csdef.axis_list[0].abbrev)+": "+str(csdef.axis_list[0].name)+" ("+str(units[csdef.axis_list[0].unit_name])+") ("+str(csdef.axis_list[0].direction)+")</text>"
        else:
            svgstr+="""<line x1=\"20\" y1=\"200\" x2=\"200\" y2=\"200\" stroke=\"red\" stroke-width=\"5\" marker-end=\"url(#arrowhead)\"></line><text x=\"110\" y=\"220\" class=\"small\">"""+str(csdef.axis_list[0].abbrev)+": "+str(csdef.axis_list[0].name)+" ("+str(csdef.axis_list[0].unit_name)+") ("+str(csdef.axis_list[0].direction)+")</text>"      
    if len(csdef.axis_list)>1:
        if csdef.axis_list[1].unit_name in units:
            svgstr+="""<line x1=\"20\" y1=\"200\" x2=\"20\" y2=\"20\" stroke=\"green\" stroke-width=\"5\" marker-end=\"url(#arrowhead)\"></line><text x=\"35\" y=\"20\" class=\"small\">"""+str(csdef.axis_list[1].abbrev)+": "+str(csdef.axis_list[1].name)+" ("+str(units[csdef.axis_list[1].unit_name])+") ("+str(csdef.axis_list[1].direction)+")</text>"
        else:
            svgstr+="""<line x1=\"20\" y1=\"200\" x2=\"20\" y2=\"20\" stroke=\"green\" stroke-width=\"5\" marker-end=\"url(#arrowhead)\"></line><text x=\"35\" y=\"20\" class=\"small\">"""+str(csdef.axis_list[1].abbrev)+": "+str(csdef.axis_list[1].name)+" ("+str(csdef.axis_list[1].unit_name)+") ("+str(csdef.axis_list[1].direction)+")</text>"
    if len(csdef.axis_list)>2: 
        if csdef.axis_list[2].unit_name in units:    
            svgstr+="""<line x1=\"20\" y1=\"200\" x2=\"190\" y2=\"30\" stroke=\"blue\" stroke-width=\"5\" marker-end=\"url(#arrowhead)\"></line><text x=\"210\" y=\"25\" class=\"small\">"""+str(csdef.axis_list[2].abbrev)+": "+str(csdef.axis_list[2].name)+" ("+str(units[csdef.axis_list[2].unit_name])+") ("+str(csdef.axis_list[1].direction)+")</text>"    
        else:
            svgstr+="""<line x1=\"20\" y1=\"200\" x2=\"190\" y2=\"30\" stroke=\"blue\" stroke-width=\"5\" marker-end=\"url(#arrowhead)\"></line><text x=\"210\" y=\"25\" class=\"small\">"""+str(csdef.axis_list[2].abbrev)+": "+str(csdef.axis_list[2].name)+" ("+str(csdef.axis_list[2].unit_name)+") ("+str(csdef.axis_list[1].direction)+")</text>"               
    return svgstr.replace("\"","'")+"</svg>"

    
def csAxisAsSVG(axisdef):
    svgstr= """<svg width=\"400\" height=\"100\" viewbox=\"0 0 275 100\"><defs><marker id=\"arrowhead\" markerWidth=\"10\" markerHeight=\"7\" refX=\"0\" refY=\"2\" orient=\"auto\"><polygon points=\"0 0, 4 2, 0 4\" /></marker></defs>"""
    if axisdef.unit_name in units:
        svgstr+="""<line x1=\"20\" y1=\"50\" x2=\"200\" y2=\"50\" stroke=\"gray\" stroke-width=\"5\" marker-end=\"url(#arrowhead)\"></line><text x=\"30\" y=\"70\" class=\"small\">"""+str(axisdef.abbrev)+": "+str(axisdef.name)+" ("+str(units[axisdef.unit_name])+") ("+str(axisdef.direction)+")</text>"
    else:
        svgstr+="""<line x1=\"20\" y1=\"50\" x2=\"200\" y2=\"50\" stroke=\"gray\" stroke-width=\"5\" marker-end=\"url(#arrowhead)\"></line><text x=\"30\" y=\"70\" class=\"small\">"""+str(axisdef.abbrev)+": "+str(axisdef.name)+" ("+str(axisdef.unit_name)+") ("+str(axisdef.direction)+")</text>"      
    return svgstr.replace("\"","'")+"</svg>"

def geoidAsSVG(a,b):
    svgstr="""<svg viewBox=\"0 0 """+str((a*2)+10)+" "+str((b*2)+10)+"""\" height=\"250\" width=\"400\"><ellipse cx=\""""+str(a)+"""\" cy=\""""+str(b)+"""\" rx=\""""+str(a)+"""\" ry=\""""+str(b)+"""\"/></svg>"""
    return svgstr.replace("\"","'")

def crsToTTL(ttl,curcrs,x,geodcounter,crsclass):
	epsgcode=str(x)
	wkt=curcrs.to_wkt().replace("\"","'").strip()
	crstypescoll[curcrs.type_name]=True
	if crsclass!=None:
		ttl.add("geoepsg:"+epsgcode+" rdf:type "+crsclass+" .\n")
		examples[crsclass]=websitens+"/"+epsgcode
	elif "Projected CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geosrs:ProjectedCRS .\n")
		examples["geosrs:ProjectedCRS"]=websitens+"/"+epsgcode
	elif "Geographic 2D CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geosrs:GeographicCRS .\n")
		examples["geosrs:GeographicCRS"]=websitens+"/"+epsgcode
	elif "Geographic 3D CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geosrs:GeographicCRS .\n")
		examples["geosrs:GeographicCRS"]=websitens+"/"+epsgcode
	elif "Bound CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geosrs:BoundCRS .\n")
		examples["geosrs:BoundCRS"]=websitens+"/"+epsgcode
	elif "Vertical CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geosrs:VerticalCRS .\n")
		examples["geosrs:VerticalCRS"]=websitens+"/"+epsgcode
	elif "Geocentric CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geosrs:GeocentricCRS .\n")
		examples["geosrs:GeocentricCRS"]=websitens+"/"+epsgcode
	elif "Geographic 3D CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geosrs:GeographicCRS .\n")
		examples["geosrs:GeographicCRS"]=websitens+"/"+epsgcode
	elif "Compound CRS" in curcrs.type_name:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geosrs:CompoundCRS .\n")
		examples["geosrs:CompoundCRS"]=websitens+"/"+epsgcode
		for subcrs in curcrs.sub_crs_list:
			ttl.add("geoepsg:"+epsgcode+" geosrs:includesSRS geoepsg:"+str(subcrs.to_epsg())+" .\n")			
	else:
		ttl.add("geoepsg:"+epsgcode+" rdf:type geosrs:CRS .\n")
		examples["geosrs:CRS"]=websitens+"/"+epsgcode
	ttl.add("geoepsg:"+epsgcode+" rdf:type prov:Entity. \n")
	ttl.add("geoepsg:"+epsgcode+" geosrs:isApplicableTo geosrsisbody:Earth .\n")
	ttl.add("geoepsg:"+epsgcode+" rdf:type owl:NamedIndividual .\n")
	ttl.add("geoepsg:"+epsgcode+" rdfs:label \""+curcrs.name.strip()+"\"@en .\n")
	ttl.add("geoepsg:"+epsgcode+" geosrs:isBound \""+str(curcrs.is_bound).lower()+"\"^^xsd:boolean . \n")
	if curcrs.coordinate_system!=None and curcrs.coordinate_system.name in coordinatesystem:
		ttl.add("geoepsg:"+epsgcode+"_cs rdf:type "+coordinatesystem[curcrs.coordinate_system.name]+" . \n")
		ttl.add("geoepsg:"+epsgcode+"_cs geosrs:asSVG \""+str(csAsSVG(curcrs.coordinate_system))+"\"^^geosrs:svgLiteral .\n")
		examples[coordinatesystem[curcrs.coordinate_system.name]]=websitens+"/"+epsgcode+"_cs"	
		if len(curcrs.coordinate_system.axis_list)==2:
			ttl.add("geoepsg:"+epsgcode+"_cs rdf:type geosrs:PlanarCoordinateSystem . \n")
			examples["geosrs:PlanarCoordinateSystem"]=websitens+"/"+epsgcode+"_cs"
		elif len(curcrs.coordinate_system.axis_list)==3:
			ttl.add("geoepsg:"+epsgcode+"_cs rdf:type geosrs:3DCoordinateSystem . \n")	
			examples["geosrs:3DCoordinateSystem"]=websitens+"/"+epsgcode+"_cs"		
		ttl.add("geoepsg:"+epsgcode+"_cs rdfs:label \"EPSG:"+epsgcode+" CS: "+curcrs.coordinate_system.name+"\" . \n")
		if curcrs.coordinate_system.remarks!=None:
			ttl.add("geoepsg:"+epsgcode+"_cs rdfs:comment \""+str(curcrs.coordinate_system.remarks)+"\"@en . \n")
		if curcrs.coordinate_system.scope!=None:
			ttl.add("geoepsg:"+epsgcode+"_cs geosrs:scope \""+str(curcrs.coordinate_system.scope)+"\" . \n")
			examples["geosrs:"+str(curcrs.coordinate_system.scope).replace(" ","")]=websitensshort+"/"+str(curcrs.coordinate_system.scope).replace(" ","")
			scopescoll[curcrs.coordinate_system.scope]=True
		for axis in curcrs.coordinate_system.axis_list:
			axisid=axis.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.unit_name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")+"_"+axis.direction.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_")
			ttl.add("geoepsg:"+epsgcode+"_cs geosrs:axis geosrsaxis:"+axisid+" . \n")
			ttl.add("geosrsaxis:"+axisid+" rdf:type geosrs:CoordinateSystemAxis . \n")
			ttl.add("geocrsaxis:"+axisid+" geosrs:asSVG \""+str(csAxisAsSVG(axis))+"\"^^geosrs:svgLiteral . \n") 
			ttl.add("geosrsaxis:"+axisid+" geosrs:direction geosrs:"+axis.direction+" . \n")
			examples["geosrs:axisDirection"]=websitensshort+"/cs/axis/"+str(axis.direction)
			ttl.add("geosrsaxis:"+axisid+" geosrs:abbreviation \""+str(axis.abbrev).replace("\"","'")+"\"^^xsd:string . \n")				
			ttl.add("geosrsaxis:"+axisid+" geosrs:unit_conversion_factor \""+str(axis.unit_conversion_factor)+"\"^^xsd:double . \n")	
			ttl.add("geosrsaxis:"+axisid+" geosrs:unit_auth_code \""+str(axis.unit_auth_code)+"\"^^xsd:string . \n")
			ttl.add("geosrsaxis:"+axisid+" geosrs:unit_code \""+str(axis.unit_code)+"\"^^xsd:string . \n")					
			ttl.add("geosrsaxis:"+axis.direction+" rdf:type geosrs:AxisDirection . \n")					
			if axis.unit_name in units:
				ttl.add("geosrsaxis:"+axisid+" geosrs:unit "+units[axis.unit_name]+" . \n")
				ttl.add("geosrsaxis:"+axisid+" rdfs:label \""+axis.name+" ("+str(units[axis.unit_name])+")\"@en . \n")						
			else:
				ttl.add("geosrsaxis:"+axisid+" geosrs:unit \""+axis.unit_name+"\" . \n")
				ttl.add("geosrsaxis:"+axisid+" rdfs:label \""+axis.name+" ("+str(axis.unit_name)+")\"@en . \n")	
			examples["geosrs:AxisDirection"]=websitensshort+"/cs/axis/direction/"+axis.direction	
			examples["geosrs:CoordinateSystemAxis"]=websitensshort+"/cs/axis/"+str(axisid)
		ttl.add("geoepsg:"+epsgcode+"_cs geosrs:asWKT \""+str(curcrs.coordinate_system.to_wkt()).replace("\"","'").replace("\n","")+"\" . \n")
		ttl.add("geoepsg:"+epsgcode+"_cs geosrs:asProjJSON \""+str(curcrs.coordinate_system.to_json()).replace("\"","'").replace("\n","")+"\" . \n")
		ttl.add("geoepsg:"+epsgcode+" geosrs:coordinateSystem geoepsg:"+epsgcode+"_cs . \n")
		examples["geosrs:coordinateSystem"]=websitens+"/cs/"+epsgcode+"_cs"	
	elif curcrs.coordinate_system!=None:
		ttl.add("geoepsg:"+epsgcode+" geosrs:coordinateSystem \""+str(curcrs.coordinate_system)+"\"^^xsd:string . \n")
	if curcrs.source_crs!=None:
		ttl.add("geoepsg:"+epsgcode+" geosrs:sourceCRS geoepsg:"+str(curcrs.source_crs.to_epsg())+" . \n")
		examples["geosrs:sourceCRS"]=websitens+"/"+epsgcode	
	if curcrs.target_crs!=None:
		ttl.add("geoepsg:"+epsgcode+" geosrs:targetCRS geoepsg:"+str(curcrs.target_crs.to_epsg())+" . \n")
		examples["geosrs:targetCRS"]=websitens+"/"+epsgcode	
	if curcrs.area_of_use!=None:
		ttl.add("geoepsg:"+epsgcode+" geosrs:area_of_use geoepsg:"+epsgcode+"_area_of_use . \n")
		ttl.add("geoepsg:"+epsgcode+"_area_of_use"+" rdf:type geosrs:AreaOfUse .\n")
		ttl.add("geoepsg:"+epsgcode+"_area_of_use"+" rdfs:label \""+str(curcrs.area_of_use.name).replace("\"","'")+"\"@en .\n")
		b = box(curcrs.area_of_use.west, curcrs.area_of_use.south, curcrs.area_of_use.east, curcrs.area_of_use.north)
		ttl.add("geoepsg:"+epsgcode+"_area_of_use"+" geosrs:extent   \"<http://www.opengis.net/def/crs/OGC/1.3/CRS84> "+str(b.wkt)+"\"^^geo:wktLiteral . \n")
		examples["geosrs:AreaOfUse"]=websitensshort+"/areaofuse/"+epsgcode+"_area_of_use"	
		#\"ENVELOPE("+str(curcrs.area_of_use.west)+" "+str(curcrs.area_of_use.south)+","+str(curcrs.area_of_use.east)+" "+str(curcrs.area_of_use.north)+")\"^^geo:wktLiteral . \n")
	if curcrs.get_geod()!=None:
		geoid="geosrsgeod:"+str(geodcounter)
		if curcrs.datum.ellipsoid!=None:
			if curcrs.datum.ellipsoid.name in spheroids:
				geoid=spheroids[curcrs.datum.ellipsoid.name]
				ttl.add(geoid+" rdf:type geosrs:Ellipsoid . \n")
				ttl.add(geoid+" rdfs:label \""+curcrs.datum.ellipsoid.name+"\"@en . \n")
				ttl.add(geoid+" geosrs:approximates geosrsisbody:Earth . \n")
				examples["geosrs:Ellipsoid"]=websitensshort+"/geod/"+geoid.replace("geosrs:","")
				examples[geoid]=websitensshort+"/geod/"+str(geoid)
			elif curcrs.get_geod().sphere:
				geoid="geosrsgeod:"+str(curcrs.datum.ellipsoid.name).replace(" ","_").replace("(","_").replace(")","_")
				ttl.add(geoid+" rdf:type geosrs:Sphere . \n")
				ttl.add(geoid+" rdfs:label \""+curcrs.datum.ellipsoid.name+"\"@en . \n")
				ttl.add(geoid+" geosrs:approximates geosrsisbody:Earth . \n")
				examples["geosrs:Sphere"]=websitensshort+"/geod/"+geoid.replace("geosrs:","")
				examples[geoid]=websitensshort+"/geod/"+str(geoid)
			else:
				geoid="geosrsgeod:"+str(curcrs.datum.ellipsoid.name).replace(" ","_").replace("(","_").replace(")","_")
				ttl.add(geoid+" rdf:type geosrs:Geoid . \n")
				ttl.add(geoid+" rdfs:label \""+curcrs.datum.ellipsoid.name+"\"@en . \n")
				ttl.add(geoid+" geosrs:approximates geosrsisbody:Earth . \n")
				examples[geoid]=websitensshort+"/geod/"+str(geoid)
		else:
			ttl.add("geoepsg:"+epsgcode+" geosrs:ellipsoid geosrsgeod:"+str(geodcounter)+" . \n")
			ttl.add("geosrsgeod:geod"+str(geodcounter)+" rdf:type geosrs:Geoid . \n")
			ttl.add(geoid+" rdfs:label \"Geoid "+str(geodcounter)+"\"@en . \n")
			ttl.add(geoid+" geosrs:approximates geosrsisbody:Earth . \n")
		ttl.add(geoid+" skos:definition \""+str(curcrs.get_geod().initstring)+"\"^^xsd:string . \n")
		ttl.add(geoid+" geosrs:eccentricity \""+str(curcrs.get_geod().es)+"\"^^xsd:double . \n")
		examples["geosrs:eccentricity"]=websitensshort+"/geod/"+geoid	
		ttl.add(geoid+" geosrs:isSphere \""+str(curcrs.get_geod().sphere)+"\"^^xsd:boolean . \n")
		examples["geosrs:isSphere"]=websitensshort+"/geod/"+geoid	
		if str(curcrs.get_geod().a).isnumeric():
			ttl.add(geoid+" geosrs:semiMajorAxis \""+str(curcrs.get_geod().a)+"\"^^xsd:double . \n")
		else:
			ttl.add(geoid+" geosrs:semiMajorAxis \""+str(curcrs.get_geod().a)+"\"^^xsd:string . \n")
		examples["geosrs:semiMajorAxis"]=websitensshort+"/geod/"+geoid	
		if str(curcrs.get_geod().a).isnumeric():
			ttl.add(geoid+" geosrs:semiMinorAxis \""+str(curcrs.get_geod().b)+"\"^^xsd:double . \n")
		else:
			ttl.add(geoid+" geosrs:semiMinorAxis \""+str(curcrs.get_geod().b)+"\"^^xsd:string . \n")
		examples["geosrs:semiMinorAxis"]=websitensshort+"/geod/"+geoid	
		if curcrs.get_geod().a!=None and curcrs.get_geod().b!=None:
			ttl.add(geoid+" geosrs:asSVG \""+str(geoidAsSVG(curcrs.get_geod().a,curcrs.get_geod().b))+"\" . \n")
		ttl.add(geoid+" geosrs:flatteningParameter \""+str(curcrs.get_geod().f)+"\"^^xsd:double . \n")
		examples["geosrs:flatteningParameter"]=websitensshort+"/geod/"+geoid	
		geodcounter+=1
	if curcrs.coordinate_operation!=None:
		coordoperationid=curcrs.coordinate_operation.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_").replace(",","_").replace("&","and").strip()
		ttl.add("geoepsg:"+epsgcode+" geosrs:coordinateOperation geosrsoperation:"+str(coordoperationid)+" . \n")
		ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:accuracy \""+str(curcrs.coordinate_operation.accuracy)+"\"^^xsd:double . \n")
		ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:method_name \""+str(curcrs.coordinate_operation.method_name)+"\" . \n")
		ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:asProj4 \""+str(curcrs.coordinate_operation.to_proj4()).strip().replace("\"","'").replace("\n","")+"\" . \n")
		ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:asProjJSON \""+str(curcrs.coordinate_operation.to_json()).strip().replace("\"","'").replace("\n","")+"\" . \n")
		ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:asWKT \""+str(curcrs.coordinate_operation.to_wkt()).replace("\"","'").replace("\n","")+"\"^^geo:wktLiteral . \n")
		if curcrs.coordinate_operation.scope!=None:
			ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:scope \""+str(curcrs.coordinate_operation.scope).replace("\"","'")+"\"^^xsd:string . \n")
		if curcrs.coordinate_operation.remarks!=None:
			ttl.add("geosrsoperation:"+str(coordoperationid)+" rdfs:comment \""+str(curcrs.coordinate_operation.remarks).replace("\"","'").replace("\n","")+"\"^^xsd:string . \n")
		ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:has_ballpark_transformation \""+str(curcrs.coordinate_operation.has_ballpark_transformation)+"\"^^xsd:boolean . \n")
		if curcrs.coordinate_operation.area_of_use!=None:
			ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:area_of_use geosrsaou:"+str(coordoperationid)+"_area_of_use . \n")
			ttl.add("geosrsaou:"+str(coordoperationid)+"_area_of_use"+" rdf:type geosrs:AreaOfUse .\n")
			ttl.add("geosrsaou:"+str(coordoperationid)+"_area_of_use"+" rdfs:label \""+str(curcrs.coordinate_operation.area_of_use.name).replace("\"","'")+"\"@en .\n")
			b = box(curcrs.coordinate_operation.area_of_use.west, curcrs.coordinate_operation.area_of_use.south, curcrs.coordinate_operation.area_of_use.east, curcrs.coordinate_operation.area_of_use.north)
			ttl.add("geosrsaou:"+str(coordoperationid)+"_area_of_use geosrs:extent \"<http://www.opengis.net/def/crs/OGC/1.3/CRS84> "+str(b.wkt)+"\"^^geo:wktLiteral . \n")
			examples["geosrs:AreaOfUse"]=websitensshort+"/areaofuse/"+str(coordoperationid)+"_area_of_use"
			#ENVELOPE("+str(curcrs.coordinate_operation.area_of_use.west)+" "+str(curcrs.coordinate_operation.area_of_use.south)+","+str(curcrs.coordinate_operation.area_of_use.east)+" "+str(curcrs.coordinate_operation.area_of_use.north)+")\"^^geosrs:wktLiteral . \n")
		#if curcrs.coordinate_operation.towgs84!=None:
		#	print(curcrs.coordinate_operation.towgs84)
		for par in curcrs.coordinate_operation.params:
			ttl.add(" geosrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" rdf:type owl:DatatypeProperty . \n") 
			ttl.add(" geosrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" rdfs:range xsd:double . \n") 
			ttl.add(" geosrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" rdfs:domain geosrs:CoordinateOperation . \n") 
			ttl.add(" geosrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" rdfs:label \""+str(par.name)+"\"@en . \n")				
			ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:"+str(par.name)[0].lower()+str(par.name).title().replace(" ","")[1:]+" \""+str(par.value)+"\"^^xsd:double . \n") 
		for grid in curcrs.coordinate_operation.grids:
			ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:grid geosrsgrid:"+str(grid.name).replace(" ","_")+" . \n")
			ttl.add("geosrsgrid:"+str(grid.name).replace(" ","_")+" rdf:type geosrs:Grid . \n")
			ttl.add("geosrsgrid:"+str(grid.name).replace(" ","_")+" rdfs:label \""+str(grid.full_name)+"\"@en . \n")
			ttl.add("geosrsgrid:"+str(grid.name).replace(" ","_")+" rdfs:label \""+str(grid.short_name)+"\"@en . \n")
			ttl.add("geosrsgrid:"+str(grid.name).replace(" ","_")+" geosrs:open_license \""+str(grid.open_license)+"\"^^xsd:boolean . \n")
			ttl.add("geosrsgrid:"+str(grid.name).replace(" ","_")+" rdfs:comment \""+str(grid.url)+"\"@en . \n")
		if curcrs.coordinate_operation.operations!=None:
			for operation in curcrs.coordinate_operation.operations:
				ttl.add("geosrsoperation:"+str(coordoperationid)+" geosrs:operation \""+str(operation).replace("\n","").replace("\"","'")+"\"^^xsd:string . \n")
		if curcrs.coordinate_operation.type_name==None:
			ttl.add("geosrsoperation:"+str(coordoperationid)+" rdf:type geosrs:CoordinateOperation . \n")
			examples["geosrs:CoordinateOperation"]=websitensshort+"/co/"+str(coordoperationid)
		elif curcrs.coordinate_operation.type_name=="Conversion":
			found=False
			if curcrs.coordinate_operation.to_proj4()!=None:
				proj4string=curcrs.coordinate_operation.to_proj4().strip().replace("\"","'").replace("\n","")
				for prj in projections:
					projectionscoll[prj]=True
					if prj in proj4string:
						ttl.add("geosrsoperation:"+str(coordoperationid)+" rdf:type "+projections[prj]+" . \n")
						examples[projections[prj]]=websitensshort+"/crs/operation/"+str(coordoperationid)
						found=True
						break
			if not found:
				ttl.add("geosrsoperation:"+str(coordoperationid)+" rdf:type geosrs:CoordinateConversionOperation . \n")
				examples["geosrs:CoordinateConversionOperation"]=websitensshort+"/operation/"+str(coordoperationid)
		elif curcrs.coordinate_operation.type_name=="Transformation":
			ttl.add("geosrsoperation:"+str(coordoperationid)+" rdf:type geosrs:CoordinateTransformationOperation . \n")
			examples["geosrs:CoordinateTransformationOperation"]=websitensshort+"/operation/"+str(coordoperationid)
		elif curcrs.coordinate_operation.type_name=="Concatenated Operation":
			ttl.add("geosrsoperation:"+str(coordoperationid)+" rdf:type geosrs:CoordinateConcatenatedOperation . \n")
			examples["geosrs:CoordinateConcatenatedOperation"]=websitensshort+"/operation/"+str(coordoperationid)
		elif curcrs.coordinate_operation.type_name=="Other Coordinate Operation":
			ttl.add("geosrsoperation:"+str(coordoperationid)+" rdf:type geosrs:OtherCoordinateOperation . \n")
			examples["geosrs:OtherCoordinateOperation"]=websitensshort+"/operation/"+str(coordoperationid)
		ttl.add("geosrsoperation:"+str(coordoperationid)+" rdfs:label \""+curcrs.coordinate_operation.name+": "+curcrs.coordinate_operation.method_name+"\"@en . \n")
	if curcrs.datum!=None:
		datumid=str(curcrs.datum.name.replace(" ","_").replace("(","_").replace(")","_").replace("/","_").replace("'","_").replace("+","_plus").replace("[","_").replace("]","_"))
		ttl.add("geoepsg:"+epsgcode+" geosrs:datum geosrsdatum:"+str(datumid)+" . \n")
		if "Geodetic Reference Frame" in curcrs.datum.type_name:
			ttl.add("geosrsdatum:"+str(datumid)+" rdf:type geosrs:GeodeticReferenceFrame . \n")
			examples["geosrs:GeodeticReferenceFrame"]=websitensshort+"/datum/"+str(datumid)
		elif "Dynamic Vertical Reference Frame" in curcrs.datum.type_name:
			ttl.add("geosrsdatum:"+str(datumid)+" rdf:type geosrs:DynamicVerticalReferenceFrame . \n")
			examples["geosrs:DynamicVerticalDatum"]=websitensshort+"/datum/"+str(datumid)
		elif "Vertical Reference Frame" in curcrs.datum.type_name:
			ttl.add("geosrsdatum:"+str(datumid)+" rdf:type geosrs:VerticalReferenceFrame . \n")
			examples["geosrs:VerticalReferenceFrame"]=websitensshort+"/datum/"+str(datumid)
		else:
			#print(curcrs.datum.type_name)
			ttl.add("geosrsdatum:"+str(datumid)+" rdf:type geosrs:Datum . \n")
			examples["geosrs:Datum"]=websitensshort+"/datum/"+str(datumid)
		ttl.add("geosrsdatum:"+str(datumid)+" rdfs:label \"Datum: "+curcrs.datum.name+"\"@en . \n")
		if curcrs.datum.remarks!=None:
			ttl.add("geosrsdatum:"+str(datumid)+" rdfs:comment \""+str(curcrs.datum.remarks)+"\"@en . \n")
		if curcrs.datum.scope!=None:
			ttl.add("geosrsdatum:"+str(datumid)+" geosrs:scope \""+str(curcrs.datum.scope)+"\"^^xsd:string . \n")
			if "," in curcrs.datum.scope:
				for scp in curcrs.datum.scope.split(","):
					#print("Scope: "+scp)
					if scp.lower().strip().replace(".","") in scope:
						ttl.add("geosrsdatum:"+str(datumid)+" geosrs:usage "+scope[scp.lower().strip().replace(".","")]+" . \n")
						ttl.add(scope[scp.lower().strip().replace(".","")]+" rdfs:subClassOf geosrs:SRSApplication . \n")
						examples[scope[scp.lower().strip().replace(".","")]]=websitensshort+"/datum/"+str(datumid)
					else:
						ttl.add("geosrsdatum:"+str(datumid)+" geosrs:usage \""+str(curcrs.datum.scope)+"\"^^xsd:string . \n")
			#print(str(curcrs.datum.scope))
		if curcrs.datum.ellipsoid!=None and curcrs.datum.ellipsoid.name in spheroids:
			spheroidscoll[curcrs.datum.ellipsoid.name]=True
			spheroidid=spheroids[curcrs.datum.ellipsoid.name]
			ttl.add("geosrsdatum:"+str(datumid)+" geosrs:ellipse "+spheroidid+" . \n")
			ttl.add(spheroidid+" rdfs:label \""+str(curcrs.datum.ellipsoid.name)+"\"@en . \n")
			ttl.add(spheroidid+" rdf:type geosrs:Ellipsoid .\n")	
			ttl.add(spheroidid+" geosrs:inverse_flattening \""+str(curcrs.datum.ellipsoid.inverse_flattening)+"\"^^xsd:double .\n")	
			examples["geosrs:inverseFlattening"]=websitensshort+"/geod/"+str(spheroidid)		
			if curcrs.datum.ellipsoid.remarks!=None:
				ttl.add(spheroidid+" rdfs:comment \""+str(curcrs.datum.ellipsoid.remarks)+"\"^^xsd:string .\n")
			ttl.add(spheroidid+" geosrs:is_semi_minor_computed \""+str(curcrs.datum.ellipsoid.is_semi_minor_computed).lower()+"\"^^xsd:boolean .\n")
			examples["geosrs:Spheroid"]=websitensshort+"/geod/"+str(spheroidid)
			examples[spheroidid.replace("geosrsgeod:","geosrs:")]=websitensshort+"/geod/"+str(spheroidid.replace("geosrsgeod:",""))
		elif curcrs.datum.ellipsoid!=None:	
			ttl.add("geosrsdatum:"+str(datumid)+" geosrs:ellipse \""+curcrs.datum.ellipsoid.name+"\" . \n")
			examples["geosrs:ellipsoid"]=websitensshort+"/datum/"+str(datumid)
			examples["geosrs:"+curcrs.datum.ellipsoid.name]=websitensshort+"/geod/"+str(curcrs.datum.ellipsoid.name)
			spheroidscoll[curcrs.datum.ellipsoid.name]=True
		if curcrs.prime_meridian!=None:
			meridianid=str(curcrs.prime_meridian.name.replace(" ",""))
			ttl.add("geosrsdatum:"+str(datumid)+" geosrs:primeMeridian geosrsmeridian:"+meridianid+" . \n")
			examples["geosrs:primeMeridian"]=websitensshort+"/datum/"+str(datumid)
			ttl.add("geosrsmeridian:"+meridianid+" rdf:type geosrs:PrimeMeridian . \n")
			ttl.add("geosrsmeridian:"+meridianid+" rdfs:label \""+curcrs.prime_meridian.name+"\"@en . \n")
			ttl.add("geosrsmeridian:"+meridianid+" geosrs:longitude \""+str(curcrs.prime_meridian.longitude)+"\"^^xsd:double . \n")
			if curcrs.prime_meridian.unit_name in units:
				ttl.add("geosrsmeridian:"+meridianid+" geosrs:unit om:"+units[curcrs.prime_meridian.unit_name]+" . \n")
				ttl.add(units[curcrs.prime_meridian.unit_name]+" rdf:type om:Unit .\n")	
			else:
				ttl.add("geosrsmeridian:"+meridianid+" geosrs:unit \""+str(curcrs.prime_meridian.unit_name)+"\" . \n")
			if curcrs.prime_meridian.unit_conversion_factor!=None:
				ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" geosrs:unitConversionFactor \""+str(curcrs.prime_meridian.unit_conversion_factor)+"\"^^xsd:double . \n")
			if curcrs.prime_meridian.name in meridiansvg:
				ttl.add("geocrsmeridian:"+curcrs.prime_meridian.name.replace(" ","")+" foaf:image \""+str(meridiansvg[curcrs.prime_meridian.name])+"\"^^xsd:anyURI . \n")
			ttl.add("geosrsmeridian:"+meridianid+" geosrs:asWKT \""+str(curcrs.prime_meridian.to_wkt()).replace("\"","'").replace("\n","")+"\" . \n")
			ttl.add("geosrsmeridian:"+meridianid+" geosrs:asProjJSON \""+str(curcrs.prime_meridian.to_json()).replace("\"","'").replace("\n","")+"\" . \n")
			if curcrs.prime_meridian.remarks!=None:
				ttl.add("geosrsmeridian:"+meridianid+" rdfs:comment \""+str(curcrs.prime_meridian.remarks)+"\"@en . \n")
			if curcrs.prime_meridian.scope!=None:
				ttl.add("geosrsmeridian:"+meridianid+" geosrs:scope \""+str(curcrs.prime_meridian.scope)+"\"^^xsd:string . \n")	
			examples["geosrs:PrimeMeridian"]=websitensshort+"/primeMeridian/"+str(meridianid)			
	ttl.add("geoepsg:"+epsgcode+" geosrs:isVertical \""+str(curcrs.is_vertical).lower()+"\"^^xsd:boolean . \n")
	ttl.add("geoepsg:"+epsgcode+" geosrs:isProjected \""+str(curcrs.is_projected).lower()+"\"^^xsd:boolean . \n")
	ttl.add("geoepsg:"+epsgcode+" geosrs:isGeocentric \""+str(curcrs.is_geocentric).lower()+"\"^^xsd:boolean . \n")
	ttl.add("geoepsg:"+epsgcode+" geosrs:isGeographic \""+str(curcrs.is_geographic).lower()+"\"^^xsd:boolean . \n")
	if curcrs.utm_zone!=None:
		ttl.add("geoepsg:"+epsgcode+" geosrs:utm_zone \""+str(curcrs.utm_zone)+"\"^^xsd:string . \n")	
	try:
		if curcrs.to_proj4()!=None:
			ttl.add("geoepsg:"+epsgcode+" geosrs:asProj4 \""+curcrs.to_proj4().strip().replace("\"","'")+"\"^^geosrs:proj4Literal . \n")
			examples["geosrs:asProj4"]=websitens+"/"+str(epsgcode)	
			examples["geosrs:proj4Literal"]=websitens+"/"+str(epsgcode)
	except:
		print("error")
	if curcrs.to_json()!=None:
		ttl.add("geoepsg:"+epsgcode+" geosrs:asProjJSON \""+curcrs.to_json().strip().replace("\"","'")+"\"^^geosrs:projJSONLiteral . \n")
		examples["geosrs:asProjJSON"]=websitens+"/"+str(epsgcode)	
		examples["geosrs:projJSONLiteral"]=websitens+"/"+str(epsgcode)		
	if wkt!="":
		ttl.add("geoepsg:"+epsgcode+" geosrs:asWKT \""+wkt+"\"^^geosrs:wktLiteral . \n")
		examples["geosrs:asWKT"]=websitens+"/"+str(epsgcode)	
		examples["geosrs:wktLiteral"]=websitens+"/"+str(epsgcode)
	ttl.add("geoepsg:"+epsgcode+" geosrs:epsgCode \"EPSG:"+epsgcode+"\"^^xsd:string . \n")		
	#i+=1


def parseSolarSystemSatellites(filename,ttlstring):
	with open(filename) as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			curname=row["Name"].replace(" ","_").replace("+","_").replace(":","_").replace("(","_").replace(")","_").replace("/","_").replace("*","_").replace("'","_").replace("~","_")
			if curname=="":
				continue
			ttlstring.add("geocrsisbody:"+curname+" rdf:type geosrs:Moon .\n")
			ttlstring.add("geocrsisbody:"+curname+" rdfs:label \""+str(row["Name"])+"\"@en .\n")
			if str(row["radius"])!="":
				ttlstring.add("geocrsisbody:"+curname+" geosrs:radius \""+str(row["radius"])+"\"^^xsd:double .\n")
			if str(row["orbital_period"])!="":
				ttlstring.add("geocrsgeod:"+curname+"_geoid geosrs:orbital_period geocrsgeod:"+curname+"_geoid_obperiod .\n")
				ttlstring.add("geocrsgeod:"+curname+"_geoid_obperiod rdf:value \""+row["orbital_period"]+"\"^^xsd:double .\n")
				ttlstring.add("geocrsgeod:"+curname+"_geoid om:hasUnit om:day .\n")
			ttlstring.add("geocrsisbody:"+curname+" geosrs:planet_status geosrs:Confirmed .\n")
			ttlstring.add("geosrs:Confirmed rdf:type geosrs:PlanetStatus .\n")
			ttlstring.add("geosrs:Confirmed rdfs:label \"Confirmed\"@en .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid rdf:type geosrs:Sphere .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid rdfs:label \"Geoid for "+str(row["Name"])+"\"@en .\n")
			if str(row["semi_major_axis"])!="":
				ttlstring.add("geocrsgeod:"+curname+"_geoid geosrs:semiMajorAxis geocrsgeod:"+curname+"_geoid_smj_axis .\n")
				ttlstring.add("geocrsgeod:"+curname+"_geoid_smj_axis rdf:value  \""+row["semi_major_axis"]+"\"^^xsd:double .\n")
				ttlstring.add("geocrsgeod:"+curname+"_geoid_smj_axis om:hasUnit  om:astronomicalUnit .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid geosrs:isApplicableTo geocrsisbody:"+curname+" .\n")
			if str(row["Parent"])!="":
				starname=row["Parent"].replace(" ","_").replace("+","_").replace(":","_").replace("(","_").replace(")","_").replace("/","_").replace("*","_").replace("'","_")
				if starname!="":
					ttlstring.add("geocrsisbody:"+starname+" rdf:type geosrs:Planet .\n")
					ttlstring.add("geocrsisbody:"+starname+" rdfs:label \""+str(row["Parent"])+"\"@en .\n")	
					ttlstring.add("geocrsisbody:"+curname+" geosrs:satelliteOf geocrsisbody:"+starname+" .\n")					


def parseAdditionalPlanetarySpheroids(filename,ttlstring):
	with open(filename) as csv_file:
		csv_reader = csv.DictReader(csv_file)
		for row in csv_reader:
			curname=row["name"].replace(" ","_").replace("+","_").replace(":","_").replace("(","_").replace(")","_").replace("/","_").replace("*","_").replace("'","_")
			ttlstring.add("geocrsisbody:"+curname+" rdf:type geosrs:Planet .\n")
			ttlstring.add("geocrsisbody:"+curname+" rdfs:label \""+str(row["name"])+"\"@en .\n")
			if str(row["discovered"])!="":
				ttlstring.add("geocrsisbody:"+curname+" dc:date \""+str(row["discovered"])+"\"^^xsd:date .\n")
			if str(row["mass"])!="":
				ttlstring.add("geocrsisbody:"+curname+" geosrs:mass \""+str(row["mass"])+"\"^^xsd:double .\n")
			if str(row["orbital_period"])!="":
				ttlstring.add("geocrsisbody:"+curname+" geosrs:orbital_period \""+str(row["orbital_period"])+"\"^^xsd:double .\n")
			if str(row["radius"])!="":
				ttlstring.add("geocrsisbody:"+curname+" geosrs:radius geocrsisbody:"+curname+"_radius .\n")
				ttlstring.add("geocrsisbody:"+curname+"_radius rdf:value \""+str(row["radius"])+"\"^^xsd:double .\n")
				ttlstring.add("geocrsisbody:"+curname+"_radius om:hasUnit om:astronomicalUnit .\n")
			ttlstring.add("geocrsisbody:"+curname+" geosrs:planet_status geosrs:"+str(row["planet_status"])+" .\n")
			ttlstring.add("geosrs:"+str(row["planet_status"])+" rdf:type geosrs:PlanetStatus .\n")
			ttlstring.add("geosrs:"+str(row["planet_status"])+" rdfs:label \""+row["planet_status"]+"\"@en .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid rdf:type geosrs:Sphere .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid rdfs:label \"Geoid for "+str(row["name"])+"\"@en .\n")
			if str(row["semi_major_axis"])!="":
				ttlstring.add("geocrsgeod:"+curname+"_geoid geosrs:semiMajorAxis geocrsgeod:"+curname+"_geoid_smj_axis .\n")
				ttlstring.add("geocrsgeod:"+curname+"_geoid_smj_axis rdf:value  \""+row["semi_major_axis"]+"\"^^xsd:double .\n")
				ttlstring.add("geocrsgeod:"+curname+"_geoid_smj_axis om:hasUnit  om:astronomicalUnit .\n")
			if str(row["eccentricity"])!="":
				ttlstring.add("geocrsgeod:"+curname+"_geoid geosrs:eccentricity \""+row["eccentricity"]+"\"^^xsd:double .\n")
			ttlstring.add("geocrsgeod:"+curname+"_geoid geosrs:approximates geocrsisbody:"+curname+" .\n")
			if str(row["star_name"])!="":
				starname=row["star_name"].replace(" ","_").replace("+","_").replace(":","_").replace("(","_").replace(")","_").replace("/","_").replace("*","_").replace("'","_")
				ttlstring.add("geocrsisbody:"+starname+" rdf:type geosrs:Star .\n")
				ttlstring.add("geocrsisbody:"+starname+" rdfs:label \""+str(row["star_name"])+"\"@en .\n")
				if str(row["discovered"])!="":
					ttlstring.add("geocrsisbody:"+starname+" dc:date \""+str(row["discovered"])+"\"^^xsd:date .\n")
				if str(row["star_mass"])!="":
					ttlstring.add("geocrsisbody:"+starname+" geosrs:mass \""+row["star_mass"]+"\"^^xsd:double .\n")
				if str(row["star_radius"])!="":
					ttlstring.add("geocrsisbody:"+starname+" geosrs:radius \""+row["star_radius"]+"\"^^xsd:double .\n")
				ttlstring.add("geocrsisbody:"+curname+" geosrs:satelliteOf geocrsisbody:"+starname+" .\n")
				if str(row["star_distance"])!="":
					ttlstring.add("geocrsisbody:"+curname+" geosrs:starDistance \""+str(row["star_distance"])+"\"^^xsd:double .\n")
		return ttlstring


units={}
units["m"]="om:meter"
units["centimetre"]="om:centimetre"
units["fathom"]="om:fathom-USSurvey"
units["chain"]="om:chain"
units["radian"]="om:radian"
units["foot"]="om:foot-International"
units["metre"]="om:metre"
units["nautical mile"]="om:nauticalMile-International"
units["kilometre"]="om:kilometre"
units["grad"]="om:degree"
units["gon"]="om:gon"
units["microradian"]="om:microradian"
units["yard"]="om:yard-International"
units["degree"]="om:degree"
units["Degree"]="om:degree"
units["metre per second"]="om:metrePerSecond-Time"
units["year"]="om:year"
units["ft"]="om:foot-International"
units["US survey foot"]="om:foot-USSurvey"
units["US Survey Foot"]="om:foot-USSurvey"
units["us-ft"]="om:foot-USSurvey"
meridiansvg={
    "Athens":"https://situx.github.io/proj4rdf/primemeridians/AthensPrimeMeridian.svg",
    "Bern":"https://situx.github.io/proj4rdf/primemeridians/BernPrimeMeridian.svg",
    "Bogota":"https://situx.github.io/proj4rdf/primemeridians/BogotaPrimeMeridian.svg",
    "Brussels":"https://situx.github.io/proj4rdf/primemeridians/BrusselsPrimeMeridian.svg",
    "Ferro":"https://situx.github.io/proj4rdf/primemeridians/FerroPrimeMeridian.svg",
    "Greenwich":"https://situx.github.io/proj4rdf/primemeridians/GreenwichPrimeMeridian.svg",
    "Jakarta":"https://situx.github.io/proj4rdf/primemeridians/JakartaPrimeMeridian.svg",
    "Lisbon":"https://situx.github.io/proj4rdf/primemeridians/LisbonPrimeMeridian.svg",
    "Madrid":"https://situx.github.io/proj4rdf/primemeridians/MadridPrimeMeridian.svg",
    "Oslo":"https://situx.github.io/proj4rdf/primemeridians/OsloPrimeMeridian.svg",
    "Paris":"https://situx.github.io/proj4rdf/primemeridians/ParisPrimeMeridian.svg",
    "ParisRGS":"https://situx.github.io/proj4rdf/primemeridians/ParisRGSPrimeMeridian.svg",
    "Rome":"https://situx.github.io/proj4rdf/primemeridians/RomePrimeMeridian.svg",
    "Stockholm":"https://situx.github.io/proj4rdf/primemeridians/StockholmPrimeMeridian.svg"
}
scope={}
scope["geodesy"]="geosrs:Geodesy"
scope["topographic mapping"]="geosrs:TopographicMap"
scope["spatial referencing"]="geosrs:SpatialReferencing"
scope["engineering survey"]="geosrs:EngineeringSurvey"
scope["satellite survey"]="geosrs:SatelliteSurvey"
scope["satellite navigation"]="geosrs:SatelliteNavigation"
scope["coastal hydrography"]="geosrs:CoastalHydrography"
scope["offshore engineering"]="geosrs:OffshoreEngineering"
scope["hydrography"]="geosrs:Hydrography"
scope["mapping"]="geosrs:Mapping"
scope["seismic survey"]="geosrs:SeismicSurvey"
scope["remote sensing"]="geosrs:RemoteSensing"
scope["oceanography"]="geosrs:Oceanography"
scope["forestry"]="geosrs:Forestry"
scope["drilling"]="geosrs:Drilling"
scope["marine navigation"]="geosrs:MarineNavigation"
scope["nautical charting"]="geosrs:NauticalChart"
scope["oil and gas exploration"]="geosrs:OilAndGasExploration"
scope["cadastre"]="geosrs:CadastreMap"
coordinatesystem={}
coordinatesystem["ellipsoidal"]="geosrs:EllipsoidalCoordinateSystem"
coordinatesystem["cartesian"]="geosrs:CartesianCoordinateSystem"
coordinatesystem["vertical"]="geosrs:VerticalCoordinateSystem"
coordinatesystem["ft"]="om:foot"
coordinatesystem["us-ft"]="om:usfoot"
spheroids={}
spheroids["Airy 1830"]="geosrs:Airy1830"
spheroids["Airy Modified 1849"]="geosrs:AiryModified1849"
spheroids["aust_SA"]="geosrs:AustralianNationalSpheroid"
spheroids["Australian National Spheroid"]="geosrs:AustralianNationalSpheroid"
spheroids["Bessel 1841"]="geosrs:Bessel1841"
spheroids["bess_nam"]="geosrs:Bessel1841"
spheroids["bessel"]="geosrs:Bessel1841"
spheroids["Bessel 1841 (Namibia)"]="geosrs:Bessel1841Namibia"
spheroids["Bessel Modified"]="geosrs:BesselModified"
spheroids["CGCS2000"]="geosrs:CGCS2000"
spheroids["Clarke 1866"]="geosrs:Clarke1866"
spheroids["Clarke 1858"]="geosrs:Clarke1858"
spheroids["Clarke 1880"]="geosrs:Clarke1880"
spheroids["Clarke 1880 (Arc)"]="geosrs:Clarke1880ARC"
spheroids["Clarke 1880 (RGS)"]="geosrs:Clarke1880RGS"
spheroids["Clarke 1880 (IGN)"]="geosrs:Clarke1880IGN"
spheroids["clrk"]="geosrs:Clarke1866"
spheroids["clrk66"]="geosrs:Clarke1866"
spheroids["clrk80"]="geosrs:Clarke1880RGS"
spheroids["clrk80ign"]="geosrs:Clarke1880IGN"
spheroids["Danish 1876"]="geosrs:Danish1876"
spheroids["engelis"]="geosrs:Engelis1985"
spheroids["evrst30"]="geosrs:Everest1830"
spheroids["Everest 1830"]="geosrs:Everest1830"
spheroids["Everest (1830 Definition)"]="geosrs:Everest1830"
spheroids["Everest 1830 Modified"]="geosrs:Everest1830Modified"
spheroids["evrst48"]="geosrs:Everest1948"
spheroids["Everest 1948"]="geosrs:Everest1948"
spheroids["evrst56"]="geosrs:Everest1956"
spheroids["Everest 1956"]="geosrs:Everest1956"
spheroids["evrst69"]="geosrs:Everest1869"
spheroids["Everest 1869"]="geosrs:Everest1869"
spheroids["fschr68"]="geosrs:Fischer1968"
spheroids["Fischer 1968"]="geosrs:Fischer1968"
spheroids["GRS80"]="geosrs:GRS1980"
spheroids["GRS 80"]="geosrs:GRS1980"
spheroids["GRS67"]="geosrs:GRS67"
spheroids["GRS 1967"]="geosrs:GRS67"
spheroids["GRS 1967 Modified"]="geosrs:GRS67Modified"
spheroids["GRS 67"]="geosrs:GRS67"
spheroids["GRS1980"]="geosrs:GRS1980"
spheroids["GRS 1980"]="geosrs:GRS1980"
spheroids["GSK-2011"]="geosrs:GSK2011"
spheroids["Helmert 1906"]="geosrs:Helmert1906"
spheroids["Hough 1960"]="geosrs:Hough1960"
spheroids["Hughes 1980"]="geosrs:Hughes1980"
spheroids["IAG 1975"]="geosrs:IAG1975"
spheroids["Indonesian National Spheroid"]="geosrs:IndonesianNationalSpheroid"
spheroids["International 1924"]="geosrs:International1924"
spheroids["intl"]="geosrs:International1924"
spheroids["Krassowsky 1940"]="geosrs:Krassowsky1940"
spheroids["krass"]="geosrs:Krassowsky1940"
spheroids["kaula"]="geosrs:Kaula1961"
spheroids["Kaula 1961"]="geosrs:Kaula1961"
spheroids["lerch"]="geosrs:Lerch1979"
spheroids["Lerch 1979"]="geosrs:Lerch1979"
spheroids["Moon_2000_IAU_IAG"]="geosrs:Moon2000_IAU_IAG"
spheroids["NWL 9D"]="geosrs:NWL9D"
spheroids["Plessis 1817"]="geosrs:Plessis1817"
spheroids["PZ-90"]="geosrs:PZ90"
spheroids["Struve 1860"]="geosrs:Struve1860"
spheroids["War Office"]="geosrs:WarOffice"
spheroids["Walbeck"]="geosrs:Walbeck"
spheroids["walbeck"]="geosrs:Walbeck"
spheroids["WGS66"]="geosrs:WGS66"
spheroids["WGS 66"]="geosrs:WGS66"
spheroids["WGS72"]="geosrs:WGS72"
spheroids["WGS 72"]="geosrs:WGS72"
spheroids["WGS84"]="geosrs:WGS84"
spheroids["WGS 84"]="geosrs:WGS84"
spheroids["Zach 1812"]="geosrs:Zach1812"
projections={}
projections["adams_ws1"]="geosrs:AdamsWorldInASquareIProjection"
projections["adams_ws2"]="geosrs:AdamsWorldInASquareIIProjection"
projections["aea"]="geosrs:AlbersEqualAreaProjection"
projections["aeqd"]= "geosrs:AzimuthalEquidistantProjection"
projections["airy"]="geosrs:AiryProjection"
projections["aitoff"]="geosrs:AitoffProjection"
projections["poly"]="geosrs:AmericanPolyconicProjection"
projections["apian"]="geosrs:ApianGlobularIProjection"
projections["august"]= "geosrs:AugustEpicycloidalProjection"
projections["bacon"]= "geosrs:BaconGlobularProjection"
projections["bertin1953"]="geosrs:BertinProjection"
projections["boggs"]="geosrs:BoggsEumorphicProjection"
projections["bonne"]="geosrs:BonneProjection"
projections["cass"]="geosrs:CassiniProjection"
projections["cc"]="geosrs:CentralCylindricalProjection"
projections["ccon"]="geosrs:CentralConicProjection"
projections["cea"]="geosrs:CylindricalEqualArea"
projections["chamb"]="geosrs:ChamberlinTrimetricProjection"
projections["comill"]="geosrs:CompactMillerProjection"
projections["col_urban"]="geosrs:ColombiaUrbanProjection"
projections["crast"]="geosrs:CrasterParabolicProjection"
projections["eck1"]="geosrs:Eckert1Projection"
projections["eck2"]="geosrs:Eckert2Projection"
projections["eck3"]="geosrs:Eckert3Projection"
projections["eck4"]="geosrs:Eckert4Projection"
projections["eck5"]="geosrs:Eckert5Projection"
projections["eck6"]="geosrs:Eckert6Projection"
projections["eqc"]="geosrs:EquidistantCylindricalProjection"
projections["eqdc"]="geosrs:EquidistantConicProjection"
projections["eqearth"]="geosrs:EqualEarthProjection"
projections["collg"]="geosrs:CollignonProjection"
projections["col_urban"]="geosrs:ColombiaUrbanProjection"
projections["denoy"]="geosrs:DenoyerSemiEllipticalProjection"
projections["fahey"]="geosrs:FaheyProjection"
projections["fouc_s"]="geosrs:FoucautSinusoidalProjection"
projections["gall"]="geosrs:GallStereographicProjection"
projections["geocent"]="geosrs:Geocentric"
projections["gins8"]="geosrs:GinzburgVIIIProjection"
projections["gnom"]="geosrs:GnomonicProjection"
projections["goode"]="geosrs:GoodeHomolosineProjection"
projections["guyou"]="geosrs:GuyouProjection"
projections["hatano"]="geosrs:HatanoAsymmetricalEqualAreaProjection"
projections["healpix"]="geosrs:HEALPixProjection"
projections["igh"]="geosrs:InterruptedGoodeHomolosineProjection"
projections["igh_o"]="geosrs:InterruptedGoodeHomolosineOceanicViewProjection"
projections["kav5"]="geosrs:PseudoCylindricalProjection"
projections["kav7"]="geosrs:Kavrayskiy7Projection"
projections["krovak"]="geosrs:Krovak"
projections["laea"]="geosrs:LambertAzimuthalEqualArea"
projections["lagrng"]="geosrs:LagrangeProjection"
projections["larr"]="geosrs:LarriveeProjection"
projections["lask"]="geosrs:LaskowskiProjection"
projections["latlong"]="geosrs:LatLonProjection"
projections["lcc"]="geosrs:LambertConformalConicProjection"
projections["leac"]="geosrs:LambertEqualAreaConic"
projections["labrd"]="geosrs:LabordeProjection"
projections["longlat"]="geosrs:LonLatProjection"
projections["loxim"]="geosrs:LoximuthalProjection"
projections["mbt_s"]="geosrs:McBrydeThomasIProjection"
projections["mbt_fps"]="geosrs:McBrydeThomasIIProjection"
projections["mbtfpp"]="geosrs:McBrydeThomasFlatPolarParabolicProjection"
projections["mbtfpq"]="geosrs:McBrydeThomasFlatPolarQuarticProjection"
projections["mbtfps"]="geosrs:McBrydeThomasFlatPolarSinusoidalProjection"
projections["merc"]="geosrs:MercatorProjection"
projections["mill"]="geosrs:MillerProjection"
projections["mil_os"]="geosrs:MillerOblatedStereographicProjection"
projections["murd1"]="geosrs:MurdochIProjection"
projections["murd2"]="geosrs:MurdochIIProjection"
projections["murd3"]="geosrs:MurdochIIIProjection"
projections["natearth"]="geosrs:NaturalEarthProjection"
projections["natearth2"]="geosrs:NaturalEarth2Projection"
projections["moll"]="geosrs:MollweideProjection"
projections["nell"]="geosrs:PseudoCylindricalProjection"
projections["nell_h"]="geosrs:NellHammerProjection"
projections["nicol"]="geosrs:NicolosiGlobularProjection"
projections["ocea"]="geosrs:ObliqueCylindricalEqualAreaProjection"
projections["omerc"]="geosrs:ObliqueMercatorProjection"
projections["sterea"]="geosrs:ObliqueStereographicProjection"
projections["ocea"]="geosrs:ObliqueCylindricalEqualAreaProjection"
projections["ortel"]="geosrs:OrteliusOvalProjection"
projections["ortho"]="geosrs:OrthographicProjection"
projections["patterson"]="geosrs:PattersonCylindricalProjection"
projections["pconic"]="geosrs:PerspectiveConicProjection"
projections["poly"]="geosrs:AmericanPolyconicProjection"
projections["peirce_q"]="geosrs:PeirceQuincuncialProjection"
projections["putp1"]="geosrs:PutninsP1Projection"
projections["putp2"]="geosrs:PutninsP2Projection"
projections["putp3"]="geosrs:PutninsP3Projection"
projections["putp3p"]="geosrs:PutninsP3'Projection"
projections["putp4"]="geosrs:PutninsP4Projection"
projections["putp4p"]="geosrs:PutninsP4'Projection"
projections["putp5"]="geosrs:PutninsP5Projection"
projections["putp6"]="geosrs:PutninsP6Projection"
projections["putp6p"]="geosrs:PutninsP6'Projection"
projections["qua_aut"]="geosrs:QuarticAuthalicProjection"
projections["qsc"]="geosrs:QuadrilateralizedSphericalCubeProjection"
projections["rpoly"]="geosrs:RectangularPolyconicProjection"
projections["robin"]="geosrs:RobinsonProjection"
projections["rouss"]="geosrs:RoussilheProjection"
projections["rpoly"]="geosrs:RectangularPolyconicProjection"
projections["stere"]="geosrs:StereographicProjection"
projections["sinu"]="geosrs:SinusoidalProjection"
projections["tcea"]="geosrs:TransverseCylindricalEqualAreaProjection"
projections["tpeqd"]="geosrs:TwoPointEquidistantProjection"
projections["times"]="geosrs:TheTimesProjection"
projections["tmerc"]="geosrs:TransverseMercatorProjection"
projections["utm"]="geosrs:UniversalTransverseMercatorProjection"
projections["vandg"]="geosrs:VanDerGrintenIProjection"
projections["vandg2"]="geosrs:VanDerGrintenIIProjection"
projections["vandg3"]="geosrs:VanDerGrintenIIIProjection"
projections["vandg4"]="geosrs:VanDerGrintenIVProjection"
projections["vitk1"]="geosrs:VitkovskyIProjection"
projections["wintri"]="geosrs:WinkelTripelProjection"
projections["wag1"]="geosrs:WagnerIProjection"
projections["wag2"]="geosrs:WagnerIIProjection"
projections["wag3"]="geosrs:WagnerIIIProjection"
projections["wag4"]="geosrs:WagnerIVProjection"
projections["wag5"]="geosrs:WagnerVProjection"
projections["wag6"]="geosrs:WagnerVIProjection"
projections["wag7"]="geosrs:WagnerVIIProjection"
projections["wag8"]="geosrs:WagnerVIIIProjection"
projections["wag9"]="geosrs:WagnerIXProjection"
projections["weren"]="geosrs:WerenskioldIProjection"
ttl=set()
ttlhead="@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .\n"
ttlhead+="@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .\n"
ttlhead+="@prefix owl: <http://www.w3.org/2002/07/owl#> .\n"
ttlhead+="@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .\n"
ttlhead+="@prefix skos: <http://www.w3.org/2004/02/skos/core#> .\n"
ttlhead+="@prefix prov: <http://www.w3.org/ns/prov-o/> .\n"
ttlhead+="@prefix geoepsg: <http://www.opengis.net/def/crs/EPSG/0/> .\n"
ttlhead+="@prefix geo: <http://www.opengis.net/ont/geosparql#> .\n"
ttlhead+="@prefix geosrs: <https://w3id.org/geosrs/> .\n"
ttlhead+="@prefix geosrsdatum: <http://www.opengis.net/ont/crs/datum/> .\n"
ttlhead+="@prefix geosrsisbody: <http://www.opengis.net/ont/crs/isbody/> .\n"
ttlhead+="@prefix geosrsgrid: <http://www.opengis.net/ont/crs/grid/> .\n"
ttlhead+="@prefix geosrsproj: <http://www.opengis.net/ont/crs/proj/> .\n"
ttlhead+="@prefix geosrsaxis: <http://www.opengis.net/ont/crs/cs/axis/> .\n"
ttlhead+="@prefix geosrsgeod: <http://www.opengis.net/ont/crs/geod/> .\n"
ttlhead+="@prefix geosrsaou: <http://www.opengis.net/ont/crs/areaofuse/> .\n"
ttlhead+="@prefix geosrsmeridian: <http://www.opengis.net/ont/crs/primeMeridian/> .\n"
ttlhead+="@prefix geosrsoperation: <http://www.opengis.net/ont/crs/operation/> .\n"
ttlhead+="@prefix geocs: <https://w3id.org/geosrs/cs/> .\n"
ttlhead+="@prefix dc: <http://purl.org/dc/elements/1.1/> .\n"
ttlhead+="@prefix wd: <http://www.wikidata.org/entity/> .\n"
ttlhead+="@prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/> .\n"
geodcounter=1

parser = argparse.ArgumentParser()
parser.add_argument("input", type=str,nargs='?',help="the input file to convert or an epsg code to convert")
parser.add_argument("outputformat", type=str, nargs='?',default="projjson", help="output format",choices=['wkt', 'proj', 'projjson','ttl'])
args = parser.parse_args()
print(args)
mapp=pyproj.list.get_proj_operations_map()
if args.input==None:
	for x in list(range(2000,10000))+list(range(20000,30000)):
		try:
			curcrs=CRS.from_epsg(x)
			#print("EPSG: "+str(x))
		except:
			continue	
		crsToTTL(ttl,curcrs,x,geodcounter,None)
	f = open("result.nt", "w", encoding="utf-8")
	f.write(ttlhead+"".join(ttl))
	f.close()
	graph2 = Graph()
	graph2.parse(data = ttlhead+"".join(ttl), format='n3')
	graph2.serialize(destination='result.ttl', format='turtle')
else:
	if str(args.input).startswith("EPSG"):
		curcrs=CRS.from_epsg(int(str(args.input).replace("EPSG:","")))
		#print(curcrs.area_of_use)
	if args.outputformat=="wkt":
		thewkt=curcrs.to_wkt()
		f = open(str(args.input).replace(":","_")+".wkt", "a")
		f.write(thewkt)
		f.close()
	if args.outputformat=="projjson":
		thedict=curcrs.to_json_dict()
		thedict["@context"]="https://opengeospatial.github.io/ontology-crs/context/geosrs-context.json"
		#print(thedict)
		with open(str(args.input).replace(":","_")+".json", 'w') as f:
			json.dump(thedict, f,indent=2,sort_keys=True)    
	if args.outputformat=="ttl":
		crsToTTL(ttl,curcrs,int(str(args.input).replace("EPSG:","")),geodcounter,None)
		graph2 = Graph()
		graph2.parse(data = ttlhead+"".join(ttl), format='n3')
		graph2.serialize(destination=str(args.input).replace(":","_")+".ttl", format='turtle')
examplefile.write(json.dumps(examples,indent=2,sort_keys=True))
examplefile.close()
print(scopescoll)
print(crstypescoll)
print(projectionscoll)
print(spheroidscoll)
