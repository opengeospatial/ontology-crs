import os

def replaceTextInFile(filepath,text="Pictures say 1,000 words",replacement=""):
    print("Replacement of "+str(text)+" to "+str(replacement)+" in "+str(filepath))
    with open(filepath, 'r') as file:
        filedata = file.read()
    filedata = filedata.replace(text, replacement)
    with open(filepath, 'w') as file:
        file.write(filedata)
		
dirname = os.path.dirname(__file__)
abspath = os.path.join(dirname, '../images/')
directory = os.fsencode(abspath)
imglist = os.listdir(directory)
for img in imglist:
    print(img)
    filename= os.fsdecode(img)
    basename=filename[0:filename.rfind('.')]
    print("Exists? "+basename+"/index.html")
    if os.path.exists(basename+"/index.html"):
        replaceTextInFile(basename+"/index.html","Pictures say 1,000 words","<img src=\"../images/"+filename+"\"/>")
    
    
