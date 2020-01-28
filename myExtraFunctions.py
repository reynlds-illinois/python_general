#---------------------------------------------------------
# get a date formated as:  YYYY-MM-DD
#---------------------------------------------------------

def getDate():
    '''format an input date and pass it back in this format YYYY-MM-DD'''
    from datetime import datetime
    while True:
        try:
            daTe = input('Enter a date in this format YYYY-MM-DD:  ')
            datetime.strptime(daTe, '%Y-%m-%d')
            break
        except:
            print(daTe + ' is invalid. Please try again: '),
            continue
    return daTe


#---------------------------------------------------------
# convert date (YYYY-MM-DD) to epoch specifically for use
# to modify Microsoft Active Directory objects
#---------------------------------------------------------

def date2Epoch(daTe):
    '''convert a date to epoch specifically for use by Active Directory'''
    import time
    pattern = '%Y-%m-%d %H:%M:%S'
    dateTime = str(daTe) + ' 23:59:59'
    tempDate = int(time.mktime(time.strptime(dateTime,pattern)))
    epochDate = (tempDate + 11644473600) * 10000000
    return int(epochDate)


#---------------------------------------------------------
# create a simple password
#---------------------------------------------------------

def createPw(newPwLength = 8):
    '''generate a simple random password - 8 chars by default'''
    import random
    from random import randint
    alphaChars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    specialChars = list(".,-_")
    newPw = ''
    for i in range (newPwLength):
        tempIndex = random.randrange(len(alphaChars))
        newPw = newPw + alphaChars[tempIndex]
    for i in range(random.randrange(1,3)):
        tempIndex = random.randrange(len(newPw)//2)
        newPw = newPw[0:tempIndex] + str(random.randrange(10)) + newPw[tempIndex+1:]
    randomChar = randint(2,newPwLength)
    newPwList = list(newPw)
    newPwList[randomChar] = specialChars[randomChar]
    newPw = ''.join(newPwList)
    return newPw


#---------------------------------------------------------
# ask a simple yes or no and return true or false
#---------------------------------------------------------

def yesOrNo(question):
    '''request simple yes or no answer and pass it back'''
    while "the answer is invalid":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


def gen_guest_pwd():

    #---------------------------------------------------------
    #
    # This definition generates a random password for use by
    # guest users of Illinois Compass 2g.
    # Rules:  8 chars, alpha mix with caps and numbers
    #
    # 2015-10-14, reynlds@illinois.edu
    #             initial config and test
    #
    #---------------------------------------------------------

    import random

    alpha = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    pw_length = 8
    guestpw = ''

    # generate base pwd
    for i in range (pw_length):
        next_index = random.randrange(len(alpha))
        guestpw = guestpw + alpha[next_index]

    # add a number or two
    for i in range(random.randrange(1,3)):
        replace_index = random.randrange(len(guestpw)//2)
        guestpw = guestpw[0:replace_index] + str(random.randrange(10)) + guestpw[replace_index+1:]

    # add a capital
    for i in range(random.randrange(1,3)):
        replace_index = random.randrange(len(guestpw)//2,len(guestpw))
        guestpw = guestpw[0:replace_index] + guestpw[replace_index].upper() + guestpw[replace_index+1:]

    PASSWORD = guestpw
    return PASSWORD


def getEnv(envConfFilePath='/services/ic-tools/config/environment_dot.conf'):
    '''parse the environment_dot.conf file into a dictionary for use'''
    #---------------------------------------------------------
    #
    # This definition parses through the environment_dot.conf
    # file and returns all values as a dictionary.
    #
    # 2015-10-30, reynlds@illinois.edu
    #             added maxsplit of 1 for line_tmp
    #
    # 2015-09-29, reynlds@illinois.edu
    #             initial config and test
    #
    #---------------------------------------------------------

    # Read in the environment_dot.conf file to a blank dictionary for later use
    envConfFile = open(envConfFilePath)

    envDict = dict()

    blankCount = 0
    hashCount = 0
    lineCount = 0

    for line in envConfFile:
        if line.strip() == '':
            blankCount = blankCount + 1
        elif line.startswith('#'):
            hashCount = hashCount + 1
        else:
            lineR = line.rstrip()
            lineTmp = lineR.split('=', 1)
            keyTmp = lineTmp[0]
            valTmp = lineTmp[1]
            envDict[keyTmp] = valTmp
            lineCount = lineCount + 1

    return envDict


def get_epoch(exp_date):

    #---------------------------------------------------------
    #
    # This definition converts a provided valid date string to
    # epoch time for use by Active Directory account
    # expiration.
    #
    # 2015-10-05, reynlds@illinois.edu
    #
    #---------------------------------------------------------

    import time

    pattern = '%Y-%m-%d %H:%M:%S'
    date_time = exp_date + ' 23:59:59'
    temp_date = int(time.mktime(time.strptime(date_time,pattern)))
    epoch_date = (temp_date + 11644473600) * 10000000

    return epoch_date


def get_date():

    #---------------------------------------------------------
    #
    # This definition requests a date and validates the format
    # prior to handing the good date back to the requestor.
    # Format returned:  YYYY-MM-DD
    #
    # 2015-10-16, reynlds@illinois.edu
    #             initial configuration and testing
    #
    #---------------------------------------------------------

    from datetime import datetime

    while True:

        try:
            DATE = input()
            datetime.strptime(DATE, '%Y-%m-%d')
            break
        except:
            print(DATE + ' is invalid. Please try again: '),
            continue

    return DATE
