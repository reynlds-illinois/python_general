#!/usr/bin/env python

#------------------------------------------------------
#
# This script will connect to the iCard database and,
# using a feeder file that consists of UIN's, export
# base64 encoded images from each entry, converting
# them to *.jpg on the fly, resizing to 300x300 resolution
# and saving them to disk as a *.zip archivei.
# These file can then be provided to Bb for addition
# to the Open Photo Roster B2
#
# 2019-11-13 reynlds@illinois.edu
#            - changed to pymssql library
#            - added *.zip file export for archive
#            - added prompt for feed file input
#
# 2019-11-12 reynlds@illinois.edu
#            - updated the FQDN host as it's been changed
#
# 2019-09-19 reynlds@illinois.edu
#            - added error checking/handling
#            - updated conversion for RGB vs. RGBE
#
# 2019-09-18 reynlds@illinois.edu
#            - initial script and testing
#
#------------------------------------------------------

import os, sys
sys.path.insert(1, '/services/ic-tools/bin')
import json, pymssql, base64, zipfile
from PIL import Image
from pymssql import *
from zipfile import *
from icFunctions import *

env_dict = getEnv()                         # environment file for credentials, etc.

host = env_dict['icard.host']               # FQDN or IP that includes the port
db = env_dict['icard.db']                   # database name
user = env_dict['icard.user']               # username for database
pw = env_dict['icard.pass']                 # user password for database

print('List of UINs should be in this location:  /services/ic-tools/iCard/')
feederFile = input('Enter the name of the feeder:  ')

sourceFile = '/services/ic-tools/iCard/' + feederFile

# define a zip file for image archive...this will be sent to hosting provider
zipFilePath = '/services/ic-tools/iCard/' + feederFile
zipFile = zipfile.ZipFile('/services/ic-tools/iCard/' + feederFile, 'a')

# this is the SQL statement that will be executed
sql = """\
DECLARE @out_value INT;
EXEC dbo.pshUINPhotoInfo @UINToLookup = %s, @ResultDataFormat = %s, @PhotoNotFoundAction = %s, @ProcedureResultMessage = @out_value OUTPUT;
SELECT @out_value AS out_value;
"""

try:    # DB connection
    conn = pymssql.connect(server=host, user=user, password=pw, database=db)
    print('> connection created <')
except:
    print('= connection NOT created =')

try:    # DB cursor
    cursor = conn.cursor()                    # creates a cursor object
    print('> cursor created <')
except:
    print('= cursor NOT created =')

inFile = open(sourceFile, 'r')                # defines the feeder file containing UINs

for line in inFile:
    line = line.rstrip('\n')                  # strip the newline
    imageFileName = str('/services/ic-tools/iCard/' + line + '.jpg')    # format the full path using the line input <<< UPDATE AS NEEDED <<<
    print(imageFileName + ' is being processed <<<')
    with open(imageFileName, 'wb') as imageFile:    # open the image file location as a writeable binary
        try:
            params = (line, 'JSON', '0')
            cursor.execute(sql, params)
            data = cursor.fetchone()
            dataJson = json.loads(data[0])    # converts the fetched line to json
            imgData = base64.standard_b64decode(str(dataJson['ImageJPGBase64']))        # converts the image data to jpg
            imageFile.write(imgData)          # writes it to disk
            imageFile.close()                 # closes the image file
            if os.path.exists(imageFileName) and os.path.getsize(imageFileName) > 0:    #checks that file exists and is not zero-byte
                imageTemp = Image.open(imageFileName)                      # opens the image file
                imResize = imageTemp.resize((300,300), Image.ANTIALIAS)    # resizes the image file
                imResize = imResize.convert("RGB")                         # converts to RGB (some images are RGBE)
                imResize.save(imageFileName)                               # writes the resized image to disk
                zipFile.write(imageFileName)                               # add the file to the zip archive
                print(imageFileName + ' has been resized. ###')
                os.remove(imageFileName)                                   # remove the resized image
            else:
                print(imageFileName + ' is a zero byte file. !!!')
                os.remove(imageFileName)
        except:
            print(imageFileName + ' has issues. @@@@@@@@@@')
            continue

zipFile.close() # close the zip archive
inFile.close()  # close the active UIN feed file
cursor.close()  # close the DB cursor object
conn.close()    # close the DB connection
