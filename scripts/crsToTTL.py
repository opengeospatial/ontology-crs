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
			ttl.add("geoepsg:"+epsgcode+" geosrs:asProj4 \""+curcrs.to_proj4().strip().replace("\"","'")+"\"^^xsd:string . \n")
	except:
		print("error")
	if curcrs.to_json()!=None:
		ttl.add("geoepsg:"+epsgcode+" geosrs:asProjJSON \""+curcrs.to_json().strip().replace("\"","'")+"\"^^xsd:string . \n")		
	if wkt!="":
		ttl.add("geoepsg:"+epsgcode+" geosrs:asWKT \""+wkt+"\"^^geosrs:wktLiteral . \n")
	ttl.add("geoepsg:"+epsgcode+" geosrs:epsgCode \"EPSG:"+epsgcode+"\"^^xsd:string . \n")		
	#i+=1


units={}
units["m"]="om:meter"
units["metre"]="om:metre"
units["grad"]="om:degree"
units["degree"]="om:degree"
units["ft"]="om:foot"
units["us-ft"]="om:usfoot"
scope={}
scope["geodesy"]="geosrs:Geodesy"
scope["topographic mapping"]="geosrs:TopographicMap"
scope["spatial referencing"]="geosrs:SpatialReferencing"
scope["engineering survey"]="geosrs:EngineeringSurvey"
scope["satellite survey"]="geosrs:SatelliteSurvey"
scope["satellite navigation"]="geosrs:SatelliteNvaigation"
scope["coastal hydrography"]="geosrs:CoastalHydrography"
scope["offshore engineering"]="geosrs:OffshoreEngineering"
scope["hydrography"]="geosrs:Hydrography"
scope["drilling"]="geosrs:Drilling"
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
spheroids["GRS80"]="geosrsgeod:GRS1980"
spheroids["GRS 80"]="geosrsgeod:GRS1980"
spheroids["GRS67"]="geosrsgeod:GRS67"
spheroids["GRS 1967"]="geosrsgeod:GRS67"
spheroids["GRS 1967 Modified"]="geosrsgeod:GRS67Modified"
spheroids["GRS 67"]="geosrsgeod:GRS67"
spheroids["GRS1980"]="geosrsgeod:GRS1980"
spheroids["GRS 1980"]="geosrsgeod:GRS1980"
spheroids["NWL 9D"]="geosrsgeod:NWL9D"
spheroids["PZ-90"]="geosrsgeod:PZ90"
spheroids["Airy 1830"]="geosrsgeod:Airy1830"
spheroids["Airy Modified 1849"]="geosrsgeod:AiryModified1849"
spheroids["intl"]="geosrsgeod:International1924"
spheroids["aust_SA"]="geosrsgeod:AustralianNationalSpheroid"
spheroids["Australian National Spheroid"]="geosrsgeod:AustralianNationalSpheroid"
spheroids["International 1924"]="geosrsgeod:International1924"
spheroids["clrk"]="geosrsgeod:Clarke1866"
spheroids["War Office"]="geosrsgeod:WarOffice"
spheroids["evrst30"]="geosrsgeod:Everest1930"
spheroids["clrk66"]="geosrsgeod:Clarke1866"
spheroids["Plessis 1817"]="geosrsgeod:Plessis1817"
spheroids["Danish 1876"]="geosrsgeod:Danish1876"
spheroids["Struve 1860"]="geosrsgeod:Struve1860"
spheroids["IAG 1975"]="geosrsgeod:IAG1975"
spheroids["Clarke 1866"]="geosrsgeod:Clarke1866"
spheroids["Clarke 1858"]="geosrsgeod:Clarke1858"
spheroids["Clarke 1880"]="geosrsgeod:Clarke1880"
spheroids["Helmert 1906"]="geosrsgeod:Helmert1906"
spheroids["Moon_2000_IAU_IAG"]="geosrsgeod:Moon2000_IAU_IAG"
spheroids["CGCS2000"]="geosrsgeod:CGCS2000"
spheroids["GSK-2011"]="geosrsgeod:GSK2011"
spheroids["Zach 1812"]="geosrsgeod:Zach1812"
spheroids["Hough 1960"]="geosrsgeod:Hough1960"
spheroids["Hughes 1980"]="geosrsgeod:Hughes1980"
spheroids["Indonesian National Spheroid"]="geosrsgeod:IndonesianNationalSpheroid"
spheroids["clrk80"]="geosrsgeod:Clarke1880RGS"
spheroids["Clarke 1880 (Arc)"]="geosrsgeod:Clarke1880ARC"
spheroids["Clarke 1880 (RGS)"]="geosrsgeod:Clarke1880RGS"
spheroids["Clarke 1880 (IGN)"]="geosrsgeod:Clarke1880IGN"
spheroids["clrk80ign"]="geosrsgeod:Clarke1880IGN"
spheroids["WGS66"]="geosrsgeod:WGS66"
spheroids["WGS 66"]="geosrsgeod:WGS66"
spheroids["WGS72"]="geosrsgeod:WGS72"
spheroids["WGS 72"]="geosrsgeod:WGS72"
spheroids["WGS84"]="geosrsgeod:WGS84"
spheroids["WGS 84"]="geosrsgeod:WGS84"
spheroids["Krassowsky 1940"]="geosrsgeod:Krassowsky1940"
spheroids["krass"]="geosrsgeod:Krassowsky1940"
spheroids["Bessel 1841"]="geosrsgeod:Bessel1841"
spheroids["bessel"]="geosrsgeod:Bessel1841"
spheroids["Bessel Modified"]="geosrsgeod:BesselModified"
projections={}
projections["tmerc"]="geosrs:TransverseMercatorProjection"
projections["omerc"]="geosrs:ObliqueMercatorProjection"
projections["merc"]="geosrs:MercatorProjection"
projections["sinu"]="geosrs:SinusoidalProjection"
projections["rpoly"]="geosrs:RectangularPolyconicProjection"
projections["poly"]="geosrs:AmericanPolyconicProjection"
projections["eqdc"]="geosrs:EquidistantConicProjection"
projections["sterea"]="geosrs:ObliqueStereographicProjection"
projections["cea"]="geosrs:CylindricalEqualArea"
projections["aea"]="geosrs:AlbersEqualAreaProjection"
projections["eqearth"]="geosrs:EqualEarthProjection"
projections["natearth"]="geosrs:NaturalEarthProjection"
projections["stere"]="geosrs:StereographicProjection"
projections["cass"]="geosrs:CassiniProjection"
projections["nell"]="geosrs:PseudoCylindricalProjection"
projections["eck1"]="geosrs:PseudoCylindricalProjection"
projections["eck2"]="geosrs:PseudoCylindricalProjection"
projections["eck3"]="geosrs:PseudoCylindricalProjection"
projections["eck4"]="geosrs:PseudoCylindricalProjection"
projections["eck5"]="geosrs:PseudoCylindricalProjection"
projections["eck6"]="geosrs:PseudoCylindricalProjection"
projections["eqc"]="geosrs:EquidistantCylindricalProjection"
projections["col_urban"]="geosrs:ColombiaUrbanProjection"
projections["laea"]="geosrs:LambertAzimuthalEqualArea"
projections["leac"]="geosrs:LambertEqualAreaConic"
projections["labrd"]="geosrs:LabordeProjection"
projections["lcc"]="geosrs:LambertConformalConicProjection"
projections["gnom"]="geosrs:GnomonicProjection"
projections["bonne"]="geosrs:BonneProjection"
projections["moll"]="geosrs:MollweideProjection"
projections["mill"]="geosrs:MillerProjection"
projections["nicol"]="geosrs:NicolosiGlobularProjection"
projections["collg"]="geosrs:CollignonProjection"
projections["robin"]="geosrs:RobinsonProjection"
projections["loxim"]="geosrs:LoximuthalProjection"
projections["aitoff"]="geosrs:AitoffProjection"
projections["ortho"]="geosrs:OrthographicProjection"
projections["kav5"]="geosrs:PseudoCylindricalProjection"
projections["tcea"]="geosrs:CylindricalProjection"
projections["utm"]="geosrs:UniversalTransverseMercatorProjection"
projections["krovak"]="geosrs:Krovak"
projections["geocent"]="geosrs:Geocentric"
projections["latlong"]="geosrs:LatLonProjection"
projections["longlat"]="geosrs:LonLatProjection"
projections["nell"]="geosrs:NellProjection"
#projections["cc"]="geosrs:CylindricalProjection"
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
