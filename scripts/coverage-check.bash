#!/bin/bash
# receives the expected acceptance percentage
coverage=`coverage report | grep TOTAL | sed -E 's/TOTAL *[0-9]+ *[0-9]* *([0-9]?[0-9])%.*/\1/'`
if [ $coverage -ge $1 ] ; then
    exit 0
else
    exit 1
fi
