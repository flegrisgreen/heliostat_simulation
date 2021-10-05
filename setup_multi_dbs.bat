@echo off
title Multiple database setup
echo Setting up databases
start cmd /K call Setup_db "dt_db4"
start cmd /K call Setup_db "dt_db5"
REM start cmd /K call Setup_db "dt_db3"
echo Done