set heading off
set lin 180
col statement for a180

    select ':'||(select INSTANCE_NAME from v$instance)||':'||
    db_unique_name||':'||open_mode||':'||database_role||':'||
    SWITCHOVER_STATUS||':'||DATAGUARD_BROKER||':'||(select round((sysdate-startup_time)*24*60,0) as startup_time_in_mins from v$instance)||':'
    AS statement from v$database;

exit;

