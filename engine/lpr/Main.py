import os
import tkinter
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import sys
sys.path.append(os.path.abspath("E:\\NIX POD\\Projects\\Vehical_Tracking_Theft_Detection_System_GUI\\engine\\lpr"))
import DetectChars
import DetectPlates
import cv2
import pandas as pd

# from engine.lpr import DetectChars
# from engine.lpr import DetectPlates
# from engine.lpr import PossiblePlate
# from engine.lpr import *

# moduleName = input('DetectChars')
# importlib.import_module(moduleName)

# moduleName1 = input('DetectPlates')
# importlib.import_module(moduleName1)

root = Tk()
root.withdraw()
root.fileName = filedialog.askopenfilename(filetypes=(("Captured Image", "*.png"), ("All Files", "*.*")))

# module level variables
SCALAR_BLACK = (0.0, 0.0, 0.0)
SCALAR_WHITE = (255.0, 255.0, 255.0)
SCALAR_YELLOW = (0.0, 255.0, 255.0)
SCALAR_GREEN = (0.0, 255.0, 0.0)
SCALAR_RED = (0.0, 0.0, 255.0)

showSteps = False


def main():
    blnKNNTrainingSuccessful = DetectChars.loadKNNDataAndTrainKNN()

    if not blnKNNTrainingSuccessful:
        print("\nerror: KNN training was not successful\n")
        return
    # end if

    imgOriginalScene = cv2.imread(root.fileName)  # open captured image from camera

    if imgOriginalScene is None:  # if image was invalid
        print("\nerror: invalid image \n\n")
        os.system("pause")
        return
    # end if

    listOfPossiblePlates = DetectPlates.detectPlatesInScene(imgOriginalScene)

    listOfPossiblePlates = DetectChars.detectCharsInPlates(listOfPossiblePlates)

    cv2.imshow("imgOriginalScene", imgOriginalScene)  # show scene image

    if len(listOfPossiblePlates) == 0:  # if no licence plates were found
        print("\nno license plates were detected\n")
    else:

        listOfPossiblePlates.sort(key=lambda possiblePlate: len(possiblePlate.strChars), reverse=True)
        licPlate = listOfPossiblePlates[0]

        cv2.imshow("imgPlate", licPlate.imgPlate)  # show crop of and threshold of licence plate.
        cv2.imshow("imgThresh", licPlate.imgThresh)

        if len(licPlate.strChars) == 0:
            print("\nno characters were detected\n\n")
            return
        # end if

        drawRedRectangleAroundPlate(imgOriginalScene, licPlate)  # draw red rectangle around plate

        print("\nlicense plate read from image = " + licPlate.strChars + "\n")
        print("----------------------------------------")
        cv2.imshow("imgOriginalScene", imgOriginalScene)

        cv2.imwrite("imgOriginalScene.png", imgOriginalScene)

        dp = pd.read_csv("D:\\VTH_LANE\\data\\theftds.csv")
        # ab = dp.loc[(dp['License Plate'] == licPlate.strChars)]
        vv = dp[dp['License Plate'].str.contains(licPlate.strChars)].count()
        #vv = bv.count()
        if vv[0] == 0:
            tkinter.messagebox.showinfo(title='Information',
                                        message="Licese plate deteted is " + licPlate.strChars + "\n")
        else:
            tkinter.messagebox.showinfo(title='Warning!!',
                                        message="Licese plate deteted is under tracking, contact police department: " + licPlate.strChars + "\n")

        writeLicensePlateCharsOnImage(imgOriginalScene, licPlate)

    # end if else
    cv2.waitKey(0)
    return


# end main

def drawRedRectangleAroundPlate(imgOriginalScene, licPlate):
    p2fRectPoints = cv2.boxPoints(licPlate.rrLocationOfPlateInScene)

    cv2.line(imgOriginalScene, tuple(p2fRectPoints[0]), tuple(p2fRectPoints[1]), SCALAR_RED, 2)  # draw 4 red lines
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[1]), tuple(p2fRectPoints[2]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[2]), tuple(p2fRectPoints[3]), SCALAR_RED, 2)
    cv2.line(imgOriginalScene, tuple(p2fRectPoints[3]), tuple(p2fRectPoints[0]), SCALAR_RED, 2)


# end function

def writeLicensePlateCharsOnImage(imgOriginalScene, licPlate):
    ptCenterOfTextAreaX = 0
    ptCenterOfTextAreaY = 0

    ptLowerLeftTextOriginX = 0
    ptLowerLeftTextOriginY = 0

    sceneHeight, sceneWidth, sceneNumChannels = imgOriginalScene.shape
    plateHeight, plateWidth, plateNumChannels = licPlate.imgPlate.shape

    intFontFace = cv2.FONT_HERSHEY_SIMPLEX
    fltFontScale = float(plateHeight) / 30.0
    intFontThickness = int(round(fltFontScale * 1.5))

    textSize, baseline = cv2.getTextSize(licPlate.strChars, intFontFace, fltFontScale,
                                         intFontThickness)

    # unpack rotated rect into center point, width and height, and angle
    ((intPlateCenterX, intPlateCenterY), (intPlateWidth, intPlateHeight),
     fltCorrectionAngleInDeg) = licPlate.rrLocationOfPlateInScene

    intPlateCenterX = int(intPlateCenterX)
    intPlateCenterY = int(intPlateCenterY)

    ptCenterOfTextAreaX = int(intPlateCenterX)

    if intPlateCenterY < (sceneHeight * 0.75):
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) + int(
            round(plateHeight * 1.6))
    else:
        ptCenterOfTextAreaY = int(round(intPlateCenterY)) - int(
            round(plateHeight * 1.6))
    # end if

    textSizeWidth, textSizeHeight = textSize

    ptLowerLeftTextOriginX = int(
        ptCenterOfTextAreaX - (textSizeWidth / 2))
    ptLowerLeftTextOriginY = int(
        ptCenterOfTextAreaY + (textSizeHeight / 2))

    cv2.putText(imgOriginalScene, licPlate.strChars, (ptLowerLeftTextOriginX, ptLowerLeftTextOriginY), intFontFace,
                fltFontScale, SCALAR_YELLOW, intFontThickness)


if __name__ == "__main__":
    main()

sys.stdout.flush()
