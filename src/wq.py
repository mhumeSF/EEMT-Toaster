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

		t = Task(cmd)
		t.specify_tag(tag)

		for i in range(1, num_inputs + 1):
			t.specify_file (arg_list[i], arg_list[i], WORK_QUEUE_INPUT, cache=True)
		
		for i in range(num_inputs + 2, len(arg_list)):
			t.specify_file (arg_list[i], arg_list[i], WORK_QUEUE_OUTPUT, cache=True)

		taskid = self.q.submit(t)
		print "submitted task (id# %d): %s" % (taskid, t.command)

		return taskid

	def wq_wait (self, tag, wait_list):
		print "waiting for tasks to complete..."
		completed_tasks = 0
		num_tasks = len(wait_list)

		while not q.empty():
			t = self.q.wait(1)
			if t and t.tag == tag:
				completed_tasks = completed_tasks + 1
				print "task (id# %d) complete: %s (return code %d)" % (t.id, t.command, t.return_status)
			if completed_tasks == num_tasks:
				break
	  
		print "all tasks complete!"
