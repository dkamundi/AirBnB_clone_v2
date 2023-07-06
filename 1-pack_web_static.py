#!/usr/bin/python3
"""
This is a Fabric script that generates a .tgz archive from the contents of the web_static folder.
"""

from fabric.api import local
from datetime import datetime
from os import isdir

def do_pack():
    """
    Generates a .tgz archive from the contents of the web_static folder.

    Returns:
        str: Archive path if the archive has been correctly generated, None otherwise.
    """
    try:
        date = datetime.now().strftime("%Y%m%d%H%M%S")
        if isdir("versions") is False:
            local("mkdir versions")
        file_name = "versions/web_static_{}.tgz".format(date)
        local(("tar -cvzf {} web_static".format(file_name))
        return file_name
    except:
        return None
