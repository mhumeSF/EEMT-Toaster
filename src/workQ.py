#!/usr/bin/python
import sys, os
from work_queue import *

class workQ:
    def __init__(self):
        self.q = WorkQueue(0)
        self.q.specify_name("eemt_toaster")

    def wq_job (self, tag, arg_list):
        cmd = arg_list[0]
        num_inputs = int(arg_list[1])
        num_outputs = int(arg_list[num_inputs + 2])

        print arg_list[0]
        try:
            os.system (arg_list[0])
        except:
            print ("command failed : " + arg_list[0])
        return 1928

        t = Task(cmd)
        t.specify_tag(tag)

        for i in range(2, num_inputs + 2):
            print ("Specifying file: " + arg_list[i])
            t.specify_file (arg_list[i], arg_list[i], WORK_QUEUE_INPUT, cache=False)
            if os.path.dirname(arg_list[i]):
                print ("Specifying directory: " + os.path.dirname(arg_list[i]))
                t.specify_directory (os.path.dirname(arg_list[i]), cache=False)

        for i in range(num_inputs + 3, len(arg_list)):
            print ("Specifying file: " + arg_list[i])
            t.specify_file (arg_list[i], arg_list[i], WORK_QUEUE_OUTPUT, cache=False)
            if os.path.dirname(arg_list[i]):
                print ("Specifying directory: " + os.path.dirname(arg_list[i]))
                t.specify_directory (os.path.dirname(arg_list[i]), cache=False)

        taskid = self.q.submit(t)
        # taskid = 0
        print t
        print "Submitted taskid #%d: %s" % (taskid, t.command)

        return taskid

    def wq_wait (self, tag, wait_list):
        if self.q.empty():
            return

        print ("Waiting for tasks with tag %s to complete...") % tag
        completed_tasks = 0
        num_tasks = len(wait_list)

        while not self.q.empty():
            t = self.q.wait(1)
            if t and t.tag == tag:
                completed_tasks = completed_tasks + 1
                print ("\ntaskid #%d complete: (return code %d) %s") % (t.id, t.return_status, t.command)
            # else:
            #     sys.stdout.write (".")
            #     sys.stdout.flush ()

            if completed_tasks == num_tasks:
                break

        print ("\nTasks with tag %s complete!") % tag
