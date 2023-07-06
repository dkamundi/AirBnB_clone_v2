#!/usr/bin/python3
"""
Fabric script based on the file 2-do_deploy_web_static.py that creates and distributes an archive to web servers.
"""

from fabric.api import env, put, run, local
from datetime import datetime
from os.path import exists, basename, splitext

env.hosts = ['100.27.10.107', '100.26.255.78']
env.user = 'ubuntu'


def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if the archive has been correctly generated, None otherwise.
    """
    now = datetime.now()
    archive_name = "web_static_" + now.strftime("%Y%m%d%H%M%S") + ".tgz"
    archive_path = "versions/" + archive_name

    local("mkdir -p versions")
    result = local("tar -czvf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path of the archive to be distributed.

    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to /data/web_static/releases/<archive filename without extension> on the web server
        archive_filename = basename(archive_path)
        archive_name = splitext(archive_filename)[0]
        release_path = "/data/web_static/releases/{}".format(archive_name)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {} {}/".format(archive_filename, release_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the uncompressed folder to the release_path
        run('mv {0}/{1}/web_static/* {0}/{1}/'.format(release_path, archive_name))

        # Remove the empty web_static folder
        run("rm -rf {}/web_static".format(release_path))

        # Delete the symbolic link /data/web_static/current from the web server
        run("rm -rf /data/web_static/current")

        # Create a new symbolic link /data/web_static/current linked to the new version of your code
        run("ln -s {} /data/web_static/current".format(release_path))

        return True

    except Exception as e:
        print("Exception occurred: {}".format(e))
        return False


def deploy():
    """
    Creates and distributes an archive to web servers.

    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    archive_path = do_pack()
    if not archive_path:
        return False
    return do_deploy(archive_path)

