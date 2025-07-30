var namespaces={"rdf":"http://www.w3.org/1999/02/22-rdf-syntax-ns#","xsd":"http://www.w3.org/2001/XMLSchema#","geo":"http://www.opengis.net/ont/geosparql#","rdfs":"http://www.w3.org/2000/01/rdf-schema#","owl":"http://www.w3.org/2002/07/owl#","dc":"http://purl.org/dc/terms/","skos":"http://www.w3.org/2004/02/skos/core#"}
var annotationnamespaces=["http://www.w3.org/2004/02/skos/core#","http://www.w3.org/2000/01/rdf-schema#","http://purl.org/dc/terms/"]
var indexpage=false
var rangesByAttribute={}
var overlayMaps={}
var baseMaps = {}
props={}
var geoproperties={
   "http://www.opengis.net/ont/geosparql#asWKT":"DatatypeProperty",
   "http://www.opengis.net/ont/geosparql#asGML": "DatatypeProperty",
   "http://www.opengis.net/ont/geosparql#asKML": "DatatypeProperty",
   "http://www.opengis.net/ont/geosparql#asGeoJSON": "DatatypeProperty",
   "http://www.opengis.net/ont/geosparql#hasGeometry": "ObjectProperty",
   "http://www.opengis.net/ont/geosparql#hasDefaultGeometry": "ObjectProperty",
   "http://www.w3.org/2003/01/geo/wgs84_pos#geometry": "ObjectProperty",
   "http://www.georss.org/georss/point": "DatatypeProperty",
   "http://www.w3.org/2006/vcard/ns#hasGeo": "ObjectProperty",
   "http://www.w3.org/2003/01/geo/wgs84_pos#lat":"DatatypeProperty",
   "http://www.w3.org/2003/01/geo/wgs84_pos#long": "DatatypeProperty",
   "http://www.semanticweb.org/ontologies/2015/1/EPNet-ONTOP_Ontology#hasLatitude": "DatatypeProperty",
   "http://www.semanticweb.org/ontologies/2015/1/EPNet-ONTOP_Ontology#hasLongitude": "DatatypeProperty",
   "http://schema.org/geo": "ObjectProperty",
   "http://schema.org/polygon": "DatatypeProperty",
   "https://schema.org/geo": "ObjectProperty",
   "https://schema.org/polygon": "DatatypeProperty",
   "http://geovocab.org/geometry#geometry": "ObjectProperty",
   "http://www.w3.org/ns/locn#geometry": "ObjectProperty",
   "http://rdfs.co/juso/geometry": "ObjectProperty",
   "http://www.wikidata.org/prop/direct/P625":"DatatypeProperty",
   "https://database.factgrid.de/prop/direct/P48": "DatatypeProperty",
   "http://database.factgrid.de/prop/direct/P48":"DatatypeProperty",
   "http://www.wikidata.org/prop/direct/P3896": "DatatypeProperty"
}

commentproperties={
    "http://www.w3.org/2004/02/skos/core#definition":"DatatypeProperty",
    "http://www.w3.org/2004/02/skos/core#note": "DatatypeProperty",
    "http://www.w3.org/2004/02/skos/core#scopeNote": "DatatypeProperty",
    "http://www.w3.org/2004/02/skos/core#historyNote": "DatatypeProperty",
    "https://schema.org/description":"DatatypeProperty",
    "http://www.w3.org/2000/01/rdf-schema#comment": "DatatypeProperty",
    "http://purl.org/dc/terms/description": "DatatypeProperty",
    "http://purl.org/dc/elements/1.1/description": "DatatypeProperty"
}

labelproperties={
    "http://www.w3.org/2004/02/skos/core#prefLabel":"DatatypeProperty",
    "http://www.w3.org/2004/02/skos/core#prefSymbol": "DatatypeProperty",
    "http://www.w3.org/2004/02/skos/core#altLabel": "DatatypeProperty",
    "https://schema.org/name": "DatatypeProperty",
    "https://schema.org/alternateName": "DatatypeProperty",
    "http://purl.org/dc/terms/title": "DatatypeProperty",
    "http://purl.org/dc/elements/1.1/title":"DatatypeProperty",
    "http://www.w3.org/2004/02/skos/core#altSymbol": "DatatypeProperty",
    "http://www.w3.org/2004/02/skos/core#hiddenLabel": "DatatypeProperty",
    "http://www.w3.org/2000/01/rdf-schema#label": "DatatypeProperty"
}

var baseurl=""
  $( function() {
    var availableTags = Object.keys(search)
    $( "#search" ).autocomplete({
      source: availableTags,
      delay: 300
    });
    //console.log(availableTags)
    setupJSTree()
  } );

function openNav() {
  document.getElementById("mySidenav").style.width = "400px";
}

function closeNav() {
  document.getElementById("mySidenav").style.width = "0";
}

function exportChartJS(){
    saveTextAsFile(JSON.stringify({"xValues":xValues,"yValues":yValues}),"json")
}

function exportGeoJSON(){
    if(typeof(feature) !== "undefined"){
        saveTextAsFile(JSON.stringify(feature),"geojson")
    }else if(window.location.href.includes("_nonns")){
        downloadFile(window.location.href.replace(".html",".geojson"))
    }
}

function parseWKTStringToJSON(wktstring){
    wktstring=wktstring.substring(wktstring.lastIndexOf('(')+1,wktstring.lastIndexOf(')')-1)
    resjson=[]
    for(coordset of wktstring.split(",")){
        curobject={}
        coords=coordset.trim().split(" ")
        //console.log(coordset)
        //console.log(coords)
        if(coords.length==3){
            resjson.push({"x":parseFloat(coords[0]),"y":parseFloat(coords[1]),"z":parseFloat(coords[2])})
        }else{
            resjson.push({"x":parseFloat(coords[0]),"y":parseFloat(coords[1])})
        }
    }
    //console.log(resjson)
    return resjson
}

function testRDFLibParsing(cururl){
    var store = $rdf.graph()
    var timeout = 5000 // 5000 ms timeout
    var fetcher = new $rdf.Fetcher(store, timeout)

    fetcher.nowOrWhenFetched(cururl, function(ok, body, response) {
        if (!ok) {
            console.log("Oops, something happened and couldn't fetch data " + body);
        } else if (response.onErrorWasCalled || response.status !== 200) {
            console.log('    Non-HTTP error reloading data! onErrorWasCalled=' + response.onErrorWasCalled + ' status: ' + response.status)
        } else {
            console.log("---data loaded---")
        }
    })
	return store
}

function exportCSV(sepchar,filesuffix){
    rescsv=""
    if(typeof(feature)!=="undefined"){
        if("features" in feature){
           for(feat of feature["features"]){
                rescsv+="\""+feat["geometry"]["type"].toUpperCase()+"("
				if(feature["geometry"]["type"].toUpperCase()=="POINT"){
                    rescsv =  rescsv + feature["geometry"].coordinates[0] + ' ' + feature["geometry"].coordinates[1]
				}else{
					feature["geometry"].coordinates.forEach(function(p,i){
						if(i<feature["geometry"].coordinates.length-1) rescsv =  rescsv + p[0] + ' ' + p[1] + ', ';
						else rescsv =  rescsv + p[0] + ' ' + p[1] + ')';
					})
				}
                rescsv+=")\""+sepchar
                if("properties" in feat){
                    if(gottitle==false){
                       rescsvtitle="\"the_geom\","
                       for(prop in feat["properties"]){
                          rescsvtitle+="\""+prop+"\""+sepchar
                       }
                       rescsvtitle+="\n"
                       rescsv=rescsvtitle+rescsv
                       gottitle=true
                    }
                    for(prop in feat["properties"]){
                        rescsv+="\""+feat["properties"][prop]+"\""+sepchar
                    }
                }
                rescsv+="\n"
           }
        }else{
            gottitle=false
            rescsv+="\""+feature["geometry"]["type"].toUpperCase()+"("
			if(feature["geometry"]["type"].toUpperCase()=="POINT"){
				rescsv =  rescsv + feature["geometry"].coordinates[0] + ' ' + feature["geometry"].coordinates[1]
			}else{
				feature["geometry"].coordinates.forEach(function(p,i){
					if(i<feature["geometry"].coordinates.length-1) rescsv =  rescsv + p[0] + ' ' + p[1] + ', ';
					else rescsv =  rescsv + p[0] + ' ' + p[1] + ')';
				})
			}
            rescsv+=")\""+sepchar
            if("properties" in feature){
                if(gottitle==false){
                   rescsvtitle=""
                   for(prop in feature["properties"]){
                      rescsvtitle+="\""+prop+"\""+sepchar
                   }
                   rescsvtitle+="\n"
                   rescsv=rescsvtitle+rescsv
                   gottitle=true
                }
                for(prop in feature["properties"]){
                    rescsv+="\""+feature["properties"][prop]+"\""+sepchar
                }
            }
        }
        saveTextAsFile(rescsv,filesuffix)
    }else if(typeof(nongeofeature)!=="undefined"){
        if("features" in nongeofeature){
           for(feat of nongeofeature["features"]){
                if("properties" in feat){
                    if(gottitle==false){
                       rescsvtitle="\"the_geom\","
                       for(prop in feat["properties"]){
                          rescsvtitle+="\""+prop+"\""+sepchar
                       }
                       rescsvtitle+="\n"
                       rescsv=rescsvtitle+rescsv
                       gottitle=true
                    }
                    for(prop in feat["properties"]){
                        rescsv+="\""+feat["properties"][prop]+"\""+sepchar
                    }
                }
                rescsv+="\n"
           }
        }else{
            gottitle=false
            if("properties" in nongeofeature){
                if(gottitle==false){
                   rescsvtitle=""
                   for(prop in nongeofeature["properties"]){
                      rescsvtitle+="\""+prop+"\""+sepchar
                   }
                   rescsvtitle+="\n"
                   rescsv=rescsvtitle+rescsv
                   gottitle=true
                }
                for(prop in nongeofeature["properties"]){
                    rescsv+="\""+nongeofeature["properties"][prop]+"\""+sepchar
                }
            }
        }
        saveTextAsFile(rescsv,filesuffix)
    }
}

