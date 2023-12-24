#!/bin/bash

Help()
{
    echo "Usage: ??????"
    echo ""
    echo "options:"
    echo "-h        Display this message and exit."
    echo ""
    echo "          Script opts:"    
    echo ""
    echo "-t        Time to get journalctl since, defaults to 'today'"
    echo "-g        Sets GPU test time."
    echo "-G        Skips GPU tests."
    echo "-M        Skips memtester??????????????????????????????????????????"
    echo ""
    echo "          Build info opts:"
    echo ""
    echo "-s        Set serial number."
    echo "-o        Set order number."
    echo "-b        Set build number."
}

SINCE="today"
SERIAL_NUM=""

#not super important now, do eventually#

while getopts ":ht:s:" option; do
   case $option in
        h) # help text
            Help
            exit;;
        t) # time
            SINCE=$OPTARG;;
        s) # Serial Num
            SERIAL_NUM="_$OPTARG";;
        \?) # Invalid option
            echo "Error: Invalid option"
	        Help
            exit;;
   esac
done