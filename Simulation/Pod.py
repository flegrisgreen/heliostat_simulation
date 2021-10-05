import Simulation as sim
import Simulation.Helio as H
from random import randint

# Pod class creates the associated heliostats and then adds the grena target for the heliostat and send the telemetry
class Pod():
    # Instance variables
    def __init__(self, name):
        self.pod_name = name
        self.heliostats = self.create_helios()
        self.helios_in_pod = []
    
    # Create 6 heliostat class instances
    def create_helios(self):
        pod = self.pod_name
        helio_list = [f'{pod}.1', f'{pod}.2', f'{pod}.3', f'{pod}.4', f'{pod}.5', f'{pod}.6']
        self.helios_in_pod = helio_list

        heliostats = []
        for helio in helio_list:
            heliostat = H.helio(helio)
            # Create database tables for the new heliostat instances
            try:
                helio_id = helio.split('.')
                helio_id = ''.join(helio_id)

                sim.DB.createTable(sim.DBname, f'local_helio{helio_id}', sim.helio_columns, sim.data_types, 'local')
                sim.DB.insertQ(sim.DBname, 'local_helio_list', ['helio_id', 'date'], [heliostat.name, 'NOW()'], 'local')

                cols = ['pod_id', 'helio_id', 'helio_status', 'date']
                vals = [pod, helio, 'running', 'NOW()']
                sim.DB.insertQ(sim.DBname, 'local_pod_list', cols, vals, 'local')
            except:
                print(f'Could not create helio {helio}')
            finally:
                heliostats.append(heliostat)

        return heliostats

    # The Grena positions are calculated by the clusters and then converted to motor values for LCUs
    def add_Grena_result(self, telemetry):
        for i in range(0, len(telemetry)):
            grena_target = 'target'
            telemetry[i].append(grena_target)
        return telemetry
    
    # Get the telemetry from a single pod 
    def pod_telemetry(self):
        heliostats = self.heliostats
        pod_telemetry_data = telemetry(heliostats)
        pod_telemetry_data = self.add_Grena_result(pod_telemetry_data)
        return pod_telemetry_data  # This is a list of heliostat lists, with each helistat list containing the telemetry

# Function that returns the telemetry values for multiple heliostats
def telemetry(helios):
    vals = []
    h_telemetry = []

    for helio in helios:
        vals.append(helio.name)
        tel = helio.telemetry()  # helio.telemetry returns a list as [battery, [motor1, motor2], date, status]

        if tel[0] is not None:
            vals.append(tel[0])
        else:
            vals.append(0)
            print('Battery value not received')

        if tel[1] is not None:
            if tel[1][0] != 'None':
                vals.append(tel[1][0])
                vals.append(tel[1][1])
            else:
                vals.append(0)
                vals.append(0)
        else:
            vals.append(0)
            vals.append(0)

        if tel[2] is not None:
            vals.append(tel[2])
        else:
            vals.append('NOW()')

        if tel[3] is not None:
            vals.append(tel[3])
        else:
            vals.append('down')

        insert_data = vals.copy()
        h_telemetry.append(insert_data)
        vals.clear()

    return h_telemetry