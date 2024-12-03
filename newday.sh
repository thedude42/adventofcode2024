#!/usr/bin/env bash

DAY="$1"

DAY_PY="day${DAY}.py"
DAY_INPUT="input$DAY"
DAYDIR="day$DAY"

mkdir $DAYDIR
touch $DAYDIR/$DAY_INPUT
touch $DAYDIR/test1
touch $DAYDIR/test2
cp newday.py $DAYDIR/$DAY_PY
