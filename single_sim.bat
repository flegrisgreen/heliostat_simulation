@echo off
title Single ccu sim
echo Launching heliosim for pods %1 and database %2
env\scripts\activate && python Run.py %1 %2
echo Simulation done...
pause