function exportGraphML(){
	resgml=`<?xml version="1.0" encoding="UTF-8"?>\n<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:y="http://www.yworks.com/xml/graphml" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">\n`
	resgml+="<key for=\"node\" id=\"nodekey\" yfiles.type=\"nodegraphics\"></key><key for=\"edge\" id=\"edgekey\" yfiles.type=\"edgegraphics\"></key><graph id=\"G\" edgedefault=\"directed\">\n"
	processedURIs={}
	literalcounter=1
	edgecounter=0
	if(typeof(featurecolls)!=="undefined"){
        for(feature of featurecolls){
			if("features" in feature){
                for(feat of feature["features"]){
					if(!(feat.id in processedURIs)){
						resgml+="<node id=\""+feat.id+"\" uri=\""+feat.id+"\"><data key=\"nodekey\"><y:ShapeNode><y:Shape shape=\"ellipse\"></y:Shape><y:Fill color=\"#800080\" transparent=\"false\"></y:Fill><y:NodeLabel alignment=\"center\" fontSize=\"12\" fontStyle=\"plain\" hasText=\"true\" visible=\"true\" width=\"4.0\">"+feat.name+"</y:NodeLabel></y:ShapeNode></data></node>\n"
						processedURIs[feat.id]=true
					}
					if("properties" in feat){
                        for(prop in feat["properties"]){
							thetarget=feat["properties"][prop]
							if((feat["properties"][prop]+"").startsWith("http") && !(feat["properties"][prop] in processedURIs)){
								resgml+="<node id=\""+feat["properties"][prop]+"\" uri=\""+feat["properties"][prop]+"\"><data key=\"nodekey\"><y:ShapeNode><y:Shape shape=\"ellipse\"></y:Shape><y:Fill color=\"#800080\" transparent=\"false\"></y:Fill><y:NodeLabel alignment=\"center\" fontSize=\"12\" fontStyle=\"plain\" hasText=\"true\" visible=\"true\" width=\"4.0\">"+feat["properties"][prop]+"</y:NodeLabel></y:ShapeNode></data></node>\n"
								processedURIs[feat["properties"][prop]]=true
							}else{
								thetarget="literal"+literalcounter
								resgml+="<node id=\""+thetarget+"\" uri=\""+thetarget+"\"><data key=\"nodekey\"><y:ShapeNode><y:Shape shape=\"ellipse\"></y:Shape><y:Fill color=\"#F08080\" transparent=\"false\"></y:Fill><y:NodeLabel alignment=\"center\" fontSize=\"12\" fontStyle=\"plain\" hasText=\"true\" visible=\"true\" width=\"4.0\">"+feat["properties"][prop]+"</y:NodeLabel></y:ShapeNode></data></node>\n"
								literalcounter+=1
							}
							resgml+="<edge id=\"e"+edgecounter+"\" uri=\""+prop+"\" source=\""+feat.id+"\" target=\""+thetarget+"\"><data key=\"edgekey\"><y:PolyLineEdge><y:EdgeLabel alignment=\"center\" configuration=\"AutoFlippingLabel\" fontSize=\"12\" fontStyle=\"plain\" hasText=\"true\" visible=\"true\" width=\"4.0\">"+shortenURI(prop)+"</y:EdgeLabel></y:PolyLineEdge></data></edge>\n"
							edgecounter+=1
						}
					}
				}
			}else if("type" in feature && feature["type"]=="Feature"){
				if(!(feature.id in processedURIs)){
					resgml+="<node id=\""+feature.id+"\" uri=\""+feature.id+"\"><data key=\"nodekey\"><y:ShapeNode><y:Shape shape=\"ellipse\"></y:Shape><y:Fill color=\"#800080\" transparent=\"false\"></y:Fill><y:NodeLabel alignment=\"center\" fontSize=\"12\" fontStyle=\"plain\" hasText=\"true\" visible=\"true\" width=\"4.0\">"+feature.name+"</y:NodeLabel></y:ShapeNode></data></node>\n"
					processedURIs[feature.id]=true
				}
				if("properties" in feature){
					for(prop in feature["properties"]){
						thetarget=feature["properties"][prop]
						if((feature["properties"][prop]+"").startsWith("http") && !(feature["properties"][prop] in processedURIs)){
							resgml+="<node id=\""+feature["properties"][prop]+"\" uri=\""+feature["properties"][prop]+"\"><data key=\"nodekey\"><y:ShapeNode><y:Shape shape=\"ellipse\"></y:Shape><y:Fill color=\"#800080\" transparent=\"false\"></y:Fill><y:NodeLabel alignment=\"center\" fontSize=\"12\" fontStyle=\"plain\" hasText=\"true\" visible=\"true\" width=\"4.0\">"+feature["properties"][prop]+"</y:NodeLabel></y:ShapeNode></data></node>\n"
							processedURIs[feature["properties"][prop]]=true
						}else{
							thetarget="literal"+literalcounter
							resgml+="<node id=\""+thetarget+"\" uri=\""+thetarget+"\"><data key=\"nodekey\"><y:ShapeNode><y:Shape shape=\"ellipse\"></y:Shape><y:Fill color=\"#F08080\" transparent=\"false\"></y:Fill><y:NodeLabel alignment=\"center\" fontSize=\"12\" fontStyle=\"plain\" hasText=\"true\" visible=\"true\" width=\"4.0\">"+feature["properties"][prop]+"</y:NodeLabel></y:ShapeNode></data></node>\n"
							literalcounter+=1
						}
						resgml+="<edge id=\"e"+edgecounter+"\" uri=\""+prop+"\" source=\""+feature.id+"\" target=\""+thetarget+"\"><data key=\"edgekey\"><y:PolyLineEdge><y:EdgeLabel alignment=\"center\" configuration=\"AutoFlippingLabel\" fontSize=\"12\" fontStyle=\"plain\" hasText=\"true\" visible=\"true\" width=\"4.0\">"+shortenURI(prop)+"</y:EdgeLabel></y:PolyLineEdge></data></edge>\n"
						edgecounter+=1
					}
				}
			}
		}
	}
	resgml+="</graph>\n</graphml>\n"
	saveTextAsFile(resgml,"graphml")
}


function convertDecimalToLatLonText(D, lng){
	dir=""
	if(D<0) {
		if(lng) {
			dir="W";
		}else {
			dir="S";
		}
	}else {
		if(lng) {
			dir="E";
		}else {
			dir="N";
		}
	}
	deg=D<0?-D:D;
	min=D%1*60;
	sec=(D*60%1*6000)/100;
	return deg+"°"+min+"'"+sec+"\""+dir;
}

function exportLatLonText(){
	res=""
	for(point of centerpoints){
		res+=convertDecimalToLatLonText(point["lat"],false)+" "+convertDecimalToLatLonText(point["lng"],true)+"\n"
	}
	saveTextAsFile(res,"txt")
}

function exportGML(){
	resgml=">\n"
    resgmlhead="<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<gml:FeatureCollection xmlns:gml=\"http://www.opengis.net/gml\" "
    nscounter=0
    nsmap={}
	if(typeof(featurecolls)!=="undefined"){
        for(feature of featurecolls){
            if("features" in feature){
                for(feat of feature["features"]){
					resgml+="<gml:featureMember>"
					if("properties" in feat){
                        for(prop in feat["properties"]){
                            ns=shortenURI(prop,true)
                            nsprefix=""
                            if(ns in namespaces && !(ns in nsmap)){
                                nsmap[ns]=namespaces[ns]
                                resgmlhead+="xmlns:"+namespaces[ns]+"=\""+ns+"\" "
                            }
                            if(!(ns in nsmap)){
                                nsmap[ns]="ns"+nscounter
                                nsprefix="ns"+nscounter
                                resgmlhead+="xmlns:"+nsprefix+"=\""+ns+"\" "
                                nscounter+=1
                            }else{
                                nsprefix=nsmap[ns]
                            }
                            if(Array.isArray(feat["properties"][prop])){
								for(arritem of feat["properties"][prop]){
									resgml+="<"+shortenURI(prop,false,nsprefix)+">"+arritem+"</"+shortenURI(prop,false,nsprefix)+">\n"
								}
                            }else{
                                resgml+="<"+shortenURI(prop,false,nsprefix)+">"+feat["properties"][prop]+"</"+shortenURI(prop,false,nsprefix)+">\n"
                            }
                        }
                    }
					if("geometry" in feat){
						resgml+="<the_geom><gml:"+feat["geometry"]["type"]+">\n"
						resgml+="<gml:pos>\n"
						if(feat["geometry"]["type"].toUpperCase()=="POINT"){
							resgml += feat["geometry"].coordinates[0] + ' ' + feat["geometry"].coordinates[1]+'\n '
						}else{
							feat["geometry"].coordinates.forEach(function(p,i){
								resgml += p[0] + ', ' + p[1] + '\n '
							})
						}
						resgml+="</gml:pos>\n"
						resgml+="</gml:"+feat["geometry"]["type"]+"></the_geom>\n"
					}
					resgml+="</gml:featureMember>"
				}
			}else if("type" in feature && feature["type"]=="Feature"){
				resgml+="<gml:featureMember>"
				if("properties" in feature){
					for(prop in feature["properties"]){
                        ns=shortenURI(prop,true)
                        nsprefix=""
                        if(ns in namespaces && !(ns in nsmap)){
                            nsmap[ns]=namespaces[ns]
                            resgmlhead+="xmlns:"+namespaces[ns]+"=\""+ns+"\" "
                        }
                        if(!(ns in nsmap)){
                            nsmap[ns]="ns"+nscounter
                            nsprefix="ns"+nscounter
                            resgmlhead+="xmlns:"+nsprefix+"=\""+ns+"\" "
                            nscounter+=1
                        }else{
                            nsprefix=nsmap[ns]
                        }
                        if(Array.isArray(feature["properties"][prop])){
							for(arritem of feature["properties"][prop]){
								resgml+="<"+shortenURI(prop,false,nsprefix)+">"+arritem+"</"+shortenURI(prop,false,nsprefix)+">\n"
							}
						}else{
							resgml+="<"+shortenURI(prop,false,nsprefix)+">"+feature["properties"][prop]+"</"+shortenURI(prop,false,nsprefix)+">\n"
						}
				    }
                }
				if("geometry" in feature){
					resgml+="<the_geom><gml:"+feature["geometry"]["type"]+">\n"
					resgml+="<gml:pos>\n"
					if(feature["geometry"]["type"].toUpperCase()=="POINT"){
						resgml += feature["geometry"].coordinates[0] + ' ' + feature["geometry"].coordinates[1]+'\n '
					}else{
						feature["geometry"].coordinates.forEach(function(p,i){
							resgml += p[0] + ', ' + p[1] + '\n '
						})
					}
					resgml+="</gml:pos>\n"
					resgml+="</gml:"+feature["geometry"]["type"]+"></the_geom>\n"
				}
				resgml+="</gml:featureMember>"
            }
		}
	}
	resgml+="</gml:FeatureCollection>"
	saveTextAsFile(resgmlhead+resgml,"gml")
}

