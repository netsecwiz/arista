#!/usr/bin/python

import ssl
ssl._https_verify_certificates( False )

from jsonrpclib import Server

switch = Server( "https://spoonman:arista@10.0.0.1/command-api" )

response = switch.runCmds( 1, [ "show hostname" ] )

print "Test is successful."

