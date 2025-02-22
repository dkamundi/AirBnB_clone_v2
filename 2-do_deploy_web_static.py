#!/usr/bin/python3
"""
This is a Fabric script that distributes an archive to web servers using do_deploy function.
"""

from fabric.api import env, put, run
import os.path


env.hosts = ['100.27.10.107', '100.26.255.78']
env.user = 'ubuntu'


def do_deploy(archive_path):
    """
    Distributes an archive to web servers.

    Args:
        archive_path (str): Path of the archive to be distributed.

    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, "/tmp/")

        # Uncompress the archive to /data/web_static/releases/<archive filename without extension> on the web server
        archive_filename = os.path.basename(archive_path)
        archive_name = os.path.splitext(archive_filename)[0]
        release_path = "/data/web_static/releases/{}".format(archive_name)
        run("mkdir -p {}".format(release_path))
        run("tar -xzf /tmp/{} -C {}/".format(archive_filename, release_path))

        # Delete the archive from the web server
        run("rm /tmp/{}".format(archive_filename))

        # Move the contents of the uncompressed folder to the release_path
        run('mv {0}{1}/web_static/* {0}{1}/'.format(release_path, archive_name))
        
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