function exportKML(){
	reskml="<?xml version=\"1.0\" ?>\n<kml xmlns=\"http://www.opengis.net/kml/2.2\">\n<Document>"
	reskml+="<Style></Style>\n"
	if(typeof(featurecolls)!=="undefined"){
        for(feature of featurecolls){
            if("features" in feature){
                for(feat of feature["features"]){
					reskml+="<Placemark><name>"+feat.id+"</name>"
					if("properties" in feat){
						reskml+="<ExtendedData>"
                        for(prop in feat["properties"]){
                            if(Array.isArray(feat["properties"][prop])){
								for(arritem of feat["properties"][prop]){
									reskml+="<Data name=\""+prop+"\"><displayName>"+shortenURI(prop)+"</displayName><value>"+arritem+"</value></Data>\n"
								}
                            }else{
                                reskml+="<Data name=\""+prop+"\"><displayName>"+shortenURI(prop)+"</displayName><value>"+feat["properties"][prop]+"</value></Data>\n"
                            }
                        }
						reskml+="</ExtendedData>"
                    }
					if("geometry" in feat){
						reskml+="<"+feat["geometry"]["type"]+">\n"
						if(feat["geometry"]["type"]=="Polygon"){
							reskml+="<outerBoundaryIs><LinearRing>"
						}
						reskml+="<coordinates>\n"
						if(feat["geometry"]["type"].toUpperCase()=="POINT"){
							reskml += feat["geometry"].coordinates[0] + ' ' + feat["geometry"].coordinates[1]+'\n '
						}else{
							feat["geometry"].coordinates.forEach(function(p,i){
								reskml += p[0] + ', ' + p[1] + '\n '
							})
						}
						reskml+="</coordinates>\n"
						if(feat["geometry"]["type"]=="Polygon"){
							reskml+="</LinearRing></outerBoundaryIs>"
						}
						reskml+="</"+feat["geometry"]["type"]+">\n"
					}
					reskml+="</Placemark>"
				}
			}else if("type" in feature && feature["type"]=="Feature"){
				reskml+="<Placemark><name>"+feature.id+"</name>"
				if("properties" in feature){
					reskml+="<ExtendedData>"
					for(prop in feature["properties"]){
						if(Array.isArray(feature["properties"][prop])){
							for(arritem of feature["properties"][prop]){
								reskml+="<Data name=\""+prop+"\"><displayName>"+shortenURI(prop)+"</displayName><value>"+arritem+"</value></Data>\n"
							}
						}else{
							reskml+="<Data name=\""+prop+"\"><displayName>"+shortenURI(prop)+"</displayName><value>"+feature["properties"][prop]+"</value></Data>\n"
						}
				    }
					reskml+="</ExtendedData>"
                }
				if("geometry" in feature){
					reskml+="<"+feature["geometry"]["type"]+">\n"
					if(feature["geometry"]["type"]=="Polygon"){
						reskml+="<outerBoundaryIs><LinearRing>"
					}
					reskml+="<coordinates>\n"
					if(feature["geometry"]["type"].toUpperCase()=="POINT"){
						reskml += feature["geometry"].coordinates[0] + ' ' + feature["geometry"].coordinates[1]+'\n '
					}else{
						feature["geometry"].coordinates.forEach(function(p,i){
							reskml += p[0] + ', ' + p[1] + '\n '
						})
					}
					reskml+="</coordinates>\n"
					if(feature["geometry"]["type"]=="Polygon"){
						reskml+="</LinearRing></outerBoundaryIs>"
					}
					reskml+="</"+feature["geometry"]["type"]+">\n"
				}
				reskml+="</Placemark>"
            }
		}
	}
	reskml+="</Document></kml>"
	saveTextAsFile(reskml,"kml")
}

function exportTGFGDF(sepchar,format){
	resgdf=""
	if(format=="gdf")
		resgdf="nodedef>name VARCHAR,label VARCHAR"
    uritoNodeId={}
    nodecounter=0
    nodes=""
    edges=""
    if(typeof(featurecolls)!=="undefined"){
        for(feature of featurecolls){
            if("features" in feature){
                for(feat of feature["features"]){
                    featid=nodecounter
                    uritoNodeId[feat["id"]]=nodecounter
                    nodes+=nodecounter+sepchar+feat["id"]+"\n"
                    nodecounter+=1
                    if("properties" in feat){
                        for(prop in feat["properties"]){
                            if(Array.isArray(feat["properties"][prop])){
                                    for(arritem of feat["properties"][prop]){
                                            if(!(arritem in uritoNodeId)){
                                                uritoNodeId[arritem]=nodecounter
                                                nodes+=nodecounter+sepchar+arritem+"\n"
                                                nodecounter+=1
                                            }
                                            edges+=featid+sepchar+uritoNodeId[arritem]+sepchar+shortenURI(prop)+"\n"
                                    }
                            }else{
                                 if(!(feat["properties"][prop] in uritoNodeId)){
                                    uritoNodeId[feat["properties"][prop]]=nodecounter
                                    nodecounter+=1
                                 }
                                 edges+=featid+sepchar+uritoNodeId[feat["properties"][prop]]+sepchar+shortenURI(prop)+"\n"
                            }
                        }
                    }
                }
            }else if("type" in feature && feature["type"]=="Feature"){
                    featid=nodecounter
                    feat=feature
                    uritoNodeId[feat["id"]]=nodecounter
                    nodes+=nodecounter+sepchar+feat["id"]+"\n"
                    nodecounter+=1
                    if("properties" in feat){
                        for(prop in feat["properties"]){
                            if(Array.isArray(feat["properties"][prop])){
                                    for(arritem of feat["properties"][prop]){
                                            if(!(arritem in uritoNodeId)){
                                                uritoNodeId[arritem]=nodecounter
                                                nodes+=nodecounter+sepchar+arritem+"\n"
                                                nodecounter+=1
                                            }
                                            edges+=featid+sepchar+uritoNodeId[arritem]+sepchar+shortenURI(prop)+"\n"
                                    }
                            }else{
                                 if(!(feat["properties"][prop] in uritoNodeId)){
                                    uritoNodeId[feat["properties"][prop]]=nodecounter
                                    nodecounter+=1
                                 }
                                 edges+=featid+sepchar+uritoNodeId[feat["properties"][prop]]+sepchar+shortenURI(prop)+"\n"
                            }
                      }
                }
            }
        }
    }
    resgdf+=nodes
	if(format=="tgf"){
		resgdf+="#\n"
	}else{
		resgdf+="edgedef>node1 VARCHAR,node2 VARCHAR,label VARCHAR\n"
	}
    resgdf+=edges
	saveTextAsFile(resgdf,format)
}

function setSVGDimensions(){
    $('svg').each(function(i, obj) {
        //console.log(obj)
        //console.log($(obj).children().first()[0])
        if($(obj).attr("viewBox") || $(obj).attr("width") || $(obj).attr("height")){
            return
        }
        maxx=Number.MIN_VALUE
        maxy=Number.MIN_VALUE
        minx=Number.MAX_VALUE
        miny=Number.MAX_VALUE
        $(obj).children().each(function(i){
            svgbbox=$(this)[0].getBBox()
            //console.log(svgbbox)
            if(svgbbox.x+svgbbox.width>maxx){
                maxx=svgbbox.x+svgbbox.width
            }
            if(svgbbox.y+svgbbox.height>maxy){
                maxy=svgbbox.y+svgbbox.height
            }
            if(svgbbox.y<miny){
                miny=svgbbox.y
            }
            if(svgbbox.x<minx){
                minx=svgbbox.x
            }
        });
        //console.log(""+(minx)+" "+(miny-(maxy-miny))+" "+((maxx-minx)+25)+" "+((maxy-miny)+25))
        newviewport=""+((minx))+" "+(miny)+" "+((maxx-minx)+25)+" "+((maxy-miny)+25)
        $(obj).attr("viewBox",newviewport)
        $(obj).attr("width",((maxx-minx))+10)
        $(obj).attr("height",((maxy-miny)+10))
        //console.log($(obj).hasClass("svgoverlay"))
        if($(obj).hasClass("svgoverlay")){
            naturalWidth=$(obj).prev().children('img')[0].naturalWidth
            naturalHeight=$(obj).prev().children('img')[0].naturalHeight
            currentWidth=$(obj).prev().children('img')[0].width
            currentHeight=$(obj).prev().children('img')[0].height
            //console.log(naturalWidth+" - "+naturalHeight+" - "+currentWidth+" - "+currentHeight)
            overlayposX = (currentWidth/naturalWidth) * minx;
            overlayposY = (currentHeight/naturalHeight) * miny;
            overlayposWidth = ((currentWidth/naturalWidth) * maxx)-overlayposX;
            overlayposHeight = ((currentHeight/naturalHeight) * maxy)-overlayposY;
            //console.log(overlayposX+" - "+overlayposY+" - "+overlayposHeight+" - "+overlayposWidth)
            $(obj).css({top: overlayposY+"px", left:overlayposX+"px", position:"absolute"})
            $(obj).attr("height",overlayposHeight)
            $(obj).attr("width",overlayposWidth)
        }
    });
}

function exportGeoURI(){
    resuri=""
    for(point of centerpoints){
		if(typeof(epsg)!=='undefined'){
			resuri+="geo:"+point["lng"]+","+point["lat"]+";crs="+epsg+"\n"
		}else{
			resuri+="geo:"+point["lng"]+","+point["lat"]+";crs=EPSG:4326\n"
		}
    }
    saveTextAsFile(resuri,"geouri")
}


function exportWKT(){
    if(typeof(featurecolls)!=="undefined"){
        reswkt=""
        for(feature of featurecolls){
            if("features" in feature){
                for(feat of feature["features"]){
                    reswkt+=feat["geometry"]["type"].toUpperCase()+"("
                    if(feature["geometry"]["type"].toUpperCase()=="POINT"){
                        reswkt =  reswkt + feature["geometry"].coordinates[0] + ' ' + feature["geometry"].coordinates[1]
                    }else{
                        feature["geometry"].coordinates.forEach(function(p,i){
                            if(i<feature["geometry"].coordinates.length-1) reswkt =  reswkt + p[0] + ' ' + p[1] + ', ';
                            else reswkt =  reswkt + p[0] + ' ' + p[1] + ')';
                        })
                    }
                    reswkt+=")\n"
                }
            }else if("geometry" in feature){
                    reswkt+=feature["geometry"]["type"].toUpperCase()+"("
                    if(feature["geometry"]["type"].toUpperCase()=="POINT"){
                        reswkt =  reswkt + feature["geometry"].coordinates[0] + ' ' + feature["geometry"].coordinates[1]
                    }else{
                        feature["geometry"].coordinates.forEach(function(p,i){
                            if(i<feature["geometry"].coordinates.length-1) reswkt =  reswkt + p[0] + ' ' + p[1] + ', ';
                            else reswkt =  reswkt + p[0] + ' ' + p[1] + ')';
                        })
                    }
                    reswkt+=")\n"
            }
            saveTextAsFile(reswkt,"wkt")
        }
    }
}

