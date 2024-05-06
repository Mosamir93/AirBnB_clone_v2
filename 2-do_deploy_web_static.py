#!/usr/bin/python3
"""
Fabric script to deploy tgz archive
fab -f 2-do_deploy_web_static.py do_deploy:archive_path=filepath
    -i private-key -u user
"""

import os.path
from fabric.api import put, run, env

env.hosts = ['52.87.230.55', '100.25.150.51']


def do_deploy(archive_path):
    """
    copies archive file from local to my webservers
    """

    if not os.path.isfile(archive_path):
        return False
    try:
        file_name = archive_path.split("/")[-1].split(".")[0]
        full_path = "/data/web_static/releases/{}/".format(file_name)
        symlink = "/data/web_static/current"
        put(archive_path, "/tmp/")

        run("mkdir -p {}".format(full_path))

        run("tar -xzf /tmp/{}.tgz -C {}"
            .format(file_name, full_path))

        run("rm /tmp/{}.tgz".format(file_name))

        run(("mv {}web_static/* {}")
            .format(full_path, full_path))

        run("rm -rf {}web_static"
            .format(full_path))

        run("rm -rf {}").format(symlink)

        run(("ln -s {} {}")
            .format(full_path, symlink))
        return True
    except Exception:
        return False
