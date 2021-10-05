from random import randint
from datetime import datetime, timedelta
import Simulation as sim
import Simulation.process as pro

# Simulate battery_levels, motor positions (to see that the helio is moving), heartbeat (check that controller is working)

class helio():

    def __init__(self, name):
        self.name = name
        # Battery parameters
        self.bat_val = 8
        # Motor parameters
        self.motor1 = 0
        self.motor2 = 0
        self.broken = False
        # System parameters
        self.status = 'running'  # Possible values: running, stow, estop, stopped, down
        # Simulate from the start of a day
        self.date = datetime.utcnow()
        self.date = self.date.replace(hour=7, minute=0, second=0)
        # Simulate a system heartbeat
        cols = ['helio_id', 'status', 'date']
        vals = [name, 'running', 'NOW()']
        sim.DB.insertQ(database=sim.DBname, tname='helio_status', params=cols, host='local', vals=vals)

    # Simulate battery value during operation
    # TODO: This is completely randomly simulated, but actually battery levels will be dependent on weather and time of day
    def battery(self):
        bat_min_allowed = 5.0
        bat_max = 8.3

        chance = sim.bat_crash
        crash = randint(1, chance)

        # Simulate a chance of complete breakdown. chance of breakdown is (1/chance)
        if crash > chance-1:
            self.status = 'down'
            col = 'status'
            val = 'down'
            sim.DB.updateQ2(database=sim.DBname, tname='helio_status', param=col, host='local', val=val, helio_id=self.name)
            return None

        # If self.running is True then return battery value of the heliostat. If self.running is false, then don't
        # send telemetry data and only monitor the local database where self.running must be reset ("repaired") by an operator
        if self.status == 'running' or self.status == 'estop' or self.status == 'stopped' or self.status == 'stow':

            # Simulate battery level fluctuation
            rand = randint(-100, 100)
            trend = sim.trend_multiplier * (rand / 100)
            bat_val = self.bat_val + bat_max * trend
            self.bat_val = bat_val

            # Return battery value
            if bat_val >= bat_max:
                bat_val = bat_max
                return bat_val
            elif bat_val <= bat_min_allowed:
                bat_val = bat_min_allowed
                return bat_val
            else:
                return bat_val

        # Monitor database to check when status is "repaired"
        else:
            pattern = f"helio_id = '{self.name}' "
            cols = ['helio_id', 'status', 'date']
            data = sim.DB.select(sim.DBname, 'helio_status', cols, pattern, 'local')
            data, cols = pro.data_dict(data)
            if data['status'] == 'running':
                self.status = 'running'
            return None

    # Create a timestamp for now and then every minute there after.
    def time(self):
        date = self.date + timedelta(minutes=1)
        self.date = date
        return date

    # Motor 1  only increases (Azimuth angle), motor 2 increases and decreases (Altitude angle).
    # TODO: Implement the Grena algorithm
    def motor(self):
        init = 2000  # If fail, motor value becomes 0, intial value is 2000 so that it doesn't conflict in failure detection
        motor_max = 200000 # 200000 steps divide 660 min in eleven hours (07:00 - 18:00) gives 303 steps per min
        step = 300
        # Operating hours
        start = self.date.replace(hour=7, minute=0, second=0)
        mid = self.date.replace(hour=12, minute=30, second=0)
        stop = self.date.replace(hour=18, minute=0, second=0)

        chance = sim.motor_crash
        crash = randint(1, chance)

        # Introduce some measurement noise
        def noise():
            return randint(-100, 100)

        # Simulate sudden break of the motor. "Repair by resetting value in database
        if crash > chance-1:
            self.broken = True
            self.status = 'down'
            col = 'status'
            val = 'down'
            sim.DB.updateQ2(database=sim.DBname, tname='helio_status', param=col, host='local', val=val,
                            helio_id=self.name)
            return None

        # Simulate motor function with simple linear function. Motor ranges limited to between 2000->200000
        if (self.status == 'running' or self.status == 'stow') and self.broken is False:
            if start <= self.date < mid:
                self.status = 'running'
                motor1 = self.motor1 + step + noise()
                if 2000 <= motor1 <= motor_max:
                    self.motor1 = motor1
                elif motor1 < 2000:
                    self.motor1 = 2000
                else:
                    self.motor1 = motor_max

                motor2 = self.motor2 + step + noise()
                if 2000 <= motor2 <= motor_max:
                    self.motor2 = motor2
                elif motor2 < 2000:
                    self.motor2 = 2000
                else:
                    self.motor2 = motor_max

            elif mid <= self.date < stop:
                motor1 = self.motor1 + step + noise()
                if 2000 <= motor1 <= motor_max:
                    self.motor1 = motor1
                elif motor1 < 2000:
                    self.motor1 = 2000
                else:
                    self.motor1 = motor_max

                motor2 = self.motor2 - step + noise()
                if 2000 <= motor2 <= motor_max:
                    self.motor2 = motor2
                elif motor2 < 2000:
                    self.motor2 = 2000
                else:
                    self.motor2 = motor_max

            else:
                self.status = 'stow'
                motor1 = init
                motor2 = init
                if self.motor1 != init:
                    self.motor1 = init
                if self.motor2 != init:
                    self.motor2 = init

            motor = [motor1, motor2]
            return motor

        # Monitor database for "repair" if self.running or self.broken is not right
        else:
            pattern = f"helio_id = '{self.name}' "
            cols = ['helio_id', 'status', 'date', 'set_motor1', 'set_motor2']
            data = sim.DB.select(sim.DBname, 'helio_status', cols, pattern, 'local')
            data, cols = pro.data_dict(data)
            if data['set_motor1'] is not None and data['set_motor2'] is not None:
                motor1 = data['set_motor1']
                motor2 = data['set_motor2']
                if data['status'] == 'running':
                    self.broken = False
                    motor = [motor1, motor2]
                elif data['status'] == 'estop':
                    motor = [motor1, motor2]
                elif data['status'] == 'stopped':
                    motor = [motor1, motor2]
                elif data['status'] == 'stow':
                    motor = [init, init]
                else:
                    motor = [motor1, motor2]

            else:
                if data['status'] == 'running':
                    self.broken = False
                    motor = [self.motor1, self.motor2]
                elif data['status'] == 'estop':
                    motor = [self.motor1, self.motor2]
                elif data['status'] == 'stopped':
                    motor = [self.motor1, self.motor2]
                elif data['status'] == 'stow':
                    motor = [init, init]
                else:
                    motor = [self.motor1, self.motor2]

            sim.DB.updateQ2(sim.DBname, 'local_pod_list', 'helio_status', data['status'], self.name, 'local')
            return motor

    # Send telemetry data when requested
    def telemetry(self):
        bat = self.battery()
        motor = self.motor()
        date = self.time()
        status = self.status
        telemetry = [bat, motor, date, status]
        return telemetry





