import cv2
import sys
from openalpr import Alpr

# region currently set to EU (Europe). Other regions include SG (Singapore) and US
alpr = Alpr("eu", "openalpr.conf", "runtime_data")

# Make sure the library loaded before continuing.
if not alpr.is_loaded():
    print("Error loading OpenALPR")
    sys.exit(1)

# Optionally, provide the library with a region for pattern matching.  Example: md for maryland
# alpr.set_default_region("md")

if len(sys.argv) > 1:
    filepath = str(sys.argv[1])
else:
    print "No file path provided. Program closing."
    sys.exit(1)

img = cv2.imread(filepath)

if not img.size:
    print "file does not exist"
    sys.exit(1)

analyzed_file = alpr.recognize_file(filepath)

if not analyzed_file['results']:
    print "No license plate detected"
    sys.exit(1)

#x,y coordinates of opposite corners of license plate
x1 = analyzed_file['results'][0]['coordinates'][0]['x']
y1 = analyzed_file['results'][0]['coordinates'][0]['y']
x3 = analyzed_file['results'][0]['coordinates'][2]['x']
y3 = analyzed_file['results'][0]['coordinates'][2]['y']

cv2.rectangle(img,(x1,y1),(x3,y3),(0,0,0),-1)
cv2.imwrite(filepath.partition(".")[0]+"_plate_censor.jpg",img)

print "License plate successfully censored"

# Call when completely done to release memory
alpr.unload()   