function exportXYZASCII(){
    if(typeof(featurecolls)!=="undefined"){
        reswkt=""
        for(feature of featurecolls){
            if("features" in feature){
                for(feat of feature["features"]){
                    if(feature["geometry"]["type"].toUpperCase()=="POINT"){
                        reswkt =  reswkt + feature["geometry"].coordinates[0] + ' ' + feature["geometry"].coordinates[1] + '\n';
                    }else{
                        feature["geometry"].coordinates.forEach(function(p,i){
                            console.log(p)
                            reswkt =  reswkt + p[0] + ' ' + p[1] + '\n';
                        })
                    }
                    reswkt+="\n"
                }
            }else if("geometry" in feature){
                    if(feature["geometry"]["type"].toUpperCase()=="POINT"){
                        reswkt =  reswkt + feature["geometry"].coordinates[0] + ' ' + feature["geometry"].coordinates[1] + '\n';
                    }else{
                        feature["geometry"].coordinates.forEach(function(p,i){
                            console.log(p)
                            reswkt =  reswkt + p[0] + ' ' + p[1] + '\n';
                        })
                    }
                    reswkt+="\n"
            }
            saveTextAsFile(reswkt,"xyz")
        }
    }
}

function downloadFile(filePath){
    var link=document.createElement('a');
    link.href = filePath;
    link.download = filePath.substr(filePath.lastIndexOf('/') + 1);
    link.click();
}

function saveTextAsFile(tosave,fileext){
    var a = document.createElement('a');
    a.style = "display: none";
    var blob= new Blob([tosave], {type:'text/plain'});
    var url = window.URL.createObjectURL(blob);
	var title=$('#title').text()
    var filename = "res."+fileext;
	if(typeof(title)!=='undefined'){
		filename=title.trim()+"."+fileext
	}
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(function(){
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }, 1000);
}

function download(){
    format=$('#format').val()
    if(format=="geojson"){
        exportGeoJSON()
    }else if(format=="ttl"){
        downloadFile(window.location.href.replace(".html",".ttl"))
    }else if(format=="json"){
        downloadFile(window.location.href.replace(".html",".json"))
    }else if(format=="wkt"){
        exportWKT()
    }else if(format=="gml"){
        exportGML()
    }else if(format=="kml"){
        exportKML()
    }else if(format=="csv"){
        exportCSV(",",format)
    }else if(format=="tsv"){
        exportCSV("\t",format)
    }else if(format=="gdf"){
        exportTGFGDF(",",format)
    }else if(format=="graphml"){
        exportGraphML()
    }else if(format=="geouri"){
        exportGeoURI()
    }else if(format=="tgf"){
        exportTGFGDF(" ",format)
    }else if(format=="xyz"){
        exportXYZASCII()
    }else if(format=="latlon"){
        exportLatLonText()
    }
}

function rewriteLink(thelink){
    if(thelink==null){
        rest=search[document.getElementById('search').value].replace(baseurl,"")
    }else{
        curlocpath=window.location.href.replace(baseurl,"")
        rest=thelink.replace(baseurl,"")
    }
    if(!(rest.endsWith("/")) && !(rest.endsWith(".html"))){
        rest+="/"
    }
    count=0
    if(!indexpage){
        count=rest.split("/").length-1
    }
    //console.log(count)
    counter=0
    if (typeof relativedepth !== 'undefined'){
        while(counter<relativedepth){
            rest="../"+rest
            counter+=1
        }
    }else{
        while(counter<count){
            rest="../"+rest
            counter+=1
        }
    }
    //console.log(rest)
    //console.log(rest.endsWith("index.html"))
	if(!rest.includes("nonns_") && !rest.endsWith(".html")){
		rest+="index.html"
	}
    //console.log(rest)
    return rest
}

function followLink(thelink=null){
    rest=rewriteLink(thelink)
    location.href=rest
}

function changeDefLink(){
	$('#formatlink').attr('href',definitionlinks[$('#format').val()]);
}

function changeDefLink2(){
	$('#formatlink2').attr('href',definitionlinks[$('#format2').val()]);
}

var definitionlinks={
    "covjson":"https://covjson.org",
    "csv":"https://tools.ietf.org/html/rfc4180",
    "cipher":"https://neo4j.com/docs/cypher-manual/current/",
    "esrijson":"https://doc.arcgis.com/de/iot/ingest/esrijson.htm",
    "geohash":"http://geohash.org",
    "json":"https://geojson.org",
    "gdf":"https://www.cs.nmsu.edu/~joemsong/software/ChiNet/GDF.pdf",
    "geojsonld":"http://geojson.org/geojson-ld/",
    "geojsonseq":"https://tools.ietf.org/html/rfc8142",
    "geouri":"https://tools.ietf.org/html/rfc5870",
    "gexf":"https://gephi.org/gexf/format/",
    "gml":"https://www.ogc.org/standards/gml",
    "gml2":"https://gephi.org/users/supported-graph-formats/gml-format/",
    "gpx":"https://www.topografix.com/gpx.asp",
    "graphml":"http://graphml.graphdrawing.org",
    "gxl":"http://www.gupro.de/GXL/Introduction/intro.html",
    "hdt":"https://www.w3.org/Submission/2011/03/",
    "hextuples":"https://github.com/ontola/hextuples",
    "html":"https://html.spec.whatwg.org",
    "jsonld":"https://json-ld.org",
    "jsonn":"",
    "jsonp":"http://jsonp.eu",
    "jsonseq":"https://tools.ietf.org/html/rfc7464",
    "kml":"https://www.ogc.org/standards/kml",
    "latlon":"",
    "mapml":"https://maps4html.org/MapML/spec/",
    "mvt":"https://docs.mapbox.com/vector-tiles/reference/",
    "n3":"https://www.w3.org/TeamSubmission/n3/",
    "nq":"https://www.w3.org/TR/n-quads/",
    "nt":"https://www.w3.org/TR/n-triples/",
    "olc":"https://github.com/google/open-location-code/blob/master/docs/specification.md",
    "osm":"https://wiki.openstreetmap.org/wiki/OSM_XML",
    "osmlink":"",
    "rdfxml":"https://www.w3.org/TR/rdf-syntax-grammar/",
    "rdfjson":"https://www.w3.org/TR/rdf-json/",
    "rt":"https://afs.github.io/rdf-thrift/rdf-binary-thrift.html",
    "svg":"https://www.w3.org/TR/SVG11/",
    "tgf":"https://docs.yworks.com/yfiles/doc/developers-guide/tgf.html",
    "tlp":"https://tulip.labri.fr/TulipDrupal/?q=tlp-file-format",
    "trig":"https://www.w3.org/TR/trig/",
    "trix":"https://www.hpl.hp.com/techreports/2004/HPL-2004-56.html",
    "ttl":"https://www.w3.org/TR/turtle/",
    "wkb":"https://www.iso.org/standard/40114.html",
    "wkt":"https://www.iso.org/standard/40114.html",
    "xls":"http://www.openoffice.org/sc/excelfileformat.pdf",
    "xlsx":"http://www.openoffice.org/sc/excelfileformat.pdf",
    "xyz":"https://gdal.org/drivers/raster/xyz.html",
    "yaml":"https://yaml.org"
    }

function shortenURI(uri,getns=false,nsprefix=""){
	prefix=""
	if(typeof(uri)!="undefined"){
		for(namespace in namespaces){
			if(uri.includes(namespaces[namespace])){
				prefix=namespace+":"
				break
			}
		}
		if(prefix=="" && nsprefix!=""){
            prefix==nsprefix
        }
	}
	if(typeof(uri)!= "undefined" && uri.includes("#") && !getns){
		return prefix+uri.substring(uri.lastIndexOf('#')+1)
	}
	if(typeof(uri)!= "undefined" && uri.includes("/") && !getns){
		return prefix+uri.substring(uri.lastIndexOf("/")+1)
	}
    if(typeof(uri)!= "undefined" && uri.includes("#") && getns){
		return prefix+uri.substring(0,uri.lastIndexOf('#'))
	}
	if(typeof(uri)!= "undefined" && uri.includes("/") && getns){
		return prefix+uri.substring(0,uri.lastIndexOf("/"))
	}
	return uri
}


var presenter = null;
function setup3dhop(meshurl,meshformat) {
  presenter = new Presenter("draw-canvas");
  presenter.setScene({
    meshes: {
			"mesh_1" : { url: meshurl}
		},
		modelInstances : {
			"model_1" : {
				mesh  : "mesh_1",
				color : [0.8, 0.7, 0.75]
			}
		}
  });
}

function addRotationControls(box,geometryF,objects){
    geometryF.close();

    const rotationFolder = geometryF.addFolder("Rotation");
    rotationFolder.add(objects.rotation, 'x', 0, Math.PI).name("X").onChange(
    function(){
        yourVar = this.getValue();
        scene.traverse(function(obj){
            if(obj.type === 'Mesh'){
                obj.rotation.x = yourVar;
            }});
    });
    rotationFolder.add(objects.rotation, 'y', 0, Math.PI).name("Y").onChange(
    function(){
        yourVar = this.getValue();
        scene.traverse(function(obj){
            if(obj.type === 'Mesh'){
                obj.rotation.y = yourVar;
            }});
    });
    rotationFolder.add(objects.rotation, 'z', 0, Math.PI).name("Z").onChange(
    function(){
        yourVar = this.getValue();
        scene.traverse(function(obj){
            if(obj.type === 'Mesh'){
                obj.rotation.z = yourVar;
            }});
    });

    const scaleFolder = geometryF.addFolder("Scale");
    scaleFolder.add(objects.scale, 'x', 0, 2).name("X").onChange(
    function(){
        yourVar = this.getValue();
        scene.traverse(function(obj){
            if(obj.type === 'Mesh'){
                obj.scale.x = yourVar;
            }});
    });
    scaleFolder.add(objects.scale, 'y', 0, 2).name("Y").onChange(
    function(){
        yourVar = this.getValue();
        scene.traverse(function(obj){
            if(obj.type === 'Mesh'){
                obj.scale.y = yourVar;
            }});
    });
    scaleFolder.add(objects.scale, 'z', 0, 2).name("Z").onChange(
    function(){
        yourVar = this.getValue();
        scene.traverse(function(obj){
            if(obj.type === 'Mesh'){
                obj.scale.z = yourVar;
            }});
    });
}

function start3dhop(meshurl,meshformat){
    init3dhop();
	setup3dhop(meshurl,meshformat);
	resizeCanvas(640,480);
  	moveToolbar(20,20);
}


function prepareAnnotationFromJSON(verts,annotations){
	var svgShape = new THREE.Shape();
    first=true
    for(vert of verts){
        if(first){
            svgShape.moveTo(vert["x"], vert["y"]);
           first=false
        }else{
            svgShape.lineTo(vert["x"], vert["y"]);
        }
        vertarray.push(vert["x"])
        vertarray.push(vert["y"])
        vertarray.push(vert["z"])
        if(vert["z"]>maxz){
            maxz=vert["z"]
        }
        if(vert["z"]<minz){
            minz=vert["z"]
        }
        if(vert["y"]>maxy){
            maxy=vert["y"]
        }
        if(vert["y"]<miny){
            miny=vert["y"]
        }
        if(vert["x"]>maxx){
            maxx=vert["x"]
        }
        if(vert["x"]<minx){
            minx=vert["x"]
        }
    }
	var extrudedGeometry = new THREE.ExtrudeGeometry(svgShape, {depth: Math.abs(maxz-minz), bevelEnabled: false});
    extrudedGeometry.computeBoundingBox()
    const material = new THREE.MeshBasicMaterial( { color: 0xFFFFFF, wireframe:true } );
    const mesh = new THREE.Mesh( extrudedGeometry, material );
    if(minz<0){
        mesh.position.z = minz;
    }
	annotations.add(mesh)
	return annotations
}

