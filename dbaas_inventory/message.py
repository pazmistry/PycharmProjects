
############################################
#        $Author: pmistry $                     $RCSfile: message.py,v $
#        $Date: 2020/09/25 22:40:46 $           $Revision: 1.3 $    Python 2.7
############################################
from datetime import datetime

def message(p_message,p_debug):

    if ('DEBUG' in p_message or 'INFO' in p_message) and p_debug == 'all':
        #print p_message
        print "{0} : {1}".format(datetime.now().time(), p_message)
    else:
        if 'INFO' in p_message and p_debug == 'yes':
            #print p_message
            print "{0} : {1}".format(datetime.now().time(), p_message)
