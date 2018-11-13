def myCreateGuest():
    from myExtraFunctions import *
    myGuestDn = 'OU=myOU,DC=ad,DC=myDomain,DC=com
    if myLdapConn.bound == True:
        try:
            myGuestUser = input('New Guest Username: ')
            myGuestUserDn = 'CN=' + myGuestUser + ',' + myGuestDn
            myGuestUserFirstName = input('First Name: ')
            myGuestUserLastName = input('Last Name: ')
            myGuestCaRequest = input('CA Request: ')
            print('Please enter a day in this format:  YYYY-MM-DD')
            myGuestAccountExpire = get_date() #found in myExtraFunctions <-----
            myGuestAccountExpireEpoch = str(get_epoch(myGuestAccountExpire))
            myGuestUserPw = str(gen_guest_pwd()) #found in myExtraFunctions <-----
            myGuestUserLdifAttr = {}
            myGuestUserLdifAttr['objectClass'] = ['top', 'Person', 'organizationalPerson', 'user']
            myGuestUserLdifAttr['cn'] = myGuestUser
            myGuestUserLdifAttr['sAMAccountName'] = myGuestUser
            myGuestUserLdifAttr['userAccountControl'] = '514'
            myGuestUserLdifAttr['givenName'] = myGuestUserFirstName
            myGuestUserLdifAttr['sn'] = myGuestUserLastName
            myGuestUserLdifAttr['description'] = myGuestCaRequest
            myGuestUserLdifAttr['accountExpires'] = myGuestAccountExpireEpoch
            myResult = myLdapConn.add(myGuestUserDn, attributes=myGuestUserLdifAttr)
            myLdapConn.extend.microsoft.modify_password(myGuestUserDn, myGuestUserPw)
            myLdapConn.modify(myGuestUserDn, {'primaryGroupID':(2,['513'])})
            myLdapConn.modify(myGuestUserDn, {'userAccountControl':(2,['512'])})
            myLdapConn.extend.microsoft.unlock_account(myGuestUserDn)
            print('=== AD ACCOUNT CREATED ===')
            print('Username:  ' + myGuestUser)
            print('Password:  ' + myGuestUserPw)
            print('Expires:   ' + myGuestAccountExpire)
            return myResult
        except:
            print('Error - account not created')
            return myResult
    else:
        print('Not bound to LDAP - exiting')
