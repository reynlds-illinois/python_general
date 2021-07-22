#----------------------------------------------------------------------------
# Facilitates connection to an LDAP directory or Microsoft Active Directory.
#----------------------------------------------------------------------------

def bind2Ldap(ldapHost, ldapBindDn, ldapBindPw):
    '''bind to a directory service like Active Directory or LDAP'''
    import ldap3
    from ldap3 import Server, Connection, ALL
    try:
        ldapServer = Server(ldapHost, port=636, use_ssl=True, get_info=ALL)
        ldapConn = Connection(ldapServer, ldapBindDn, ldapBindPw, auto_bind=True)
        return ldapConn
    except:
        return False
