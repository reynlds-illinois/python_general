#---------------------------------------------------------
# Facilitates connection to an LDAP directory or Microsoft
# Active Directory.
# Requires:   ldap3, from ldap3: Server, Connection, ALL
#             all variables a defined below
#---------------------------------------------------------

def bind2Ldap(myLdapHost, myLdapBindDn, myLdapBindPw):
    global myLdapConn
    try:
        myLdapServer = Server(myLdapHost, port=636, use_ssl=True, get_info=ALL)
        myLdapConn = Connection(myLdapServer, myLdapBindDn, myLdapBindPw, auto_bind=True)
        print('=== SUCCESSFULLY CONNECTED TO LDAP ===')
        return myLdapConn
    except:
        print('=== NOT CONNECTED TO LDAP ===')
        return myLdapConn

