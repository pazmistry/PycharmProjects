whenever sqlerror exit failure

set heading off
set lin 180
col statement for a50

shutdown immediate;

exec dbms_lock.sleep(10);

startup;
exit;

