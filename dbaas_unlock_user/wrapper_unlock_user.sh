#!/bin/ksh
# ~/dbaas_unlock_user/wrapper_unlock_user.sh

execute_action()
{
 P_ACTION=$1
 echo "INFO: action=$P_ACTION : type=$TYPE is valid "
 for I in rmb eds bie cor dst och odi ; do
  ./oraUserAction.py -a $ACTION -s $I -c oraUserAction.json -d $D -t $TYPE
 done
 for I in rmb eds bie cor dst och odi ; do
  ./oraUserAction.py -a check -s   $I -c oraUserAction.json -d $D -t $TYPE
 done
}

message_type()
{
 D="no"
}

usage()
{
 echo " USAGE:
 ./deploy_user_action.sh action type
 action is one of check unlock lock
 type is one of pt1 pt2 pa1 ot1 sc1 mi1 "
}

#MAIN
typeset local ACTION=""
typeset local TYPE=""
ACTION=$1
TYPE=$2
D="no"
cd ~/PycharmProjects/dbaas_unlock_user/

if [[ $TYPE == "pt1" ]]	||	[[ $TYPE == "pt2" ]] ||	[[ $TYPE == "pa1" ]] || [[ $TYPE == "otl" ]] ||	[[ $TYPE == "sc1" ]] ||	[[ $TYPE == "mi1" ]]
then
 message_type $TYPE
else
 echo "ERROR: type invalid, terminating"
 usage
 exit 1
fi

case $ACTION in
 lock)   execute_action $ACTION
 ;;
 unlock) execute_action $ACTION
 ;;
 check)  execute_action $ACTION
 ;;
 *) echo "ERROR: action $ACTION invalid, now terminating"
 usage
 exit 1
 ;;
esac
