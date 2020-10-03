unset TWO_TASK
ORACLE_SID=$1
ORAENV_ASK=NO
export ORACLE_SID ORAENV_ASK
. oraenv -s
$ORACLE_HOME/bin/sqlplus -S "/ as sysdba" <<EOF | grep -v "^$"
/*
set heading off
set lin 180
col statement for a50
select ':'||db_unique_name||':'||open_mode||':'||database_role||':' statement from v\$database;
exit;
*/
start db_details.sql
EOF
