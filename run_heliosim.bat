@echo off
title Main sim launch
REM arguements "<pod instance numbers>" "<local database names>"
start cmd /K call single_sim "148,149,150,151,152" "dt_db4"
start cmd /K call single_sim "153,154,155,156,157" "dt_db5"
REM start cmd /K call single_sim "22,23,24,25" "dt_db3"