let camera, scene, renderer,controls,axesHelper,box,center,size;

function fitCameraToSelection(camera, controls, selection, fitOffset = 1.2) {
  size = new THREE.Vector3();
  center = new THREE.Vector3();
  box = new THREE.Box3();
  box.makeEmpty();
  for(const object of selection) {
    box.expandByObject(object);
  }

  box.getSize(size);
  box.getCenter(center );

  const maxSize = Math.max(size.x, size.y, size.z);
  const fitHeightDistance = maxSize / (2 * Math.atan(Math.PI * camera.fov / 360));
  const fitWidthDistance = fitHeightDistance / camera.aspect;
  const distance = fitOffset * Math.max(fitHeightDistance, fitWidthDistance);

  const direction = controls.target.clone()
    .sub(camera.position)
    .normalize()
    .multiplyScalar(distance);

  controls.maxDistance = distance * 10;
  controls.target.copy(center);

  if(typeof(camera)!="undefined" && camera!=null){
      camera.near = distance / 100;
      camera.far = distance * 100;
      camera.updateProjectionMatrix();
      camera.position.copy(controls.target).sub(direction);
  }

  controls.update();
}

function addFloatingButtonToMap(mapObject, textForButton, onClickFunction, elementID='mapButton1') {
        // Create the button element with basic dom manipulation
        let buttonElement = document.createElement("button");
        buttonElement.id=elementID

        // Set the innertext and class of the button
        buttonElement.innerHTML = textForButton;
        buttonElement.className = 'leaflet-floating-button';

        // Add this leaflet control
        var buttonControl = L.Control.extend({
          options: {
            // if you wish to edit the position of the button, change the position here and also make the corresponding changes in the css attached below
            position: 'bottomright'
          },

          onAdd: function () {
            var container = L.DomUtil.create('div');
            container.appendChild(buttonElement);
            return container;
          }
        });

        // Add the control to the mapObject
        mapObject.addControl(new buttonControl());

        // The user defined on click action added to the button
        buttonElement.onclick = onClickFunction;
}

function initThreeJS(domelement,verts,meshurls) {
    scene = new THREE.Scene();
    minz=Number.MAX_VALUE
    maxz=Number.MIN_VALUE
    miny=Number.MAX_VALUE
    maxy=Number.MIN_VALUE
    minx=Number.MAX_VALUE
    maxx=Number.MIN_VALUE
	vertarray=[]
    annotations=new THREE.Group();
	const objects=new THREE.Group();
    console.log(verts)
    var svgShape = new THREE.Shape();
    first=true
    height=500
    width=480
    annotations=prepareAnnotationFromJSON(verts,annotations)
    const gui = new dat.GUI({autoPlace: false})
	gui.domElement.id="gui"
    $("#threejsnav").append($(gui.domElement))
	const geometryFolder = gui.addFolder("Mesh");
	geometryFolder.open();
	const lightingFolder = geometryFolder.addFolder("Lighting");
	const geometryF = geometryFolder.addFolder("Geometry");
	geometryF.open();
    renderer = new THREE.WebGLRenderer( { antialias: false } );
	renderer.setPixelRatio( window.devicePixelRatio );
    renderer.setSize( width, height);
    document.getElementById(domelement).appendChild( renderer.domElement );
    bbox=null
    if(meshurls.length>0){
        if(meshurls[0].includes(".ply")){
            var loader = new THREE.PLYLoader();
            loader.load(meshurls[0], function(object){
                const material = new THREE.MeshPhongMaterial({
                    color: 0xffffff,
                    flatShading: true,
                    vertexColors: THREE.VertexColors,
                    wireframe: false
                });
                const mesh = new THREE.Mesh(object, material);
                objects.add(mesh);
                scene.add(objects);
                addRotationControls(object,geometryF,objects)
                if(objects.children.length>0 && typeof(camera)!=="undefined" && camera!=null){
                    camera.lookAt( objects.children[0].position );
                }
                fitCameraToSelection(camera, controls, objects.children)
            });
        }else if(meshurls[0].includes(".obj")){
            var loader= new THREE.OBJLoader();
            loader.load(meshurls[0],function ( object ) {objects.add(object);scene.add(objects); addRotationControls(object,geometryF,objects);if(objects.children.length>0){camera.lookAt( objects.children[0].position );}fitCameraToSelection(camera, controls, objects.children) })
        }else if(meshurls[0].includes(".nxs") || meshurls[0].includes(".nxz")){
            var nexus_obj=new NexusObject(meshurls[0],function(){},renderNXS,renderer);
            objects.add(nexus_obj)
            scene.add(objects);
            addRotationControls(nexus_obj,geometryF,objects)
            /*if(objects.children.length>0){
                camera.lookAt( objects.children[0].position );
            }
            fitCameraToSelection(camera, controls, objects.children)*/
        }else if(meshurls[0].includes(".gltf")){
            var loader = new THREE.GLTFLoader();
            loader.load(meshurls[0], function ( gltf )
            {
                box = gltf.scene;
                box.position.x = 0;
                box.position.y = 0;
                objects.add(box)
                scene.add(objects);
                addRotationControls(box,geometryF,objects)
                if(objects.children.length>0){
                    camera.lookAt( objects.children[0].position );
                }
                fitCameraToSelection(camera, controls, objects.children)
            });
        }
    }
    //camera = new THREE.PerspectiveCamera(90,window.innerWidth / window.innerHeight, 0.1, 150 );
    camera = new THREE.PerspectiveCamera(90,width / height, 0.1, 2000 );
    scene.add(new THREE.AmbientLight(0x222222));
    var light = new THREE.DirectionalLight(0xffffff, 1);
    light.position.set(20, 20, 0);
    scene.add(light);
    lightingFolder.add(light.position, "x").min(-5).max(5).step(0.01).name("X Position")
	lightingFolder.add(light.position, "y").min(-5).max(5).step(0.01).name("Y Position")
	lightingFolder.add(light.position, "z").min(-5).max(5).step(0.01).name("Z Position")
    axesHelper = new THREE.AxesHelper( Math.max(1000, 1000, 1000) );
    scene.add( axesHelper );
    console.log("Depth: "+(maxz-minz))
    scene.add( annotations );
	centervec=new THREE.Vector3()
    controls = new THREE.OrbitControls( camera, renderer.domElement );
    //controls.target.set( centervec.x,centervec.y,centervec.z );
    controls.target.set( 0,0,0 );
    camera.position.x= 0
    camera.position.y= 0
    camera.position.z = 150;
    controls.maxDistance= Math.max(1000, 1000, 1000)
    controls.update();
    const updateCamera = () => {
		camera.updateProjectionMatrix();
	}
	const cameraFolder = geometryFolder.addFolder("Camera");
	cameraFolder.add(camera, 'fov', 1, 180).name('Zoom').onChange(updateCamera);
    cameraFolder.add(camera.position, 'x').min(-500).max(500).step(5).name("X Position").onChange(updateCamera);
    cameraFolder.add(camera.position, 'y').min(-500).max(500).step(5).name("Y Position").onChange(updateCamera);
    cameraFolder.add(camera.position, 'z').min(-500).max(500).step(5).name("Z Position").onChange(updateCamera);
    gui.add(objects, 'visible').name('Meshes')
    gui.add(annotations, 'visible').name('Annotations')
    gui.add(axesHelper, 'visible').name('Axis Helper')
    gui.add({"FullScreen":toggleFullScreen2}, 'FullScreen')
    document.addEventListener("fullscreenchange",function(){
        if(document.fullscreenElement){
            camera.aspect = width / height;
            camera.updateProjectionMatrix();
            renderer.setSize( width, height );
        }
    })
    if(meshurls.length>0 && (meshurls[0].includes(".nxs") || meshurls[0].includes(".nxz"))){
        renderNXS()
    }
    animate()
}

function renderNXS(){
    console.log(renderer)
    Nexus.beginFrame(renderer.getContext());
    renderer.render( scene, camera );
    Nexus.endFrame(renderer.getContext());
}

function animate() {
    requestAnimationFrame( animate );
    controls.update();
    renderer.render( scene, camera );
}

function getTextAnnoContext(){
$('span.textanno').each(function(i, obj) {
    startindex=$(obj).attr("start").val()
    endindex=$(obj).attr("end").val()
    exact=$(obj).attr("exact").val()
    if($(obj).attr("src")){
        source=$(obj).attr("src").val()
        $.get( source, function( data ) {
            markarea=data.substring(start,end)
            counter=0
            startindex=0
            endindex=data.indexOf("\\n",end)
            for(line in data.split("\\n")){
                counter+=line.length
                if(counter>start){
                    startindex=counter-line.length
                    break
                }
            }
            $(obj).html(data.substring(startindex,endindex)+"</span>".replace(markarea,"<mark>"+markarea+"</mark>"))
        });
    }
  });
}

function labelFromURI(uri,label){
    if(uri.includes("#")){
        prefix=uri.substring(0,uri.lastIndexOf('#')-1)
        if(label!=null){
            return label+" ("+prefix.substring(prefix.lastIndexOf("/")+1)+":"+uri.substring(uri.lastIndexOf('#')+1)+")"

        }else{
            return uri.substring(uri.lastIndexOf('#')+1)+" ("+prefix.substring(uri.lastIndexOf("/")+1)+":"+uri.substring(uri.lastIndexOf('#')+1)+")"
        }
    }
    if(uri.includes("/")){
        prefix=uri.substring(0,uri.lastIndexOf('/')-1)
        if(label!=null){
            return label+" ("+prefix.substring(prefix.lastIndexOf("/")+1)+":"+uri.substring(uri.lastIndexOf('/')+1)+")"
        }else{
            return uri.substring(uri.lastIndexOf('/')+1)+" ("+prefix.substring(uri.lastIndexOf("/")+1)+":"+uri.substring(uri.lastIndexOf('/')+1)+")"
        }
    }
    return uri
}

