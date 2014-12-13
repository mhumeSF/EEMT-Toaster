#!/usr/bin/python

import urllib2, os, sys

url = sys.argv[1]
filename = url.split('/')[-1]

req_info = urllib2.urlopen('http://uanow.org/ISTA-420-Midterm/gooey/index.html')
req_info.headers.keys()

contentLength = req_info.headers['content-length']

fileSize = os.path.getsize(filename)

print "Length: " + str(contentLength)
print "Size: " + str(fileSize)
if(int(contentLength) == int(fileSize)):
    print "Hoo-ray!"
else:
    print "BoOoOoOo..."