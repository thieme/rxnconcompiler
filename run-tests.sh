#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
#echo $DIR
"$DIR/tests/test_data"
XVALUE = "$DIR/tests/test_data"
MYVALUE="$DIR/tests/test_data"
#echo "$MYVALUE"
export PYTHONPATH=${PYTHONPATH}:$DIR:$XVALUE:$MYVALUE
#echo ${PYTHONPATH}
cd tests
python test_all.py