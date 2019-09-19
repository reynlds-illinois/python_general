#!/usr/bin/env python

#------------------------------------------------------
#
# This script will connect to the iCard database and,
# using a feeder file that consists of UIN's, export
# base64 encoded images from each entry, converting
# them to *.jpg on the fly, and saving them to disk,
# as well as resizing each one to 300 x 300 resolution.
# These file can then be provided to Bb for addition
# to the Open Photo Roster B2
#
# >>> PLEASE NOTE THE PATHS AND FEEDER NAME AND UPDATE AS NEEDED!!! <<<
#
# 2019-09-19 reynlds@illinois.edu
#            - added error checking/handling
#            - updated conversion for RGB vs. RGBE
#
# 2019-09-18 reynlds@illinois.edu
#            initial script and testing
#
#------------------------------------------------------

import os, sys, json, pyodbc, sqlalchemy, base64
from PIL import Image

host = "MY_HOST_NAME,MY_PORT_NUMBR"    # FQDN or IP that also contains the port
db   = "MY_DATABASE_NAME"    # database name
user = "MY_USERNAME"    # database username
pw   = "MY_PASSWORD"    # database username password

format   = 'JSON'    # define the return format as a JSON object
notfound = '0'    # this value is generated for the stored procedure to handle null image data
sourceFile = 'c:/icard/120198.txt'    # define the feeder file containing UINs <<< UPDATE AS NEEDED <<<
width    = 300    # define resized image width
length   = 300    # define resized image length

conn = pyodbc.connect(driver="{SQL SERVER}",server=host,database=db,UID=user,pwd=pw)    # authenticates to DB
cursor = conn.cursor()    # creates a cursor object

inFile = open(sourceFile, 'r')    # defines the feeder file containing UINs

for line in inFile:
    line = line.rstrip('\n')    # strip the newline 
    imageFileName = str('c:/icard/images/' + line + '.jpg')    # format the full path using the line input <<< UPDATE AS NEEDED <<<
    with open(imageFileName, 'wb') as imageFile:    # open the image file location as a writeable binary
        try:
            storedProc = str("exec IDClientPortal..pshUINPhotoInfo '"+ line +"', '" + format + "', '" + notfound + "'")    # format the sql as a string
            r = cursor.execute(storedProc)    # executes the sql
            data = r.fetchone()    # returns back the next line in the db
            dataJson = json.loads(data[0])    # converts the fetched line to json
            imgData = base64.standard_b64decode(str(dataJson['ImageJPGBase64']))    # converts the image data to jpg
            imageFile.write(imgData)    # writes it to disk
            imageFile.close()    # closes the image file
            if os.path.exists(imageFileName) and os.path.getsize(imageFileName) > 0:    #checks that file exists and is not zero-byte
                imageTemp = Image.open(imageFileName)    # opens the image file
                imResize = imageTemp.resize((300,300), Image.ANTIALIAS)    # resizes the image file
                imResize = imResize.convert("RGB")    # converts to RGB (some images are RGBE)
                imResize.save(imageFileName)    # writes the resized image to disk
                #print(imageFileName + ' has been resized. ###')    # uncomment for debug
            else:
                #print(imageFileName + ' is a zero byte file. !!!') # uncomment for debug
        except:
            #print(imageFileName + ' has issues. @@@@@@@@@@')       # uncomment for debug
            continue

inFile.close()  # close the active UIN feed file
cursor.close()  # close the DB cursor object
conn.close()    # close the DB connection
