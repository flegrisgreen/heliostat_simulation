from matplotlib import pyplot as plt
from matplotlib import animation as anim
import Simulation as sim
# Make a plots for the battery and motor values
def plot(date, bat_vals, name, motor1, motor2):
    fig = plt.figure()
    ax = fig.add_subplot(3, 1, 1)
    ax.plot(date, bat_vals)
    ax.set_xlabel('Time')
    ax.set_ylabel('Battery Value')
    ax.set_title(name + ' battery')

    axm = fig.add_subplot(3, 1, 2)
    axm.plot(date, motor1, label='motor 1')
    axm.xlabel('Time')
    axm.ylabel('Motor Count')
    axm.title(name + ' motor 1 counts')

    axm2 = fig.add_subplot(3, 1, 3)
    axm2.plot(date, motor2, label='motor 2')
    axm.xlabel('Time')
    axm.ylabel('Motor Count')
    axm.title(name + ' motor 2 counts')

    fig.show()





