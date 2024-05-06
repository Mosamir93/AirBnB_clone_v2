#!/usr/bin/python3
"""
A Fabric script  that distributes
an archive to web servers
"""

from fabric.api import local, run, env, put
import os.path

env.hosts = ['52.87.230.55', '100.25.150.51']
env.user = 'ubuntu'
env.key_filename = '~/.ssh/school'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers
    """
    if os.path.isfile(archive_path) is False:
        return False

    try:
        archive = archive_path.split('/')[-1]
        folder = archive.split('.')[0]
        deploy_path = "/data/web_static/releases/"
        tmp_path = "/tmp/"

        put(archive_path, tmp_path)
        run("mkdir -p {}{}/".format(deploy_path, folder))
        run("tar -xzf {}{} -C {}{}/".format(
            tmp_path, archive, deploy_path, folder))
        run("rm {}{}".format(
            tmp_path, archive))
        run("mv {}{}/web_static/* {}{}/".format(
            deploy_path, folder, deploy_path, folder))
        run("rm -rf {}{}/web_static".format(
            deploy_path, folder))
        run("rm -rf /data/web_static/current")
        run("ln -sf {}{}/ /data/web_static/current".format(
            deploy_path, folder))
        print("New version deployed!")
        return True
    except Exception:
        return False
