#!/usr/bin/python3
"""
A Fabric script that generates a .tgz archive
from the contents of the web_static folder
"""

from fabric.api import *
from datetime import datetime
import os.path

env.hosts = ['52.87.230.55', '100.25.150.51']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_pack():
    """
    Generates a .tgz archive from the
    contents of the web_static folder of
    your AirBnB Clone repo
    """
    now = datetime.now()
    file_name = "web_static_{}{}{}{}{}{}.tgz".format(
        now.year, now.month, now.day, now.hour, now.minute, now.second
    )
    local("mkdir -p versions")
    result = local("tar -cvzf versions/{} web_static".format(file_name))
    path = "versions/{}".format(file_name)
    if result.succeeded:
        return path
    else:
        return None


def do_deploy(archive_path):
    """copies archive file from local to webservers"""
    if os.path.isfile(archive_path) is False:
        return False
    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        full_path = "/data/web_static/releases/{}/".format(no_ext)
        symlink = "/data/web_static/current"
        put(archive_path, "/tmp/")
        run("mkdir -p {}".format(full_path))
        run("tar -xzf /tmp/{} -C {}".format(file_name, full_path))
        run("rm /tmp/{}".format(file_name))
        run("mv {}web_static/* {}".format(full_path, full_path))
        run("rm -rf {}web_static".format(full_path))
        run("rm -rf {}".format(symlink))
        run("ln -s {} {}".format(full_path, symlink))
        return True
    except Exception:
        return False


def deploy():
    """
    Deploys the archive to web servers
    """
    archive = do_pack()
    if archive is None:
        return False
    res = do_deploy(archive_path=archive)
    return res
