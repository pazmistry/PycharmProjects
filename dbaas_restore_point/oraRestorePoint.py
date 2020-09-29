#!/Users/pmistry/PycharmProjects/dbaas_restore_point/bin/python
#/usr/bin/python

############################################
#        $Author: pmistry $                     $RCSfile: oraRestorePoint.py,v $
#        $Date: 2020/09/29 21:15:50 $           $Revision: 1.4 $     Python 2.7
############################################
# usage :  ./oraRestorePoint.py --help
# usage :  ./oraRestorePoint.py -a [create|drop|check] -s rmb -t sc1 -c oraRestorePoint.json -d [yes|no]
# ./oraRestorePoint.py -a check -s dst -d yes -t ot1 -c oraRestorePoint.json

#import message

''' Takes user input and executes command on the db from a central jump server
PREREQUISTE
 All tns wallet connections must be set up first
'''

import argparse
import json
import os
import time
from datetime import datetime

import message as m
import tns as t


def getInputArgs(p_timestamp):
    ''' Parses the args via args function '''
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", help="optional, cfg file details", default="oraRestorePoint.json")
    parser.add_argument("--debug",  "-d", help="optional, Set debug mode", default="no")
    parser.add_argument("--label",  "-l", help="optional, Set debug mode", default=p_timestamp)
    parser.add_argument("--action", "-a", help="mandatory, values[create|drop|check]")
    parser.add_argument("--db",  "-s", help="mandatory, values[eds|rmb|bie|cor|dst|och|odi]")
    parser.add_argument("--type", "-t", help="mandatory, values[pt1|pt2|pa1|ot1|sc1|mi1]")
    args = parser.parse_args()
    return args


def loadConfig(p_cfg_file):
    ''' Loads config file into global dict '''
    isValid = os.path.isfile(p_cfg_file)
    if isValid == True:
        ln_counter = 0
#        print "INFO : loadConfig.1 : {0} exists: {1}".format(p_cfg_file, isValid)
    else:
        print "ERROR: loadConfig.2 : {0} does not exist, terminating :{1}".format(p_cfg_file, isValid)
        exit(1)
    try:
        with open(p_cfg_file) as f:
            ld_cfgDict = json.load(f)
            f.close()
            return ld_cfgDict
    except Exception as e:
        print "ERROR: loadConfig 3 : {0} config file error, terminating :{1}".format(p_cfg_file, str(e))
        exit(1)


def validate_arguments(p_action, p_db, p_type, pd_cfgDict, p_debug):
    ''' Validate the input arguments   '''
    isValid = True
    errMsg = ""
    if p_action is None or p_db is None:
        errMsg = "arg=none"
        isValid = False
    if isValid == True and p_action not in pd_cfgDict['oraUserAction']['valid_action_list']:
        errMsg += ",action = invalid"
        isValid = False
    if isValid == True and p_db not in pd_cfgDict['oraUserAction']['valid_db_list']:
        errMsg += ",environment = invalid"
        isValid = False
    if isValid == True and p_type not in pd_cfgDict['oraUserAction']['valid_type_list']:
        errMsg += ",type = invalid"
        isValid = False
    if isValid == False:
        print "ERROR: validate_arguments 1, error message {0}!".format(errMsg)
        exit(1)
    else:
        pd_cfgDict['oraUserAction']['action'] = p_action
        pd_cfgDict['oraUserAction']['db'] = p_db
        pd_cfgDict['oraUserAction']['type'] = p_type
        m.message( "INFO : validate_arguments 2, are {0} and {1}!".format(pd_cfgDict['oraUserAction']['action'],pd_cfgDict['oraUserAction']['db']), p_debug)
        return pd_cfgDict



##############
# Main
##############

#executed when script is run
if __name__ == '__main__':
    g_timestamp=datetime.now().time()
    g_datestamp=datetime.now()
    args = getInputArgs("RP_"+g_datestamp.strftime("%Y%m%d%H%M%S"))
    gd_cfgDict = dict()

    lpath_rel = os.path.abspath(__file__) + '/'

    fileDir = os.path.dirname(os.path.realpath('__file__'))
    lpath = os.path.join(fileDir, '../dbaas_inventory/')

    tns_names_list = []
    l_action = args.action.lower().strip()
    l_debug = args.debug.lower().strip()

    if args.config is None:
        #print ("ERROR: Incorrect arguments, see --help. Exiting")
        m.message("ERROR: main.1, Incorrect arguments, see --help. Exiting",l_debug)
        exit(1)
    else:
        gd_cfgDict = loadConfig(lpath + args.config)
        m.message("INFO : main.2, Started ", l_debug)
        gd_cfgDict = validate_arguments(args.action.lower(),args.db.lower(),args.type.lower(),gd_cfgDict,l_debug)
        tns_names_list = t.get_tns_entries(gd_cfgDict['oraUserAction']['db'] + gd_cfgDict['oraUserAction']['environment'] + gd_cfgDict['oraUserAction']['type'] , gd_cfgDict['oraUserAction']['tns_admin']+gd_cfgDict['oraUserAction']['tns_file'],l_debug)
        m.message("DEBUG : main.3, tns list : {0}".format(tns_names_list),l_debug)
        l_tns_count =len(tns_names_list)
        m.message("DEBUG : main.4, tns count : {0}".format(len(tns_names_list)),l_debug)

        # Undertake primary and standby actions
        l_primary_tns, l_standby_tns = t.get_tns_role(tns_names_list,gd_cfgDict['oraUserAction']['sql_connect_string'],gd_cfgDict['oraUserAction']['sql_database_role'] ,gd_cfgDict['oraUserAction']['oracle_home'],gd_cfgDict['oraUserAction']['tns_admin'],l_debug)
        if len(tns_names_list) == 2:
            queryResult = t.implement_sql_action(gd_cfgDict['oraUserAction']['sql_connect_string'], gd_cfgDict['oraUserAction'][l_action]['user_sql_implement'].format(args.label) ,gd_cfgDict['oraUserAction']['oracle_home'], gd_cfgDict['oraUserAction']['tns_admin'], l_action, l_standby_tns, l_debug)
            time.sleep(5)
        queryResult = t.implement_sql_action(gd_cfgDict['oraUserAction']['sql_connect_string'], gd_cfgDict['oraUserAction'][l_action]['user_sql_implement'].format(args.label) ,gd_cfgDict['oraUserAction']['oracle_home'], gd_cfgDict['oraUserAction']['tns_admin'], l_action, l_primary_tns, l_debug)

m.message ("INFO : main.5, SUCCESSFULLY COMPLETED ", l_debug)
# need to display action of check and create and drop
