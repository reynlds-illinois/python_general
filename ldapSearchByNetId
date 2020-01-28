#---------------------------------------------------------
# check AD/ldap to see if a username already exists
# Requires a valid ldap Connection
#---------------------------------------------------------

def ldapSearchByNetId(ldapConn, ldapSearchBase, netId):
    '''search for an existing user in a directory service like AD or LDAP'''
    adFilter = '(&(objectclass=user)(sAMAccountName=' + netId  + '))'
    if ldapConn.bind():
        netIdSearch = ldapConn.search(search_base=ldapSearchBase,
                            search_filter=adFilter,
                            search_scope='SUBTREE',
                            attributes = ['sAMAccountName',
                           'displayName',
                           'userPrincipalName',
                           'givenName',
                           'sn',
                           'mail',
                           'distinguishedName'],
                            size_limit=0)
        return netIdSearch
    else:
        print('>>> Not bound to AD or LDAP <<<')
