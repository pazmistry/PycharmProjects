set heading off
set lin 180
col statement for a50
select ':'||db_unique_name||':'||open_mode||':'||database_role||':' statement from v$database;
exit;
