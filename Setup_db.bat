@echo off
title Single database setup
echo Setting up database %1 for heliostat simulation
env\scripts\activate && cd Simulation && python DatabaseManager.py -dbname %1
echo Database %1 setup
Pause