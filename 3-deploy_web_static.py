#!/usr/bin/python3
"""
This is a Fabric script that creates and distributes an archive to web servers using the deploy function.
"""

from fabric.api import env, run, put, local
from datetime import datetime
from os.path import exists
from fabric.api import put

env.hosts = ['<IP web-01>', '<IP web-02>']
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
        archive_filename = archive_path.split("/")[-1]
        archive_name = archive_filename.split(".")[0]
        release_path = "/data/web_static/releases/{}".format(archive_name)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}".format(archive_filename, release_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the uncompressed folder to the release_path
        run("mv {}/web_static/* {}".format(release_path, release_path))

        # Remove the empty web_static folder
        run("rm -rf {}/web_static".format(release_path))

        # Delete the current symbolic link
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

