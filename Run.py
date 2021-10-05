import Simulation.SimSetup as S
import Simulation as sim
import argparse

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Enter the id numbers of the desired pods. Separate numbers with a comma.')
    parser.add_argument(dest='pod_ids', metavar='pod_ids',
                        help='Creates the heliostat pods that are listed')
    parser.add_argument(dest='dbname', metavar='dbname',
                        help='Give the name of the database where the data should be written to')
    args = parser.parse_args()
    pods = args.pod_ids
    if args.dbname is not None:
        dbname = args.dbname
        sim.DBname = dbname
        print(dbname)
    # sim.DBname = 'dt_db1'
    # pods = '13,14,15,16,17'
    print(pods)
    S.Sim(pods)