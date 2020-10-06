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

unset TWO_TASK
ORAENV_ASK=NO
export ORACLE_SID DB_UNIQUE_NAME IS_RAC ORAENV_ASK


. oraenv
ORAENV_ASK=YES
echo $ORACLE_SID

shutdown_db_non_rac()
{
  echo "is non rac"
  sqlplus / as sysdba @shutdown_db.sql > shutdown_db_${ORACLE_SID}.log 2>&1
  RC=$?
  [[ $RC != 0 || -n $RC ]]   && echo "ERROR: shutdown  database failed: $RC"         && exit 1
  echo "INFO : shutdown database completed ok"
}

startup_db_non_rac()
{
  echo "is non rac"
  sqlplus / as sysdba @startup_db.sql > startup_db_${ORACLE_SID}.log 2>&1
  RC=$?
  [[ $RC != 0 || -n $RC ]]   && echo "ERROR: startup database failed: $RC"         && exit 1
  echo "INFO : startup database completed ok"
}


case $IS_RAC in
 yes|YES)
   srvctl stop database -d ${DB_UNIQUE_NAME} | tee ${ORACLE_SID}.log
   [[ $? != 0 ]]   && echo "ERROR: stop rac database failed"          && exit 1
   sleep 20
   srvctl start database -d ${DB_UNIQUE_NAME} | tee -a ${ORACLE_SID}.log
   [[ $? != 0 ]]   && echo "ERROR: start rac database failed"          && exit 1
 ;;
 no|NO)
   shutdown_db_non_rac
   sleep 10
   startup_db_non_rac
 ;;
 *)
   echo "invalid is_rac string ${IS_RAC}"
   exit 1
 ;;
esac

echo "INFO : restart_db.sh completed ok"
