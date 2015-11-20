# -*- coding: utf-8 -*-

from distutils.core import setup
import py2exe
import requests.certs
import os
build_exe_options = {"include_files":[(requests.certs.where(),'cacert.pem')]}
os.environ["REQUESTS_CA_BUNDLE"] = os.path.join(os.getcwd(), "cacert.pem")
setup(console=['jodelpost.py'])
