#!/usr/bin/env bash

# obtains all data tables from database
TS=`sqlite3 $1 "SELECT tbl_name FROM sqlite_master WHERE type='table' and tbl_name not like 'sqlite_%';"`
mkdir tables
# exports each table to csv
for T in $TS; do

sqlite3 $1 <<!
.headers on
.mode csv
.output tables/$T.csv
select * from $T;
!

done

echo
echo 'Use one of the following IDs to plot the GDPR chart:'

sqlite3 $1 <<!
.headers on
.mode column
select id, name from subject;
!
echo '---'