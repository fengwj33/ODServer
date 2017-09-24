#!/bin/sh
basepath=$(cd `dirname $0`; pwd)
DIR=$basepath"/static/"
wget -O $DIR$2 $1
echo "finish" >>$DIR$2".finish"