function formatHTMLTableForPropertyRelations(propuri,result,propicon){
    dialogcontent="<h3><img src=\""+propicon+"\" height=\"25\" width=\"25\" alt=\"Instance\"/><a href=\""+propuri.replace('/index.json','/index.html')+"\" target=\"_blank\"> "+shortenURI(propuri)+"</a></h3><table border=1 id=classrelationstable><thead><tr><th>Incoming Concept</th><th>Relation</th><th>Outgoing Concept</th></tr></thead><tbody>"
    //console.log(result)
    if("from" in result) {
        for (instance in result["from"]) {
//
            if (result["from"][instance] == "instancecount") {
                continue;
            }
            dialogcontent += "<tr><td><img onclick=\"getClassRelationDialog($('#jstree').jstree(true).get_node('" + result["from"][instance] + "'))\" src=\"" + iconprefix + "class.png\" height=\"25\" width=\"25\" alt=\"Class\"/><a href=\"" + result["from"][instance] + "\" target=\"_blank\">" + shortenURI(result["from"][instance]) + "</a></td>"
            dialogcontent += "<td><img src=\"" + propicon + "\" height=\"25\" width=\"25\" alt=\"Instance\"/><a href=\"" + propuri + "\" target=\"_blank\">" + shortenURI(propuri) + "</a></td><td></td></tr>"
            // }
        }
    }
    if("to" in result) {
        for (instance in result["to"]) {
            //for(instance in result["to"][res]){
            if (result["to"][instance] == "instancecount") {
                continue;
            }
            dialogcontent += "<tr><td></td><td><img src=\"" + propicon + "\" height=\"25\" width=\"25\" alt=\"Class\"/><a href=\"" + propuri + "\" target=\"_blank\">" + shortenURI(propuri) + "</a></td>"
            dialogcontent += "<td><img onclick=\"getClassRelationDialog($('#jstree').jstree(true).get_node('" + result["to"][instance] + "'))\" src=\"" + iconprefix + "class.png\" height=\"25\" width=\"25\" alt=\"Instance\"/><a href=\"" + result["to"][instance] + "\" target=\"_blank\">" + shortenURI(result["to"][instance]) + "</a></td></tr>"
            // }
        }
    }
    dialogcontent+="</tbody></table>"
    dialogcontent+="<button style=\"float:right\" id=\"closebutton\" onclick='document.getElementById(\"classrelationdialog\").close()'>Close</button>"
    return dialogcontent
}

function determineTableCellLogo(uri){
    result="<td>"
    logourl=""
    finished=false
    if(uri in labelproperties){
        result+="<img onclick=\"getPropRelationDialog('"+uri+"','"+iconprefix+"labelproperty.png')\"  src=\""+iconprefix+"labelproperty.png\" height=\"25\" width=\"25\" alt=\"Label Property\"/>"
        logourl=iconprefix+"labelproperty.png"
        finished=true
    }
    if(!finished){
        for(ns in annotationnamespaces){
            if(uri.includes(annotationnamespaces[ns])){
                result+="<img onclick=\"getPropRelationDialog('"+uri+"','"+iconprefix+"annotationproperty.png')\" src=\""+iconprefix+"annotationproperty.png\" height=\"25\" width=\"25\" alt=\"Annotation Property\"/>"
                logourl=iconprefix+"annotationproperty.png"
                finished=true
            }
        }
    }
    if(!finished && uri in geoproperties && geoproperties[uri]=="ObjectProperty"){
        result+="<img onclick=\"getPropRelationDialog('"+uri+"','"+iconprefix+"geoobjectproperty.png')\" src=\""+iconprefix+"geoobjectproperty.png\" height=\"25\" width=\"25\" alt=\"Geo Object Property\"/>"
        logourl=iconprefix+"geoobjectproperty.png"
    }else if(!finished && uri in geoproperties && geoproperties[uri]=="DatatypeProperty"){
        result+="<img onclick=\"getPropRelationDialog('"+uri+"','"+iconprefix+"geodatatypeproperty.png')\" src=\""+iconprefix+"geodatatypeproperty.png\" height=\"25\" width=\"25\" alt=\"Geo Datatype Property\"/>"
        logourl=iconprefix+"geodatatypeproperty.png"
    }else if(!finished){
        result+="<img onclick=\"getPropRelationDialog('"+uri+"','"+iconprefix+"objectproperty.png')\" src=\""+iconprefix+"objectproperty.png\" height=\"25\" width=\"25\" alt=\"Object Property\"/>"
        logourl=iconprefix+"objectproperty.png"
    }
    result+="<a href=\""+uri+"\" target=\"_blank\">"+shortenURI(uri)+"</a></td>"
    return [result,logourl]
}

function formatHTMLTableForClassRelations(result,nodeicon,nodelabel,nodeid){
    dialogcontent=""
    if(nodelabel.includes("[")){
        nodelabel=nodelabel.substring(0,nodelabel.lastIndexOf("[")-1)
    }
    dialogcontent="<h3><img src=\""+nodeicon+"\" height=\"25\" width=\"25\" alt=\"Instance\"/><a href=\""+nodeid.replace('/index.json','/index.html')+"\" target=\"_blank\"> "+nodelabel+"</a></h3><table border=1 id=classrelationstable><thead><tr><th>Incoming Concept</th><th>Incoming Relation</th><th>Concept</th><th>Outgoing Relation</th><th>Outgoing Concept</th></tr></thead><tbody>"
    if("from" in result) {
        for (res in result["from"]) {
            for (instance in result["from"][res]) {
                if (instance == "instancecount") {
                    continue;
                }
                dialogcontent += "<tr><td><img onclick=\"getClassRelationDialog($('#jstree').jstree(true).get_node('" + instance + "'))\" src=\"" + iconprefix + "class.png\" height=\"25\" width=\"25\" alt=\"Class\"/><a href=\"" + instance + "\" target=\"_blank\">" + shortenURI(instance) + "</a></td>"
                dialogcontent += determineTableCellLogo(res)[0]
                dialogcontent += "<td><img onclick=\"getClassRelationDialog($('#jstree').jstree(true).get_node('" + nodeid + "'))\" src=\"" + nodeicon + "\" height=\"25\" width=\"25\" alt=\"Instance\"/><a href=\"" + nodeid + "\" target=\"_blank\">" + nodelabel + "</a></td><td></td><td></td></tr>"
            }
        }
    }
    if("to" in result) {
        for (res in result["to"]) {
            for (instance in result["to"][res]) {
                if (instance == "instancecount") {
                    continue;
                }
                dialogcontent += "<tr><td></td><td></td><td><img onclick=\"getClassRelationDialog($('#jstree').jstree(true).get_node('" + nodeid + "'))\" src=\"" + nodeicon + "\" height=\"25\" width=\"25\" alt=\"Instance\"/><a href=\"" + nodeid + "\" target=\"_blank\">" + nodelabel + "</a></td>"
                dialogcontent += determineTableCellLogo(res)[0]
                dialogcontent += "<td><img onclick=\"getClassRelationDialog($('#jstree').jstree(true).get_node('" + instance + "'))\" src=\"" + iconprefix + "class.png\" height=\"25\" width=\"25\" alt=\"Class\"/><a href=\"" + instance + "\" target=\"_blank\">" + shortenURI(instance) + "</a></td></tr>"
            }
        }
    }
    dialogcontent+="</tbody></table>"
    dialogcontent+="<button style=\"float:right\" id=\"closebutton\" onclick='document.getElementById(\"classrelationdialog\").close()'>Close</button>"
    return dialogcontent
}

listthreshold=5

function formatHTMLTableForResult(result,nodeicon,nodetype){
    dialogcontent=""
    dialogcontent="<h3><img src=\""+nodeicon+"\" height=\"25\" width=\"25\" alt=\"Instance\"/><a href=\""+nodeid.replace('/index.json','/index.html')+"\" target=\"_blank\"> "+nodelabel+"</a></h3><table border=1 id=dataschematable><thead><tr><th>Type</th><th>Relation</th><th>Value</th></tr></thead><tbody>"
    for(res in result){
        /*console.log(result)
        console.log(result[res])
        console.log(result[res].size)*/
        dialogcontent+="<tr>"
        detpropicon=""
        if(res in geoproperties && geoproperties[res]=="ObjectProperty"){
            dialogcontent+="<td><img src=\""+iconprefix+"geoobjectproperty.png\" height=\"25\" width=\"25\" alt=\"Geo Object Property\"/>Geo Object Property</td>"
            detpropicon=iconprefix+"geoobjectproperty.png"
        }else if((result[res][0]+"").startsWith("http")){
            dialogcontent+="<td><img src=\""+iconprefix+"objectproperty.png\" height=\"25\" width=\"25\" alt=\"Object Property\"/>Object Property</td>"
            detpropicon=iconprefix+"objectproperty.png"
        }else{
            finished=false
            ress=determineTableCellLogo(res)
            dialogcontent+=ress[0]
            detpropicon=ress[1]
        }
        dialogcontent+="<td><a href=\""+res+"\" target=\"_blank\">"+shortenURI(res)+"</a> <a href=\"#\" onclick=\"getPropRelationDialog('"+res+"','"+detpropicon+"')\">[x]</a></td>"
        if(Object.keys(result[res]).length>1){
            dialogcontent+="<td>"
            if(result[res].length>listthreshold){
                dialogcontent+="<details><summary>"+result[res].length+" values</summary>"
            }
            dialogcontent+="<ul>"
            for(resitem in result[res]){
                if(!(nodetype.includes("class"))) {
                    if ((result[res][resitem] + "").trim().startsWith("http")) {
                        dialogcontent += "<li><a href=\"" + rewriteLink(result[res][resitem]) + "\" target=\"_blank\">" + shortenURI(result[res][resitem]) + "</a></li>"
                    } else if (resitem != "instancecount") {
                        dialogcontent += "<li>" + result[res][resitem] + "</li>"
                    }
                }else{
                    if ((resitem+ "").trim().startsWith("http")) {
                        dialogcontent += "<li><a href=\"" + rewriteLink(resitem) + "\" target=\"_blank\">" + shortenURI(resitem) + "</a> [" + result[res][resitem] + "]</li>"
                    } else if (resitem != "instancecount") {
                        dialogcontent += "<li>" + result[res][resitem] + "</li>"
                    }
                }
            }
            dialogcontent+="</ul>"
            if(result[res].length>listthreshold){
                dialogcontent+="</details>"
            }
            dialogcontent+="</td>"
        }else if((Object.keys(result[res])[0]+"").startsWith("http") || (result[res][Object.keys(result[res])[0]]+"").startsWith("http")){
            if(!(nodetype.includes("class"))) {
                dialogcontent+="<td><a href=\""+rewriteLink(result[res][Object.keys(result[res])[0]]+"")+"\" target=\"_blank\">"+shortenURI(result[res][Object.keys(result[res])[0]]+"")+"</a></td>"
            }else{
                dialogcontent+="<td><a href=\""+rewriteLink(Object.keys(result[res])[0]+"")+"\" target=\"_blank\">"+shortenURI(Object.keys(result[res])[0]+"")+"</a></td>"
            }
        }else if(Object.keys(result[res])[0]!="instancecount"){
            if(!(nodetype.includes("class"))) {
                dialogcontent += "<td>" + result[res][Object.keys(result[res])[0]] + "</td>"
            }else{
                dialogcontent += "<td>" + Object.keys(result[res])[0] + "</td>"
            }
        }else{
            dialogcontent+="<td></td>"
        }
        dialogcontent+="</tr>"
    }
    dialogcontent+="</tbody></table>"
    dialogcontent+="<button style=\"float:right\" id=\"closebutton\" onclick='document.getElementById(\"dataschemadialog\").close()'>Close</button>"
    return dialogcontent
}

