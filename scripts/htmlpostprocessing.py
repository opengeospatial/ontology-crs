import os
import json

modules=["cs","co","datum","core","planet","application","projection"]

def replaceTextInFile(filepath,text="Pictures say 1,000 words",replacement=""):
    print("Replacement of "+str(text)+" to "+str(replacement)+" in "+str(filepath))
    with open(filepath, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(text, replacement)
    with open(filepath, 'w') as file:
        file.write(filedata)

def addExamplesToPyLode(examples,filepath,basename=""):
    filedata=""
    with open(filepath, 'r') as file:
        filedata = file.read()
    for exx in examples:
        ex=exx.replace("geosrs:","https://w3id.org/geosrs/"+basename+"/").replace("geosrsgeod:","https://w3id.org/geosrs/"+basename+"/")
        if basename=="projection":
            filedata=filedata.replace("<code>"+ex+"</code></td>","<code>"+ex+"</code></td></tr><tr><th>Example</th><td><a target=\"_blank\" href=\""+examples[exx].replace("geosrsgeod:","")+"\">[Link]</a></td></tr><tr><th>Image</th><td><img src=\"https://raw.githubusercontent.com/situx/proj4rdf/refs/heads/main/resources/projection/"+ex[ex.rfind("/")+1:]+".svg\" width=\"50%\"/></td>")
        else:
            filedata=filedata.replace("<code>"+ex+"</code></td>","<code>"+ex+"</code></td></tr><tr><th>Example</th><td><a target=\"_blank\" href=\""+examples[exx].replace("geosrsgeod:","")+"\">[Link]</a></td>")
    with open(filepath, 'w') as file:
        file.write(filedata)

examples={}
with open("examples.json") as f:
    examples=json.load(f)

dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../images/')
directory = os.fsencode(abspath)
imglist = os.listdir(directory)
for img in imglist:
    print(img)
    filename= os.fsdecode(img)
    if str(filename).endswith(".png"):
        basename=filename[0:filename.rfind('.')]
        print("Exists? "+basename+"/index.html")
        if os.path.exists(basename+"/index.html"):
            replaceTextInFile(basename+"/index.html","<div style=\"width:500px; height:50px; background-color: lightgrey; border:solid 2px grey; padding:10px;margin-bottom:5px; text-align:center;\">Pictures say 1,000 words</div>","<div style=\"background-color: lightgrey; border:solid 2px grey; padding:10px;margin-bottom:5px; text-align:center;\"><img src=\"../images/"+filename+"\"/></div>")

for mod in modules:
    if os.path.exists(mod+"/index.html"):
        addExamplesToPyLode(examples,mod+"/index.html",mod)    
    
