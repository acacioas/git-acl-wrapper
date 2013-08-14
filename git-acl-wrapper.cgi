#!/usr/bin/env python

# 
# git-acl-wrapper
# 
# This python cgi script lets you control per base-url (project) and per repositories acls
# when you're deploying git over git "smart http" protocol (under apache)
# 
# It's based on xrunhprof wrapper for git-http-backend
# http://xrunhprof.wordpress.com/2010/06/01/trac-and-git-http-backend/
# 
#
# For instructions, please, read README file.
#

import os
import subprocess
import csv
import re

# CentOS/RedHat default, please set it to your own git-http-backend path
GIT_HTTP_BACKEND = '/usr/libexec/git-core/git-http-backend'

# environment variables 
remote_user = os.environ.get('REMOTE_USER')
script_name = os.environ.get('SCRIPT_NAME')
path_info = os.environ.get('REQUEST_URI')
git_project_root = os.environ.get('GIT_PROJECT_ROOT')

# repository variables
path_info = path_info[ len(script_name): ]
project_name = path_info.split("/")[1]
repos_name = path_info.split("/")[2]
is_writing = path_info.endswith("git-receive-pack")

valid_user = False
try:
    # check if is there an acl.conf file for project and for repository
    # if both of them exists, *ONLY* repository file is considered
    repos_acl_file = "%s/%s/%s/acl.conf" % (git_project_root, project_name, repos_name)
    project_acl_file = "%s/%s/acl.conf" % (git_project_root, project_name)
    if os.path.isfile(repos_acl_file):
        acl_file = repos_acl_file
    else:
        acl_file = project_acl_file
    
    # reading acl csv file
    reader = csv.reader(open(acl_file, "rb"), delimiter=',')
    
    # check if remote user is listed in acl file and if it has rw or only r permission
    for l in reader:
        if len(l) == 2 and (remote_user == l[0].strip() or l[0].strip() == '*') and ( (l[1].strip() == 'r' and not is_writing) or l[1].strip() == 'rw'):
            valid_user = True
            break
    
except IOError:
    pass

if valid_user:
    # call git-http-backend if everything is ok
    subprocess.call([GIT_HTTP_BACKEND])
else:
    # default behavior is to deny anything that is not a valid user
    print "Content-type: text/html"
    print "Status: 403 Forbidden\n"
    print "The user %s is not allowed to access this path." % str(remote_user)

