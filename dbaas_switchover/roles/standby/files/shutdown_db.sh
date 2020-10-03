unset TWO_TASK
ORACLE_SID=$1
DB_UNIQUE_NAME=$1
ORAENV_ASK=NO
export ORACLE_SID ORAENV
. oraenv -s
$ORACLE_HOME/bin/sqlplus -S "/ as sysdba" <<EOF | grep -v "^$"
start db_details.sql
EOF
