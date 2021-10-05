
from Simulation import DatabaseManager as db

# Database constants
DB = db.DatabaseManager()
DBname = 'testdb'
helio_columns = ['helio_id', 'battery', 'motor1', 'motor2', 'date', 'status', 'grena_target']
data_types = ['varchar(50)', 'real', 'real', 'real', 'timestamp', 'varchar(50)', 'varchar(50)']

# Heliostat simulation parameters
bat_crash = 50000  # chance of crash is equal to (1/bat_crash)
motor_crash = 5000
trend_multiplier = 0.0025  # Scale effect of battery trend
duration = 4000  # Number of minutes (and therefore number of readings) that will be simulated

# counter variable to keep track of database inserts
count = 0

# Number of simulation points for the plotting function
simulation_points = 200
