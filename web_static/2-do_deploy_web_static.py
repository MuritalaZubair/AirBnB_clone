#!/usr/bin/python3

from fabric.api import run, put, env

env.hosts = ['<server_ip_1>', '<server_ip_2>']

def do_deploy(archive_path):
    if not os.path.exists(archive_path):
        return False

    try:
        file_name = archive_path.split("/")[-1]
        no_ext = file_name.split(".")[0]
        dest = "/data/web_static/releases/"

        put(archive_path, f"/tmp/{file_name}")
        run(f"mkdir -p {dest}{no_ext}/")
        run(f"tar -xzf /tmp/{file_name} -C {dest}{no_ext}/")
        run(f"rm /tmp/{file_name}")
        run(f"mv {dest}{no_ext}/web_static/* {dest}{no_ext}/")
        run(f"rm -rf {dest}{no_ext}/web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {dest}{no_ext}/ /data/web_static/current")
        return True
    except:
        return False
