#!/usr/bin/ksh
# restart_db.sh
# restarts the database rac and or non rac used by ansible only not interactive
# ./restart_db.sh CDB2 CDB2 no

typeset ORACLE_SID=$1
typeset DB_UNIQUE_NAME=$2
typeset IS_RAC=$3

[[ -z ${ORACLE_SID} ]]      && echo " ORACLE_SID is null"       && exit 1
[[ -z ${DB_UNIQUE_NAME} ]]  && echo " DB_UNIQUE_NAME is null"   && exit 1
[[ -z ${IS_RAC} ]]          && echo " IS_RAC is null"           && exit 1


ORAENV_ASK=NO
export ORACLE_SID DB_UNIQUE_NAME IS_RAC ORAENV_ASK

unset TWO_TASK
set oraenv -s
ORAENV_ASK=YES

restart_db_non_rac()
{
  echo "is non rac"
  sqlplus -s "/ as sysdba" @restart_db.sql  | tee ./restart_db_non_rac_${ORACLE_SID}.log
  [[ $? != 0 ]]   && echo "ERROR: restart database failed"           && exit 1
}


case $IS_RAC in
 yes|YES)
  srvctl stop database -d ${DB_UNIQUE_NAME}
  [[ $? != 0 ]]   && echo "ERROR: stop rac database failed"           && exit 1
  sleep 20
  srvctl start database -d ${DB_UNIQUE_NAME}
  [[ $? != 0 ]]   && echo "ERROR: start rac database failed"           && exit 1
 ;;
 no|NO)  restart_db_non_rac
 ;;
 *)   echo "invalid is_rac string ${IS_RAC}"
 exit 1
 ;;
esac

