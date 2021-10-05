# Heliostat field simulation

## Overview
This program simulutes a basic heliostat field and writes the data to an SQL database

## Getting started
- Install Python 3.8
- Install postgreSQL 
- Create postgreSQL database(s)

## Running the simulation
- run the setup_venv.bat file
- run setup_multi_dbs.bat file
- run run_heliosim.bat file
- Note: .bat files can be opened as text file using notepad++ to run individual steps or change arguements

## Modules
* Run.py is the entry point but it requires inputs which are provided by the .bat files
* DatabaseManager.py is a set of functions to interact with a SQL database
* Graph.py is for debugging
* Helio.py simulates a single heliostat
* Pod.py spawns heliostats
* SimSetup spawns the pods according to the config in the init.py file

