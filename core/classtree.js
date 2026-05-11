
function generateClassTree(titleattarr, superatt, classOrProp) {
    classTree = {
        "plugins": ["search", "types", "sort", "state", "wholerow"],
        "search": {
            "case_sensitive": false,
            "show_only_matches": true
        },
        "core": {
            "themes":{"responsive":true},
            "data": []
        }
    }
    parentmap = {}
    var topConcept="#"
    if (titleattarr.includes("class")) {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#Thing",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
            "parent": "#",
            "text": "owl:Thing"
        })
        parentmap["http://www.w3.org/2002/07/owl#Thing"]=true
        topConcept="http://www.w3.org/2002/07/owl#Thing"
    } else if (titleattarr.includes("data property") || titleattarr.includes("datatype property")) {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#topDataProperty",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
            "parent": "#",
            "text": "owl:topDataProperty"
        })
        parentmap["http://www.w3.org/2002/07/owl#topDataProperty"]=true
        topConcept="http://www.w3.org/2002/07/owl#topDataProperty"
    } else if (titleattarr.includes("annotation property")) {
        topConcept="#"
    }else if (titleattarr.includes("named individual")) {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#NamedIndividual",
            "parent": "#",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
            "text": "owl:NamedIndividual"
        })
        parentmap["http://www.w3.org/2002/07/owl#NamedIndividual"]=true
        topConcept="http://www.w3.org/2002/07/owl#NamedIndividual"
    } else {
        classTree["core"]["data"].push({
            "id": "http://www.w3.org/2002/07/owl#topObjectProperty",
            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
            "parent": "#",
            "text": "owl:topObjectProperty"
        })
        parentmap["http://www.w3.org/2002/07/owl#topObjectProperty"]=true
        topConcept="http://www.w3.org/2002/07/owl#topObjectProperty"
    }

    var counter = 0;
    //console.log($('#ontview').contents())
    //console.log($('#ontview').contents().find('.type-c'))
    //console.log($('#ontview').contents().find(' h3 > sup[title="'+titleatt+'"]'))
    for(titleatt of titleattarr){
    $('#ontview').contents().find(' h3 > sup[title="' + titleatt + '"]').each(function() {
        //console.log($(this))
        if (counter > 0) {
            var id = $(this).parent().parent().attr("id");
            //console.log(id)
            var parentcls = "";
            if (titleatt == "class") {
                parentcls = "http://www.w3.org/2002/07/owl#Thing"
            } else if (titleatt == "data property") {
                parentcls = "http://www.w3.org/2002/07/owl#topDataProperty"
            } else if (titleatt == "object property") {
                parentcls = "http://www.w3.org/2002/07/owl#topObjectProperty"
            } else if (titleatt == "named individual") {
                parentcls = "http://www.w3.org/2002/07/owl#NamedIndividual"
            }

            //console.log("Superclasses")
            if (!(id.startsWith("4"))) {
                sup = $(this).parent().parent().children('dl').children('dt:contains("' + superatt + '")').next().children("a")
                //console.log("Sup: ")
                //console.log(sup)
                if (sup.length != 0) {
                    sup.each(function() {
                        //console.log($(this))
                        theth=$(this).parent().parent().children("table").children("tbody").children("tr").children("th")
                        uri=$(theth[0]).next().children("code")
                        //console.log("URI Elem: ")
                        //console.log(uri)
                        if(typeof(uri)!=='undefined'){
                            //console.log("URI: ")
                            //console.log(uri.html())
                            if(typeof(uri.html())!='undefined' && uri.html().startsWith("http")){
                                id=uri.html()
                            }                  
                        }
                        
                        //console.log(theth)
                        if(titleatt=="class" && typeof(theth)!=='undefined' && typeof($(theth).next().children("a").attr("href"))!=='undefined'){
                            //console.log($(theth).next().children("a").attr("href"))
                            parentcls=$(theth).next().children("a").attr("href")
                        }else if (!($(this).attr("href").startsWith("4"))) {
                            parentcls = $(this).attr("href")
                            //console.log($(this).attr("href"));
                        }
                    });
                } else {
                    theth=$(this).parent().parent().children("table").children("tbody").children("tr").children("th")
                    if(titleatt=="class" && typeof(theth)!=='undefined'){
                        //console.log(theth[2])
                        //console.log($(theth[2]).next().children("a").attr("href"))
                        uri=$(theth[0]).next().children("code")
                        //console.log("URI Elem: ")
                        //console.log(uri)
                        if(typeof(uri)!=='undefined'){
                            //console.log("URI: ")
                            //console.log(uri.html())
                            if(typeof(uri.html())!='undefined' && uri.html().startsWith("http")){
                                id=uri.html()
                            }                  
                        }
                        theth=$(theth[2]).next().children("a")                        
                        theth.each(function() {        
                            //console.log($(this).attr("href"))
                            parentcls = $(this).attr("href")
                        });
                    }else{
                       $(this).parent().parent().children('div').children('dl').children('dt:contains("' + superatt + '")').next().children("a").each(function() {
                        //console.log($(this))
                        if (!($(this).attr("href").startsWith("4"))) {
                            parentcls = $(this).attr("href")
                            //console.log($(this).attr("href"));
                        }
                    });
                    }

                }
                //console.log(parentcls)
                
                if (parentcls == "") {
                    parentcls = "#"
                }

                ////console.log(superclasslist[0])
                //var topush={ "id" : id,parent:
                if (id.includes('#')) {
                    var textt = id.substring(id.lastIndexOf('#') + 1)
                } else {
                    var textt = id.substring(id.lastIndexOf('/') + 1)
                }
                if (titleatt == "class") {
                    if (id != "http://www.w3.org/2002/07/owl#Thing" && id!="#"){
                       if (!(parentcls in parentmap) && parentcls!="#") {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            treeitem={
                                "id": parentcls,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt2
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[parentcls] = treeitem
                       }
                       if(id==parentcls){
                           treeitem={
                                "id": id,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt
                            }
                           classTree["core"]["data"].push(treeitem)
                           parentmap[id] = treeitem
                       }else if(id in parentmap && parentmap[id]["parent"]==topConcept){
                            parentmap[id]["parent"]=parentcls
                        }else{
                           treeitem={
                                "id": id,
                                "parent": parentcls,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt
                            }
                           classTree["core"]["data"].push(treeitem)
                           parentmap[id] = treeitem
                       }
                       
                    }
                } else if (titleatt == "data property" || titleatt == "datatype property") {
                    if (id != "http://www.w3.org/2002/07/owl#topDataProperty" && id!="#"){
                        if (!(parentcls in parentmap) && parentcls!="#") {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            treeitem={
                                "id": parentcls,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
                                "text": textt2
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[parentcls] = treeitem
                        }
                        if(id==parentcls){
                            treeitem={
                                "id": id,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id] = treeitem
                        }else if(id in parentmap && parentmap[id]["parent"]==topConcept){
                            parentmap[id]["parent"]=parentcls
                        }else{
                            treeitem={
                                "id": id,
                                "parent": parentcls,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLDatatypeProperty.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id] = treeitem
                        }
                        
                    }
                } else if (titleatt == "annotation property") {
                        classTree["core"]["data"].push({
                            "id": id,
                            "parent": "#",
                            "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Metadata.gif",
                            "text": textt
                        })                        
                }else if (titleatt == "named individual") {
                    if (id != "http://www.w3.org/2002/07/owl#NamedIndividual" && id!="#"){
                        if (!(parentcls in parentmap) && parentcls!="#") {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                            treeitem={
                                "id": parentcls,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/Classes.gif",
                                "text": textt2
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[parentcls] = treeitem
                        }
                        if(id==parentcls){
                            treeitem={
                                "id": id,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id] = treeitem
                        }else if(id in parentmap && parentmap[id]["parent"]==topConcept){
                            parentmap[id]["parent"]=parentcls
                        }else{
                            treeitem={
                                "id": id,
                                "parent": parentcls,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLIndividual.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id] = treeitem
                        }
                        
                    }
                } else {
                    if (id != "http://www.w3.org/2002/07/owl#topObjectProperty" && id!="#"){
                       if (!(parentcls in parentmap) && parentcls!="#") {
                            if (parentcls.includes('#')) {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('#') + 1)
                            } else {
                                var textt2 = parentcls.substring(parentcls.lastIndexOf('/') + 1)
                            }
                           treeitem={
                                "id": parentcls,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
                                "text": textt2
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[parentcls] = treeitem
                        }
                        if(id==parentcls){
                            treeitem={
                                "id": id,
                                "parent": topConcept,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)
                            parentmap[id]=treeitem
                        }else if(id in parentmap && parentmap[id]["parent"]==topConcept){
                            parentmap[id]["parent"]=parentcls
                        }else{
                            treeitem={
                                "id": id,
                                "parent": parentcls,
                                "icon": "https://raw.githubusercontent.com/protegeproject/protege/master/protege-editor-owl/src/main/resources/OWLObjectProperty.gif",
                                "text": textt
                            }
                            classTree["core"]["data"].push(treeitem)  
                            parentmap[id]=treeitem
                        }
                        //parentmap[id] = true
                    }
                }


            }
        }
        counter++;
    });
    }
    console.log(classTree["core"]["data"])
    //console.log(classTree)
    return classTree;
}

function createClassTreeFromJSON(json) {
    classTree = {
        "plugins": ["search", "types", "sort", "state", "wholerow"],
        "search": {
            "case_sensitive": false,
            "show_only_matches": true
        },
        "core": {
            "data": []
        }
    }
    classTree["core"]["data"] = json
    return classTree
}
