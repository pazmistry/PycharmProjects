#!/bin/ksh
############################################
#        $Author: pmistry $                     $RCSfile: wrapper_restore_point.sh,v $
#        $Date: 2020/09/29 21:16:19 $           $Revision: 1.2 $
############################################
# ~/PycharmProjects/dbaas_restore_point/wrapper_restore_point.sh check ot1 <rp_name>
#

execute_action()
{
 P_ACTION=$1
 echo "INFO: action=$P_ACTION : type=$TYPE is valid "
 for I in rmb eds bie cor dst och odi ; do
  ./oraRestorePoint.py -a $ACTION -s $I -c oraRestorePoint.json -d $D -t $TYPE -l $LABEL
  [[ $? != 0 ]] && echo "ERROR: wrapper failed! ACTION:$P_ACTION TYPE:$TYPE, now terminating" && exit 1
 done
 for I in rmb eds bie cor dst och odi ; do
  ./oraRestorePoint.py -a check -s   $I -c oraRestorePoint.json -d $D -t $TYPE
  [[ $? != 0 ]] && echo "ERROR: wrapper failed! ACTION:$P_ACTION TYPE:$TYPE, now terminating" && exit 1
 done
}

message_type()
{
 D="no"
}

usage()
{
 echo " USAGE:
 ./wrapper_restore_point.sh action type
 action is one of: check create drop
 type   is one of: pt1 pt2 pa1 ot1 sc1 mi1
 label <aRPname> (optional)
 #
 ./wrapper_restore_point.sh $1 $2 $3
 "

}

#MAIN
typeset local ACTION=""
typeset local TYPE=""
ACTION=$1
TYPE=$2
LABEL=$3

D="no"
cd ~/PycharmProjects/dbaas_restore_point/

if [[ $TYPE == "pt1" ]]	|| [[ $TYPE == "pt2" ]] ||	[[ $TYPE == "pa1" ]] || [[ $TYPE == "ot1" ]] ||	[[ $TYPE == "sc1" ]] ||	[[ $TYPE == "mi1" ]]
then
 message_type $TYPE
else
 echo "ERROR: type specified is invalid invalid: $TYPE, now terminating"
 usage
 exit 1
fi

case $ACTION in
 create)   execute_action $ACTION
 ;;
 drop) execute_action $ACTION
 ;;
 check)  execute_action $ACTION
 ;;
 *) echo "ERROR: action $ACTION specified is invalid: $ACTION, now terminating"
 usage
 exit 1
 ;;
esac
