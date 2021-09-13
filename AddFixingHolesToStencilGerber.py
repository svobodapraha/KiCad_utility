import sys


cmdFlash = "D03"
cmdMove  = "D02"
cmdDraw  = "D01"

XposMM = 0
YposMM = -25


GerberFormat = "FSLAX24Y24"
holePitch = 15
rowPitch = 240
holeXLength = 200
holeDiamMM = 5
holeMarginMM = 15


holeApertureCodeNumber = 99

bbApertureNumber = 98
bbDiamMM = 0.2

holeDiamINCH = holeDiamMM/25.4
bbDiamINCH = bbDiamMM/25.4

def toGerberCoorFormat(posMM, GerberFormat):


    posINCH = posMM / 25.4

    MultK = 1
    if GerberFormat == "FSLAX24Y24":
        MultK = 10000


 
    else:
        print("unknown format")
        sys.exit(-1)
    
    posGerFmt = int(MultK* posINCH)
    posStr = str(posGerFmt).zfill(6)

    return (posStr)

#define aperture
holeApertureCode = "D{}".format(holeApertureCodeNumber).zfill(2)
bbApertureCode   = "D{}".format(bbApertureNumber).zfill(2)
#%ADD20C,0.1969*%

print("%AD{}C,{:.4f}*%".format(holeApertureCode, holeDiamINCH)) 
print("%AD{}C,{:.4f}*%".format(bbApertureCode,   bbDiamINCH)) 

#fixing holes

print("{}*".format(holeApertureCode))
currXposMM = XposMM
currYposMM = YposMM
lastXEndPosMM = -1
for i in range(100):

    #y first row
    XposStr = toGerberCoorFormat(currXposMM, GerberFormat)
    YposStr = toGerberCoorFormat(currYposMM, GerberFormat)
    GerberCommandLine = "X{}Y{}{}*".format(XposStr, YposStr, cmdFlash)
    print(GerberCommandLine)

    
    #y second row
    XposStr = toGerberCoorFormat(currXposMM, GerberFormat)
    YposStr = toGerberCoorFormat(currYposMM+rowPitch, GerberFormat)
    GerberCommandLine = "X{}Y{}{}*".format(XposStr, YposStr, cmdFlash)
    print(GerberCommandLine)

    lastXEndPosMM = currXposMM  #saved last printed position

    #next x pos
    currXposMM = currXposMM + holePitch
    if((i+1)*holePitch > holeXLength):
       break


#boundig box
bbBL_XposMM = XposMM - (holePitch - holeDiamMM/2)
bbBL_YposMM = YposMM - holeMarginMM
bbBR_XposMM = lastXEndPosMM + (holePitch - holeDiamMM/2)
bbBR_YposMM = bbBL_YposMM
bbTR_XposMM = bbBR_XposMM
bbTR_YposMM = YposMM + rowPitch + holeMarginMM
bbTL_XposMM = bbBL_XposMM
bbTL_YposMM = bbTR_YposMM

print("{}*".format(bbApertureCode))

GerberCommandLine = "X{}Y{}{}*".format(toGerberCoorFormat(bbBL_XposMM, GerberFormat), toGerberCoorFormat(bbBL_YposMM, GerberFormat), cmdMove)
print(GerberCommandLine)

GerberCommandLine = "X{}Y{}{}*".format(toGerberCoorFormat(bbBR_XposMM, GerberFormat), toGerberCoorFormat(bbBR_YposMM, GerberFormat), cmdDraw)
print(GerberCommandLine)

GerberCommandLine = "X{}Y{}{}*".format(toGerberCoorFormat(bbTR_XposMM, GerberFormat), toGerberCoorFormat(bbTR_YposMM, GerberFormat), cmdDraw)
print(GerberCommandLine)

GerberCommandLine = "X{}Y{}{}*".format(toGerberCoorFormat(bbTL_XposMM, GerberFormat), toGerberCoorFormat(bbTL_YposMM, GerberFormat), cmdDraw)
print(GerberCommandLine)

GerberCommandLine = "X{}Y{}{}*".format(toGerberCoorFormat(bbBL_XposMM, GerberFormat), toGerberCoorFormat(bbBL_YposMM, GerberFormat), cmdDraw)
print(GerberCommandLine)
