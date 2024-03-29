import json
import subprocess
import urllib.request
import os
import logging

#download the repodata.json file only if its a new one
def downloadFile (oldLink, newLink):
    if newLink != oldLink:
        with urllib.request.urlopen(newLink) as url:
            somedata = json.loads(url.read().decode())

        with open("repodata.json", "w") as write_file:
            json.dump(somedata, write_file)

    oldLink = newLink
    return somedata


#this funtion copie all the packages matching with the given package name from the repodata
#take the deserialized json file and the (part of the) package name  to search
def findPackages (input_data, pkg):
    found_packages = []
    for key in input_data["packages"].keys():
        if pkg in key:
            found_packages.append(key)

    return found_packages

def upload_repodataFiles(owner, tag):

    latest= "latest"
    for subdir in os.listdir("./temp_dir"):

        repodata = os.path.join("./temp_dir", subdir, "repodata.json")
        path_subdir = os.path.join("./temp_dir", subdir)

        if os.path.isdir(path_subdir) and os.path.isfile(repodata):
            upload_cmd = f"oras push ghcr.io/{owner}/samples/{subdir}/repodata.json:{tag} {repodata}:application/json"
            upload_cmd_latest = f"oras push ghcr.io/{owner}/samples/{subdir}/repodata.json:{latest} {repodata}:application/json"

            logging.warning(f"Uploading repodata to <<ghcr.io/{owner}/samples/{subdir}/repodata.json:{tag}>> ")
            subprocess.run(upload_cmd, shell=True)
            logging.warning("uploaded")

            logging.warning(f"Uploading the same repo with the tag <latest>")
            subprocess.run(upload_cmd_latest, shell=True)
            logging.warning("uploaded")


def rename_new_repo_files():
    file = "repodata.json"
    newName = "old_repodata.json"
    for subdir in os.listdir("./temp_dir"):
        repodata = os.path.join("./temp_dir", subdir, file)
        renamedFile = os.path.join("./temp_dir", subdir, newName)
        if os.path.isfile(repodata):
            os.rename (repodata, renamedFile)
