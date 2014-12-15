from workQ import *
from grassData import *

grassFolder="../../nc_spf/PERMANENT"
command="r.mapcalc \"z=5\""

outputRasters = []
for folder in grassData.rmapOutputFolders:
    outputRasters.append(grassFolder + "/" + folder + "/z")

print outputRasters

wq_command = []
wq_command.append(command)
wq_command.append("0")
wq_command.append(str(len(outputRasters)))
for item in outputRasters:
    wq_command.append(item)

print wq_command

wq = workQ()

taskid = wq.wq_job("test_grass", wq_command)
taskids = []
taskids.append(taskid)

print "command: " 
for c in wq_command:
    print c
print "tasks: "
for c in taskids:
    print c

wq.wq_wait("test_grass", taskids)
