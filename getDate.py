#---------------------------------------------------------
# request date input and check formate before handing back
# the corrected date in this format: YYYY-MM-DD
#---------------------------------------------------------

def getDate():
    from datetime import datetime
    while True:
        try:
            myDate = input()
            datetime.strptime(myDate, '%Y-%m-%d')
            break
        except:
            print(myDate + ' is invalid. Please try again: '),
            continue
    return myDate
