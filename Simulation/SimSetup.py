import Simulation.Pod as P
from threading import Thread as thread
from time import sleep
import Simulation as sim  # import all values and instance defined in __init__
from Simulation.Graph import plot
import sys

# TODO: Simulate that when breakdown occurs, someone has to reset the helios
# Reset database by running function in DatabaseManager, at the bottom.

count = 1
# Create a thread for each pod so that data is written concurrently
def create_thread(pod):
    class Thread(thread):
        def __init__(self, name):
            thread.__init__(self)
            self.name = name

        def run(self):
            while True:
                global count

                # Get telelmetry from pod periodically and write it to the PostgreSQL database
                pod_info = pod.pod_telemetry()
                for i in range(0, len(pod_info)):
                    helio_id = pod_info[i][0]
                    helio_id_str = helio_id.split('.')
                    helio_id_str = ''.join(helio_id_str)
                    vals = pod_info[i].copy()
                    sim.DB.insertQ(sim.DBname, f'local_helio{helio_id_str}', sim.helio_columns, vals, 'local')
                # sleep(0.2)
                print(count)
                count += 1
                if count >= sim.duration:
                    sys.exit(0)

    T = Thread(pod.pod_name)
    T.start()

def Sim(pod_ids):
    pods_list = pod_ids.split(',')

    # Create heliostat pod instance in its own thread
    for pod in pods_list:
        Pod = P.Pod(pod)
        create_thread(Pod)

# The Sim() and telemetry(helio) functions below write to the database. Below these two functions are redefined to give a trend plot

# def Sim():
#     # Setup database
#     DB = sim.DB
#     database = sim.DBname
#     table = sim.table
#     host = sim.host
#     cols = sim.columns
#     dtypes = sim.data_types
#     DB.deleteTable(database=database, table=table, host=host)
#     DB.createTable(database=database, host=host, cols=cols, dtype=dtypes, name=table)
#
#     # Create heliostat instances
#     helio1 = H.helio('1.1')
#     helio2 = H.helio('1.2')
#     helio3 = H.helio('1.3')
#
#     # Create threads for the heliostats
#     helios = [helio1, helio2, helio3]
#     for helio in helios:
#         create_thread(helio)
#
# def telemetry(helio):
#     vals = []
#     DB = sim.DB
#
#     while True:
#         vals.append(helio.name)
#         tel = helio.telemetry()  # helio.telemetry returns a list as [battery, [motor1, motor2], date]
#
#         if tel[0] is not None:
#            vals.append(tel[0])
#         else:
#            vals.append(0)
#            print('Battery value not received')
#
#         if tel[1] is not None:
#             vals.append(tel[1][0])
#             vals.append(tel[1][1])
#         else:
#             vals.append(0)
#             vals.append(0)
#
#         if tel[2] is not None:
#             vals.append(tel[2])
#         else:
#             vals.append('NOW()')
#
#         DB.insertQ(database=sim.DBname, tname=sim.table, params=sim.columns, host=sim.host, vals=vals)
#         print(sim.count)
#         vals.clear()
#         sleep(0.4)


# def telemetry(helio):
#     bat_vals = []
#     date = []
#     motor1 = []
#     motor2 = []
#     print('Plotting graph')
#     for i in range(1, sim.simulation_points, 1):
#
#         tel = helio.telemetry()  # helio.telemetry returns a list as [battery, [motor1, motor2], date]
#
#         if tel[0] is not None:
#             bat_vals.append(tel[0])
#
#         else:
#            bat_vals.append(0)
#
#         if tel[1] is not None:
#             motor1.append(tel[1][0])
#             motor2.append(tel[1][1])
#
#         else:
#             motor1.append(0)
#             motor2.append(0)
#
#         if tel[2] is not None:
#             date.append(tel[2])
#         else:
#             date.append(date[i-1])
#
#     print('Creating plot')
#     plot(date, bat_vals, helio.name, motor1, motor2)
#     bat_vals.clear()
#     date.clear()
#     motor1.clear()
#     motor2.clear()