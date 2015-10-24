#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import os
import cgi, cgitb

querys = cgi.FieldStorage()

name = querys.getvalue('name')

print "Content-type:text/html\r\n\r\n"
print ("<html><p>Hello, %s</p></html>" % name)

