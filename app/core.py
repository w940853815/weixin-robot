# -*- coding: utf-8 -*-
# coding=utf-8
__author__ = 'ruidong.wang@tsingdata.com'


import sys
sys.path.insert(0, "../")

import aiml

# The Kernel object is the public interface to
# the AIML interpreter.

k = aiml.Kernel()
# Use the 'learn' method to load the contents
# of an AIML file into the Kernel.
k.learn("/var/www/weixin-robot/app/cn-startup.xml")

# Use the 'respond' method to compute the response
# to a user's input string.  respond() returns
# the interpreter's response, which in this case
# we ignore.

k.respond("载入配置文件")
# Loop forever, reading user input from the command
# line and printing responses.
def respond(input):
    return k.respond(input=input)

