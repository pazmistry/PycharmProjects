
############################################
#        $Author: pmistry $                     $RCSfile: tns.py,v $
#        $Date: 2020/08/30 08:08:53 $           $Revision: 1.4 $
#        Python 3.7
############################################

import message as m
import re
import os
from subprocess import Popen, PIPE


def get_tns_entries (p_tns_pattern,p_tns_file, p_debug):
    ''' get a list of tns entries by pattern from tnsnames.ora normally primary and standby '''
    isValid = False
    ln_counter = 0
    l_tns_names = []
    m.message("DEBUG: get_tns_entries.1, {0}".format(p_tns_pattern),p_debug)
    m.message("DEBUG: get_tns_entries.2, {0}".format(p_tns_file),p_debug)
    try:
        file = open(p_tns_file, "r")
        for line in file:
            if re.search(p_tns_pattern.upper(), line):
                l_string = str(str.split(line).pop(0))
                l_string = l_string.replace("=","")
                l_tns_names.append(l_string)
                m.message( "INFO : get_tns_entries.3, found {0}".format(l_tns_names[ln_counter]),p_debug)
                ln_counter = ln_counter + 1
        if ln_counter == 0:
            print "ERROR: get_tns_entries.4 : found {0}  entries ".format(ln_counter)
            exit(1)
        return(l_tns_names)
    except Exception as e:
        print "ERROR: get_tns_entries.5 : {0}  file error {1}, :{2}".format(p_tns_pattern,p_tns_file, str(e))
        exit(1)



def get_primary_tns(p_tns_names_list, p_connectString, p_sqlCommand ,p_oracle_home, p_tns_admin,p_debug):
    l_tns_name=''
    m.message("DEBUG: get_primary_tns.1, {0}".format(p_tns_names_list),p_debug)
    for tns_name in p_tns_names_list:
        queryResult, errorMessage = exec_sql(p_connectString + tns_name, p_sqlCommand,p_oracle_home, p_tns_admin,p_debug)
        m.message("DEBUG: get_primary_tns.2, {0}".format(queryResult.strip()),p_debug)
        m.message("DEBUG: get_primary_tns.3, {0}".format(errorMessage),p_debug)
        if queryResult.strip() == 'PRIMARY' and 'ORA-' not in queryResult and 'ORA-' not in errorMessage:
            l_tns_name = tns_name
            m.message("DEBUG: get_primary_tns.4, {0}".format(l_tns_name),p_debug)
    if l_tns_name is not None and l_tns_name != "" and l_tns_name:
        m.message("INFO : get_primary_tns.5, {0}".format(l_tns_name),p_debug)
        return l_tns_name
    else:
        print "ERROR: get_primary_tns.6 : {0}  no primary ".format(l_tns_name)
        exit(1)



def exec_sql(p_connectString, p_sqlCommand ,p_oracle_home, p_tns_admin,p_debug):
    ''' run any statements given against any db credential and return results '''

    os.environ['ORACLE_HOME'] = p_oracle_home
    os.environ['LD_LIBRARY_PATH'] = os.environ['ORACLE_HOME'] + ':' + os.environ['ORACLE_HOME'] + '/lib'
    os.environ['TNS_ADMIN'] = p_tns_admin
    os.environ['PATH'] = os.environ['ORACLE_HOME'] + ':' + os.environ['ORACLE_HOME'] + '/bin:' + os.environ['ORACLE_HOME'] + '/lib:' + os.environ['TNS_ADMIN'] + ':' + os.environ['PATH'] \

    m.message("DEBUG: exec_sql.1, {0}".format(p_connectString),p_debug)
    m.message("DEBUG: exec_sql.2, {0}".format(p_sqlCommand),p_debug)
    m.message("DEBUG: exec_sql.3, {0}".format(p_oracle_home),p_debug)
    m.message("DEBUG: exec_sql.4, {0}".format(p_tns_admin),p_debug)

    try:
        session = Popen(['sqlplus', '-S', p_connectString], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        session.stdin.write(p_sqlCommand)
        return session.communicate()
    except Exception as e:
        print "ERROR: exec_sql.5 : {0}  sql error {1}, {2}".format(p_connectString,p_sqlCommand, str(e))
        exit(1)



def implement_sql_action(p_connectString, p_sqlCommand ,p_oracle_home, p_tns_admin, p_action, p_tns_name,p_debug):
        ''' submit sql to be executed and capture and return results '''
        queryResult, errorMessage = exec_sql(p_connectString, p_sqlCommand,p_oracle_home, p_tns_admin, p_debug)
        m.message("DEBUG: implement_sql_action.1, {0}".format(queryResult.strip()),p_debug)
        m.message("DEBUG: implement_sql_action.2, {0}".format(errorMessage.strip()),p_debug)
        if 'ORA-' not in errorMessage or 'ORA-' not in queryResult:
            print "INFO : implement_sql_action.3, {0} {1}: {2}".format(p_tns_name,p_action,queryResult.strip())
            return queryResult.strip()
        else:
            print "ERROR: implement_sql_action.4, {0} : {1} {2}".format(p_tns_name,p_action, queryResult + errorMessage)
            exit(1)

