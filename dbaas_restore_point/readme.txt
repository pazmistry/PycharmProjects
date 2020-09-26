#Oracle user setup

SQL> alter session set "_ORACLE_SCRIPT"=true;
Session altered.

SQL> create user svc_automation identified by oracle;
User created.

SQL> grant connect to svc_automation;
Grant succeeded.

SQL> grant select_catalog_role to svc_automation;
Grant succeeded.

SQL> grant sysdba to svc_automation;
Grant succeeded.




select 'drop restore point "'||name||'";' from v$restore_point ;


# ./oraRestorePoint.py -a check -s dst -d yes -t ot1 -c oraRestorePoint.json


# ~/PycharmProjects/dbaas_restore_point/wrapper_restore_point.sh check ot1


