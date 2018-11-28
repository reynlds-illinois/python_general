#---------------------------------------------------------
# create a simple password
#---------------------------------------------------------

def createPw(newPwLength = 8):
    import random
    from random import randint
    alphaChars = 'abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    specialChars = list('!@#$%&*._-')
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
