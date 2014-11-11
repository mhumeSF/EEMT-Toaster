#!/usr/bin/python

import os, getopt, sys, argparse
#from work_queue import *


def main():
    parser=argparse.ArgumentParser(description='''My Description. And what a lovely description it is. ''')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 0.1')

    parser.add_argument('-t', '--geotiff', type=str, help='geotiff or folder of geotiffs', required=True)
    parser.add_argument('-s', '--start', type=str, help='Enter a start year [Default 1980]')
    parser.add_argument('-e', '--end', type=str, help='Enter an end year [Default 2013]')

    if len(sys.argv)==1:
        parser.print_help()
        parser.print_help()
        sys.exit(1)

    args=parser.parse_args()

    print(args)

    startYear = args.start
    endYear= args.end

    #if(os.path.isdir(args.geotiff)):
        #geotiff = []
        #for file in os.listdir(args.geotiff):
            #if file.endswith("*.tif"):
                #geotiff.append(file)

    #print startYear + ' ' + endYear

if __name__ == "__main__":
    main()


#q = WorkQueue(0)
#q.specify_name("HyperCompute");

#os.system("torque_submit_workers -N HyperCompute 10")

#for day in range(timeSpan):

    #command = ("docker doSomething()")
    #t = Task(command)
    #taskid = q.submit(t)
    #print "submitted task (id# %d): %s" % (taskid, t.command)

#print "waiting for tasks to complete..."
#while not q.empty():
    #t = q.wait(5)
    #if t:
        #print "task (id# %d) complete: %s (return code %d)" % (t.id, t.command, t.return_status)
        #if t.return_status != 0:
            #None

#print "all tasks complete!"
#os.system("qdel $(qselect -u mhume)")
