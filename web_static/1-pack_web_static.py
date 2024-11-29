#!/usr/bin/python3

from fabric.api import local
from datetime import datetime
import os

def do_pack():
    try:
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = f"versions/web_static_{timestamp}.tgz"

        if not os.path.exists("versions"):
            os.makedirs("versions")

        local(f"tar -cvzf {archive_path} web_static")
        return archive_path
    except Exception as e:
        return None
