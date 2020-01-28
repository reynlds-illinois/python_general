#---------------------------------------------------------
# query AD/LDAP to get members of a group
# Requires a valid ldap Connection and returns list of CNs
#---------------------------------------------------------

def ldapGetGroupMembers(ldapConn, ldapSearchBase, groupCn):
    '''show members of a group in a directory service like AD or LDAP'''
    if ldapConn.bind():
        adFilter = '(&(objectclass=group)(sAMAccountName=' + groupCn  + '))'
        ldapConn.search(search_base=ldapSearchBase, search_filter=adFilter, search_scope='SUBTREE',attributes = ['member'], size_limit=0)
        members = (ldapConn.entries)
        return members
    else:
        print('>>> Not bound to AD or LDAP <<<')
