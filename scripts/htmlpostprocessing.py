import os
import json

modules=["cs","co","datum","core","planet","application","projection"]

images=[
"AiryProjection.svg",
"AitoffProjection.svg",
"AlbersEqualAreaProjection.svg",
"ArmadilloProjection.svg",
"AtlantisProjection.svg",
"AugustEpicycloidalProjection.svg",
"AzimuthalEqualAreaProjection.svg",
"AzimuthalEquidistantProjection.svg",
"BSAMCylindricalProjection.svg",
"BakerDinomicProjection.svg",
"BalthasartProjection.svg",
"BehrmannProjection.svg",
"BerghausStarProjection.svg",
"BertinProjection.svg",
"BoggsEumorphicProjection.svg",
"BonneProjection.svg",
"BottomleyProjection.svg",
"BraunStereographicProjection.svg",
"BriesemeisterProjection.svg",
"BromleyProjection.svg",
"CahillKeyesProjection.svg",
"CassiniProjection.svg",
"CollignonButterflyProjection.svg",
"CollignonProjection.svg",
"CoxConformalProjection.svg",
"CraigRetroazimuthalProjection.svg",
"CrasterParabolicProjection.svg",
"CylindricalEqualAreaProjection.svg",
"CylindricalStereographicProjection.svg",
"DodecahedralProjection.svg",
"DymaxionProjection.svg",
"Eckert1Projection.svg",
"Eckert2Projection.svg",
"Eckert3Projection.svg",
"Eckert4Projection.svg",
"Eckert5Projection.svg",
"Eckert6Projection.svg",
"EisenlohrProjection.svg",
"EqualEarthProjection.svg",
"EquidistantConicProjection.svg",
"EquirectangularProjection.svg",
"FaheyProjection.svg",
"FoucautProjection.svg",
"FoucautSinusoidalProjection.svg",
"GS50Projection.svg",
"GallPetersProjection.svg",
"GallStereographicProjection.svg",
"GilbertTwoWorldPerspectiveProjection.svg",
"GingeryProjection.svg",
"GinzburgIVProjection.svg",
"GinzburgIXProjection.svg",
"GinzburgVIIIProjection.svg",
"GinzburgVIProjection.svg",
"GinzburgVProjection.svg",
"GnomonicButterflyProjection.svg",
"GnomonicProjection.svg",
"GoodeHomolosineProjection.svg",
"GringortenProjection.svg",
"GringortenQuincuncialProjection.svg",
"GuyouProjection.svg",
"HEALPixProjection.svg",
"HammerProjection.svg",
"HammerRetroazimuthalProjection.svg",
"HillEucyclicProjection.svg",
"HoboDyerProjection.svg",
"HufnagelIIIProjection.svg",
"HufnagelIIProjection.svg",
"HufnagelIProjection.svg",
"HufnagelIVProjection.svg",
"HufnagelIXProjection.svg",
"HufnagelVIIIProjection.svg",
"HufnagelVIIProjection.svg",
"HufnagelVIProjection.svg",
"HufnagelVProjection.svg",
"HufnagelXIIProjection.svg",
"HufnagelXIProjection.svg",
"HufnagelXProjection.svg",
"IcosahedralProjection.svg",
"InterruptedGoodeHomolosineOceanicViewProjection.svg",
"InterruptedGoodeHomolosineProjection.svg",
"InterruptedQuarticAuthalicProjection.svg",
"KamenetskiyIProjection.svg",
"Kavrayskiy7Projection.svg",
"LagrangeProjection.svg",
"LambertConformalConicProjection.svg",
"LambertCylindricalEqualAreaProjection.svg",
"LarriveeProjection.svg",
"LaskowskiProjection.svg",
"LeeProjection.svg",
"LittrowProjection.svg",
"LoximuthalProjection.svg",
"MaurerNo73Projection.svg",
"McBrydeThomasFlatPolarParabolicProjection.svg",
"McBrydeThomasFlatPolarQuarticProjection.svg",
"McBrydeThomasFlatPolarSinusoidalProjection.svg",
"MercatorProjection.svg",
"MillerProjection.svg",
"MollweideProjection.svg",
"MollweideWagnerProjection.svg",
"NaturalEarth2Projection.svg",
"NaturalEarthProjection.svg",
"NellHammerProjection.svg",
"NicolosiGlobularProjection.svg",
"NordicProjection.svg",
"OrthographicProjection.svg",
"PattersonCylindricalProjection.svg",
"PeirceQuincuncialProjection.svg",
"PolyconicProjection.svg",
"PolyhedralProjection.svg",
"QuarticAuthalicProjection.svg",
"RectangularPolyconicProjection.svg",
"RobinsonProjection.svg",
"SinusoidalProjection.svg",
"SmythEqualSurfaceProjection.svg",
"StabiusWernerIIProjection.svg",
"StereographicProjection.svg",
"TheTimesProjection.svg",
"ToblerHyperellipticalProjection.svg",
"ToblerWorldInASquareProjection.svg",
"TransverseMercatorProjection.svg",
"TrystanEdwardsProjection.svg",
"VanDerGrintenIIIProjection.svg",
"VanDerGrintenIIProjection.svg",
"VanDerGrintenIProjection.svg",
"VanDerGrintenIVProjection.svg",
"WagnerIVProjection.svg",
"WagnerVIIIProjection.svg",
"WagnerVIIProjection.svg",
"WagnerVIProjection.svg",
"WatermanButterflyProjection.svg",
"WiechelProjection.svg",
"WinkelTripelProjection.svg"
]

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
    for img in images:
        imguri="https://w3id.org/geosrs/projection/"+img
        filedata=filedata.replace("<code>"+img.replace(".svg","")+"</code></td>","<code>"+img.replace(".svg","")+"</code></td></tr><tr><th>Image</th><td><img src=\"https://raw.githubusercontent.com/situx/proj4rdf/refs/heads/main/resources/projection/"+img+"\" width=\"50%\"/></td>")
    for exx in examples:
        ex=exx.replace("geosrs:","https://w3id.org/geosrs/"+basename+"/").replace("geosrsgeod:","https://w3id.org/geosrs/"+basename+"/")
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
    
