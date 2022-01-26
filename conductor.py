#import json
#import urllib.request
import sys
#import subprocess
#import logging
#import os
#import urllib.request
#from functions import *
from manager import *
#initializations
owner = sys.argv[1]
manager = Manager(owner)
list_of_dirs = []
os.mkdir("temp_dir")

channel = ""
subdir = ""
pkgname = ""
oldLink = ""
last_link = ""
latest_mirror_json = ""

#import json files
with open("input_file.json", "r") as read_file:
    input_data_json = json.load(read_file)

already_uploaded_pkgs = {}

#go through entire set of entries in the input_data.json file
for entry in input_data_json:
    channel = entry["channel"]
    subdir = entry["subdir"]

    manager.resetValues(channel, subdir)

    repodata_exists = True
    pull_repo = f"oras pull ghcr.io/{owner}/samples/{subdir}/repodata.json:latest -t \"application/json\""
    logging.warning(f"cmd {pull_repo} ")
    result = subprocess.run(pull_repo, shell=True)

    if result.returncode != 0:
        repodata_exists = False

    if repodata_exists:
        subprocess.run("pwd", shell=True)
        subprocess.run(f"ls -al", shell=True)

        logging.warning("ls tempdir")
        subprocess.run(f"ls -al ./temp_dir", shell=True)

        logging.warning("ls tempdir/subdir")
        subprocess.run(f"ls -al ./temp_dir/{subdir}", shell=True)
        with open(f"./temp_dir/{subdir}/repodata.json", "r") as read_file:
            current_repodata = json.load(read_file)
        for key_pkg in current_repodata["packages"]:
            if key_pkg in already_uploaded_pkgs:
                already_uploaded_pkgs[subdir].append(key_pkg)
            else:
                already_uploaded_pkgs[subdir] = []
                already_uploaded_pkgs[subdir].append(key_pkg)

#see if there is already something on the registry that can pulled
    subdir_already_exists = True

    newLink = f"https://conda.anaconda.org/{channel}/{subdir}/repodata.json"
    downloaded_repodata_dic = downloadFile(oldLink, newLink)
    pkgname = entry ["package"]

    found_packages = set (findPackages(downloaded_repodata_dic, pkgname))


    #subdir has some pkgs already downloaded the last time
    if subdir in already_uploaded_pkgs:
        last_uploaded_pkgs_for_subdir = set (already_uploaded_pkgs[subdir])
        new_packages_set = found_packages - last_uploaded_pkgs_for_subdir

    #the subdir is new and havent been uploaded the last time
    else:
        new_packages_set = found_packages

    if not len(new_packages_set):
        logging.warning(f"no new packages for {subdir} ")
    else:
        logging.warning(f"new packages found for {subdir}")

        for pkg in new_packages_set:
            #reset package name
            manager.resetPkg(pkg)

            #download
            manager.downloadbz2()

            #get push package to registry
            manager.push_pkg()

            #add pkg to my tracker
            if repodata_exists:
                already_uploaded_pkgs[subdir].append(pkg)
            else:
                already_uploaded_pkgs[subdir]=(pkg)


#rename all the downloaded repodata before creating new ones with << conda index >>
manager.prepare()

# push updated repodata files
manager.push_repodata()