function getClassRelationDialog(node){
     nodeid=rewriteLink(normalizeNodeId(node)).replace(".html",".json")
     nodelabel=node.text
     nodetype=node.type
     nodeicon=node.icon
     props={}
     if("data" in node){
        props=node.data
     }
     console.log(nodetype)
     if(nodetype=="class" || nodetype=="geoclass" || nodetype=="collectionclass" || nodetype=="halfgeoclass"){
        console.log(props)
        dialogcontent=formatHTMLTableForClassRelations(props,nodeicon,nodelabel,nodeid)
        document.getElementById("classrelationdialog").innerHTML=dialogcontent
        $('#classrelationstable').DataTable();
        document.getElementById("classrelationdialog").showModal();
     }
}

function getPropRelationDialog(propuri,propicon){
     dialogcontent=formatHTMLTableForPropertyRelations(propuri,proprelations[propuri],propicon)
     console.log(dialogcontent)
     document.getElementById("classrelationdialog").innerHTML=dialogcontent
     $('#classrelationstable').DataTable();
     document.getElementById("classrelationdialog").showModal();
}

function normalizeNodeId(node){
    if(node.id.includes("_suniv")){
        return node.id.replace(/_suniv[0-9]+_/, "")
    }
    return node.id
}

function getDataSchemaDialog(node){
     nodeid=rewriteLink(normalizeNodeId(node)).replace(".html",".json")
     nodelabel=node.text
     nodetype=node.type
     nodeicon=node.icon
     props={}
     if("data" in node){
        props=node.data
     }
     console.log(nodetype)
     if(nodetype=="class" || nodetype=="halfgeoclass" || nodetype=="geoclass" || node.type=="collectionclass"){
        console.log(props)
        dialogcontent=formatHTMLTableForResult(props["to"],nodeicon,nodetype)
        document.getElementById("dataschemadialog").innerHTML=dialogcontent
        $('#dataschematable').DataTable();
        document.getElementById("dataschemadialog").showModal();
     }else{
         $.getJSON(nodeid, function(result){
            dialogcontent=formatHTMLTableForResult(result,nodeicon,nodetype)
            document.getElementById("dataschemadialog").innerHTML=dialogcontent
            $('#dataschematable').DataTable();
            document.getElementById("dataschemadialog").showModal();
          });
    }
}

iconprefix="https://cdn.jsdelivr.net/gh/i3mainz/geopubby@master/public/icons/"

function setupJSTree(){
    console.log("setupJSTree")
	if(iconprefixx!=""){
		iconprefix=iconprefixx
	}
    tree["contextmenu"]={}
    tree["core"]["check_callback"]=true
    tree["sort"]=function(a, b) {
        a1 = this.get_node(a);
        b1 = this.get_node(b);
        if (a1.icon == b1.icon){
            return (a1.text > b1.text) ? 1 : -1;
        } else {
            return (a1.icon > b1.icon) ? 1 : -1;
        }
    }
	tree["types"]={
            "default": {"icon": iconprefix+"instance.png"},
            "class": {"icon": iconprefix+"class.png"},
            "geoclass": {"icon": iconprefix+"geoclass.png","valid_children":["class","halfgeoclass","geoclass","geoinstance"]},
            "halfgeoclass": {"icon": iconprefix+"halfgeoclass.png"},
            "collectionclass": {"icon": iconprefix+"collectionclass.png"},
            "geocollection": {"icon": iconprefix+"geometrycollection.png"},
            "featurecollection": {"icon": iconprefix+"featurecollection.png"},
            "instance": {"icon": iconprefix+"instance.png"},
            "geoinstance": {"icon": iconprefix+"geoinstance.png"}
    }
    tree["contextmenu"]["items"]=function (node) {
        nodetype=node.type
        thelinkpart="class"
        if(nodetype=="instance" || nodetype=="geoinstance"){
            thelinkpart="instance"
        }
        contextmenu={
            "lookupdefinition": {
                "separator_before": false,
                "separator_after": false,
                "label": "Lookup definition",
                "icon": iconprefix+"searchclass.png",
                "action": function (obj) {
                    newlink=normalizeNodeId(node)
                    var win = window.open(newlink, '_blank');
                    win.focus();
                }
            },
            "copyuriclipboard":{
                "separator_before": false,
                "separator_after": false,
                "label": "Copy URI to clipboard",
                "icon": iconprefix+thelinkpart+"link.png",
                "action":function(obj){
                    copyText=normalizeNodeId(node)
                    navigator.clipboard.writeText(copyText);
                }
            },
            "discoverrelations":{
                "separator_before": false,
                "separator_after": false,
                "label": "Discover "+node.type+" relations",
                "icon": iconprefix+thelinkpart+"link.png",
                "action":function(obj){
                    console.log("class relations")
                    if(node.type=="class" || node.type=="halfgeoclass" || node.type=="geoclass" || node.type=="collectionclass"){
                        getClassRelationDialog(node)
                    }
                }
            },
            "loaddataschema": {
                "separator_before": false,
                "separator_after": false,
                "icon": iconprefix+node.type+"schema.png",
                "label": "Load dataschema for "+node.type,
                "action": function (obj) {
                    /*console.log(node)
                    console.log(node.id)
                    console.log(baseurl)*/
                    if(node.id.includes(baseurl)){
                        getDataSchemaDialog(node)
                    }else if(node.type=="class" || node.type=="halfgeoclass" || node.type=="geoclass" || node.type=="collectionclass"){
                        getDataSchemaDialog(node)
                    }
                }
            }
        }
        return contextmenu
    }
    $('#jstree').jstree(tree);
    $('#jstree').bind("dblclick.jstree", function (event) {
        var node = $(event.target).closest("li");
        var data = node[0].id
        if(data.includes(baseurl)){
            //console.log(node[0].id)
            //console.log(normalizeNodeId(node[0]))
            followLink(normalizeNodeId(node[0]))
        }else{
            window.open(data, '_blank');
        }
    });
    var to = false;
	$('#classsearch').keyup(function () {
        if(to) { clearTimeout(to); }
        to = setTimeout(function () {
            var v = $('#classsearch').val();
            $('#jstree').jstree(true).search(v,false,true);
        });
    });
}

function toggleFullScreen2(){
    toggleFullScreen("threejs",true)
}

function toggleFullScreen(elementid,threejs=false) {
  if (!document.fullscreenElement) {
    document.getElementById(elementid).requestFullscreen();
    if(threejs){
        var elem = document.getElementById(elementid);
        var sceneWidth = window.innerWidth;
        var sceneHeight = elem.offsetHeight;
        camera.aspect = sceneWidth / sceneHeight;
        camera.updateProjectionMatrix();
        renderer.setSize( sceneWidth, sceneHeight );
    }
  } else if (document.exitFullscreen) {
    document.exitFullscreen();
  }
}

function restyleLayer(propertyName,geojsonLayer) {
    //geojsonLayer.eachLayer(function(featureInstanceLayer) {
    propertyValue = geojsonLayer["features"][0]["properties"][propertyName];
    rangesByAttribute=createColorRangeByAttribute(propertyName,geojsonLayer)
    //console.log(rangesByAttribute)
    document.getElementById("legend").innerHTML=rangestoLegendHTML(rangesByAttribute)
    // Your function that determines a fill color for a particular
    // property name and value.
    //console.log(layerr)
    layerr.eachLayer(function(layer) {
        //console.log(layer)
        thecolor=getColor(layer.feature, propertyName, layer.feature.properties[propertyName], rangesByAttribute)
        //console.log(thecolor)
        if( layer instanceof L.Marker ) {
            //console.log("Is Marker")
            layer.setIcon(L.divIcon({
                className: "my-custom-pin",
                iconAnchor: [0, 24],
                labelAnchor: [-6, 0],
                popupAnchor: [0, -36],
                html: "<span id=\"feature\" style=\"background-color: "+thecolor+";width: 1.5rem;height: 1.5rem;display: block;left: -1rem;top: 0rem;position: relative;border-radius: 3rem 3rem 0;transform: rotate(45deg);border: 1px solid #FFFFFF;\"></span>"
            }))
        }else{
            //console.log("No Marker")
            layer.setStyle({
                fillColor: thecolor,
                color: thecolor,
                fillOpacity:0.8,
                weight:2
            })
        }
    });
}


function rangestoLegendHTML(rangesByAttribute){
    result="<table style=\"border: 1px solid;background-color:#d3d3d3\">"
    //console.log(rangesByAttribute)
    for(rang in rangesByAttribute){
        //console.log(rang)
        for(therange of rangesByAttribute[rang]){
             result+="<tr><td><span style=\"width: 20px;height: 20px;border: 5px solid rgba(0, 0, 0, .2);background-color:"+therange["color"]+"\"></span>"
            if("min" in therange && "max" in therange){
                result+=therange["min"]+" <b>-</b> "+therange["max"]
            }else{
                result+=therange["label"]
            }
            result+="</td>"
        }

    }
    //console.log(result)
    result+="</table>"
    return result
}

colors=["#a6cee3","#1f78b4","#b2df8a","#33a02c","#fb9a99","#e31a1c","#fdbf6f","#ff7f00","#cab2d6","#6a3d9a","#ffff99","#b15928"]

function getColor(feature,propertyName,propertyValue,rangesByAttribute){
    if(propertyName=="None"){
        return "#000000"
    }
    if(!isNaN(propertyValue) && propertyName in rangesByAttribute){
        propNum=Number(propertyValue)
        for(therange of rangesByAttribute[propertyName]){
            if("min" in therange && "max" in therange){
                if(propNum>=therange["min"] && propNum<=therange["max"]){
                    //console.log("COLOR FOUND: "+propertyValue+" ["+therange["min"]+","+therange["max"]+"]: "+therange["color"])
                    return therange["color"];
                }
            }
        }
    }else{
        if(propertyName in rangesByAttribute) {
            for (rang of rangesByAttribute[propertyName]) {
                if (rang["label"] == propertyValue) {
                    return rang["color"]
                }
            }
        }
    }
    return "#000000"
}




