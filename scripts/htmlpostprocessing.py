import os

def replaceTextInFile(filepath,text="Pictures say 1,000 words",replacement=""):
    with open(fikepath, 'r') as file:
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
    filename=str(img)
    basename=filename[0:filename.rfind('.')]
    if os.path.exists(basename+"/"+basename+".html"):
        replaceTextInFile(basename+"/"+basename+".html","Pictures say 1,000 words","<img src=\"images/"+img+"/>")
    
    