#!/usr/bin/python3
"""
This is a Fabric script that generates a .tgz archive from the contents of the web_static folder.
"""

from fabric.api import local
from datetime import datetime
from os import exists

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if the archive has been correctly generated, None otherwise.
    """
    now = datetime.now()
    archive_name = "web_static_" + now.strftime("%Y%m%d%H%M%S") + ".tgz"
    archive_path = "versions/" + archive_name
    web_static_path = "web_static"
    
    if not exists(web_static_path):
        return None

    local("mkdir -p versions")
    result = local("tar -czvf {} web_static".format(archive_path))

    if result.succeeded:
        return archive_path
    else:
        return None