function createColorRangeByAttribute(propertyName,geojsonlayer){
    var valueset={}
    var minamount=999999,maxamount=-999999
    var amountofrelevantitems=0
    var stringitems=0
    var numberitems=0
    //var amountofitems=geojsonlayer.size()
    var maxColors=8
    rangesByAttribute={}
    for(feat of geojsonlayer["features"]){
        if(propertyName in feat["properties"]){
            if(!(feat["properties"][propertyName] in valueset)){
                valueset[feat["properties"][propertyName]]=0
            }
            valueset[feat["properties"][propertyName]]+=1
            if(isNaN(feat["properties"][propertyName])){
                stringitems+=1
            }else{
                numberitems+=1
                numb=Number(feat["properties"][propertyName])
                if(numb<minamount){
                    minamount=numb
                }
                if(numb>maxamount){
                    maxamount=numb
                }
            }
            amountofrelevantitems+=1
        }else{
            if(!("undefined" in valueset)){
                valueset["undefined"]=0
            }
            valueset["undefined"]+=1
        }
    }
    rangesByAttribute[propertyName]=[]
    if(numberitems===amountofrelevantitems){
        myrange=maxamount-minamount
        myrangesteps=myrange/maxColors
        curstep=minamount
        stepcounter=0
        while(curstep<maxamount){
            curstepstr=(curstep+"")
            rangesByAttribute[propertyName].push({"min":curstep,"max":curstep+myrangesteps,"label":"["+curstep+" - "+(curstep+myrangesteps)+"]","color":colors[stepcounter%12]})
            curstep+=myrangesteps
            stepcounter+=1
        }
    }else if(stringitems<amountofrelevantitems){
        stepcounter=0
        for(item in valueset){
            rangesByAttribute[propertyName].push({"label":item,"color":colors[stepcounter%12]})
            stepcounter+=1
        }
    }else{
        stepcounter=0
        for(item in valueset){
            rangesByAttribute[propertyName].push({"label":item,"color":colors[stepcounter%12]})
            stepcounter+=1
        }
    }
    //console.log(rangesByAttribute)
    return rangesByAttribute
}

function generateLeafletPopup(feature, layer){
    var popup="<b>"
    if("name" in feature && feature.name!=""){
        popup+="<a href=\""+rewriteLink(feature.id)+"\" class=\"footeruri\" target=\"_blank\">"+feature.name+"</a></b><br/><ul>"
    }else{
        popup+="<a href=\""+rewriteLink(feature.id)+"\" class=\"footeruri\" target=\"_blank\">"+feature.id.substring(feature.id.lastIndexOf('/')+1)+"</a></b><br/><ul>"
    }
    for(prop in feature.properties){
        popup+="<li>"
        if(prop.startsWith("http")){
            if(prop.includes("#")){
               popup+="<a href=\""+prop+"\" target=\"_blank\">"+prop.substring(prop.lastIndexOf('#')+1)+"</a>"
            }else{
               popup+="<a href=\""+prop+"\" target=\"_blank\">"+prop.substring(prop.lastIndexOf('/')+1)+"</a>"
            }
        }else{
            popup+=prop
        }
        popup+=" : "
        if(Array.isArray(feature.properties[prop]) && feature.properties[prop].length>1){
            popup+="<ul>"
            for(item of feature.properties[prop]){
                popup+="<li>"
                if((item+"").startsWith("http")){
                    if((item+"").includes("#")){
                        popup+="<a href=\""+item+"\" target=\"_blank\">"+item.substring(item.lastIndexOf('#')+1)+"</a>"
                    }else{
                        popup+="<a href=\""+item+"\" target=\"_blank\">"+item.substring(item.lastIndexOf('/')+1)+"</a>"
                    }
                }else{
                    popup+=item
                }
                popup+="</li>"
            }
            popup+="</ul>"
        }else if(Array.isArray(feature.properties[prop]) && (feature.properties[prop][0]+"").startsWith("http")){
            if(feature.properties[prop][0].includes("#")){
              popup+="<a href=\""+rewriteLink(feature.properties[prop][0])+"\" target=\"_blank\">"+feature.properties[prop][0].substring(feature.properties[prop][0].lastIndexOf('#')+1)+"</a>"
            }else{
              popup+="<a href=\""+rewriteLink(feature.properties[prop][0])+"\" target=\"_blank\">"+feature.properties[prop][0].substring(feature.properties[prop][0].lastIndexOf('/')+1)+"</a>"
            }
        }else{
            if((feature.properties[prop]+"").startsWith("http")){
                    if((feature.properties[prop]+"").includes("#")){
                        popup+="<a href=\""+(feature.properties[prop]+"")+"\" target=\"_blank\">"+(feature.properties[prop]+"").substring((feature.properties[prop]+"").lastIndexOf('#')+1)+"</a>"
                    }else{
                        popup+="<a href=\""+(feature.properties[prop]+"")+"\" target=\"_blank\">"+(feature.properties[prop]+"").substring((feature.properties[prop]+"").lastIndexOf('/')+1)+"</a>"
                    }
            }else{
                popup+=feature.properties[prop]+""
            }
        }
        popup+="</li>"
    }
    popup+="</ul>"
    return popup
}

function fetchLayersFromList(thelist){
	fcolls=[]
	for(url in thelist){
		$.ajax({
			url:thelist[url],
			dataType : 'json',
			async : false,
			success : function(data) {
				fcolls.push(data)
			}
		});
	}
	return fcolls
}

function createDropdownOptions(featurecolls){
    result=new Set()
    for(coll in featurecolls) {
        if ("features" in featurecolls[coll]) {
            for (feat in featurecolls[coll]["features"]) {
                for (prop in featurecolls[coll]["features"][feat]["properties"]) {
                    result.add(prop)
                }
            }
        }else if("properties" in featurecolls[coll]){
            for (prop in coll["properties"]) {
                 result.add(prop)
            }
        }
    }
    if(result.size>0) {
        legendstr="<table>"
        selectstr = "<select id=\"filterdropdown\"><option value=\"\">None</option>"
        for (item of Array.from(result).sort()) {
            if ((item + "").includes("#")) {
                selectstr += "<option value=\"" + item + "\">" + item.substring(item.lastIndexOf('#') + 1) + "</option>"
            } else {
                selectstr += "<option value=\"" + item + "\">" + item.substring(item.lastIndexOf('/') + 1) + "</option>"
            }
        }
        selectstr += "</select><div id=\"legend\"></div>"
        var legend = L.control({position: 'topright'});
        legend.onAdd = function (map) {
            var div = L.DomUtil.create('div', 'info legend');
            div.innerHTML = selectstr;
            div.firstChild.onmousedown = div.firstChild.ondblclick = L.DomEvent.stopPropagation;
            return div;
        };
        legend.addTo(map);
        document.getElementById("filterdropdown").onchange = function () {
            restyleLayer(document.getElementById("filterdropdown").value, featurecolls[coll])
        }
    }
}

var centerpoints=[]
var clustersfrozen=false
var layerr;
var markerlist=[]

function setupLeaflet(baselayers,epsg,baseMaps,overlayMaps,map,featurecolls,dateatt="",ajax=true){
	if(ajax){
		featurecolls=fetchLayersFromList(featurecolls)
	}
    if(typeof (baselayers) === 'undefined' || baselayers===[]){
        basemaps["OSM"]=L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'})
        baseMaps["OSM"].addTo(map);
    }else{
        first=true
        for(bl in baselayers){
            if("type" in baselayers[bl] && baselayers[bl]["type"]==="wms") {
                if("layername" in baselayers[bl]){
                    baseMaps[bl] = L.tileLayer.wms(baselayers[bl]["url"],{"layers":baselayers[bl]["layername"]})
                }else{
                    baseMaps[bl] = L.tileLayer.wms(baselayers[bl]["url"])
                }

            }else if(!("type" in baselayers[bl]) || baselayers[bl]["type"]==="tile"){
                baseMaps[bl]=L.tileLayer(baselayers[bl]["url"])
            }
            if(first) {
                baseMaps[bl].addTo(map);
                first = false
            }
        }
    }
	L.control.scale({
	position: 'bottomright',
	imperial: false
	}).addTo(map);
    L.Polygon.addInitHook(function () {
        this._latlng = this._bounds.getCenter();
    });
    L.Polygon.include({
        getLatLng: function () {
            return this._latlng;
        },
        setLatLng: function () {} // Dummy method.
    });
	var bounds = L.latLngBounds([]);
    first=true
    counter=1
    featcounter=0
    for(feature of featurecolls){
        var markercluster = L.markerClusterGroup.layerSupport({})
        if(epsg!="" && epsg!="EPSG:4326" && epsg in epsgdefs){
            feature=convertGeoJSON(feature,epsgdefs[epsg],null)
        }
        if("features" in feature){
            featcounter+=feature["features"].length
        }else{
            featcounter+=1
        }
        layerr=L.geoJSON.css(feature,{
        pointToLayer: function(feature, latlng){
            greenIcon=L.divIcon({
                className: "my-custom-pin",
                iconAnchor: [0, 24],
                labelAnchor: [-6, 0],
                popupAnchor: [0, -36],
                html: "<span style=\"background-color: black;width: 1.5rem;height: 1.5rem;display: block;left: -1rem;top: 0rem;position: relative;border-radius: 3rem 3rem 0;transform: rotate(45deg);border: 1px solid #FFFFFF;\"></span>"
            })
            themarker=L.marker(latlng, {icon: greenIcon});
            markerlist.push(themarker);
            return themarker
        },onEachFeature: function (feature, layer) {layer.bindPopup(generateLeafletPopup(feature, layer))}})
        layername="Content "+counter
        if("name" in feature) {
            layername = feature["name"]
        }else {
            counter += 1
        }
		markercluster.checkIn(layerr);
        overlayMaps[layername]=L.featureGroup.subGroup(markercluster,[layerr])
        if(first) {
            overlayMaps[layername].addTo(map);
            var layerBounds = layerr.getBounds();
            bounds.extend(layerBounds);
            map.fitBounds(bounds);
            first = false
        }
        centerpoints.push(layerr.getBounds().getCenter());
    }
    //createDropdownOptions(featurecolls)
    addFloatingButtonToMap(map, 'Toggle Clusters', ()=>{
        if(clustersfrozen){
            markercluster.enableClustering()
        }else{
            markercluster.disableClustering()
        }
        clustersfrozen=!clustersfrozen
    }, 'toggleClusters')
    layercontrol=L.control.layers(baseMaps,overlayMaps).addTo(map)
	createDropdownOptions(featurecolls)
    if(featcounter>1 && dateatt!=null && dateatt!="" && dateatt!="[]" && dateatt!=[]){
        let textbox   = L.Control.extend({
            onAdd: function() {
                var text = L.DomUtil.create('div');
                text.id = "info_text";
                text.innerHTML = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                return text;
            }
        });
        new textbox({ position: 'bottomleft' }).addTo(map);
		var sliderControl = L.control.sliderControl({
			position: "bottomleft",
			layer: layerr,
			range: true,
			rezoom: 10,
			showAllOnStart: true,
			timeAttribute: dateatt
		});
        //console.log(sliderControl.options)
		map.addControl(sliderControl);
        sliderControl.options.markers.sort(function (a, b) {
            try{
                return (parseFloat(a.feature.properties[dateatt]) > parseFloat(b.feature.properties[dateatt]));
            }catch(e){
                return (new Date(a.feature.properties[dateatt]) > new Date(b.feature.properties[dateatt]));
            }

        });
		sliderControl.startSlider();
	}
    markercluster.addTo(map)
}
