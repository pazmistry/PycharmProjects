
############################################
#        $Author: pmistry $                     $RCSfile: message.py,v $
#        $Date: 2020/08/30 08:09:17 $           $Revision: 1.2 $
#        Python 3.7
############################################

def message(p_message,p_debug):

    if ('DEBUG' in p_message or 'INFO' in p_message) and p_debug == 'all':
        print p_message
    else:
        if 'INFO' in p_message and p_debug == 'yes':
            print p_message
