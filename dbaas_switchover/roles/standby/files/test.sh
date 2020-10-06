#!/usr/bin/ksh
# restart_db.sh
# restarts the database rac and or non rac used by ansible only not interactive
# ./restart_db.sh CDB2 CDB2 no

typeset ORACLE_SID=$1
typeset DB_UNIQUE_NAME=$2
typeset IS_RAC=$3

echo " $ORACLE_SID $DB_UNIQUE_NAME $IS_RAC" ./test.log
