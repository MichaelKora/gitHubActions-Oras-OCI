import json
import urllib.request
import sys
import subprocess
import logging
import os
#import stat
from datetime import datetime

import urllib.request
from functions import *

#initializations & make files executable
owner = sys.argv[1]
list_of_dirs = []
#subprocess.run("mkdir temp_dir", shell=True)
os.mkdir("temp_dir")
os.chmod("./rename_new_repo_files.sh", 0o777)
os.chmod("./upload_repodataFiles.sh", 0o777)

#subprocess.run("chmod +x ./rename_new_repo_files.sh", shell=True)
#subprocess.run("chmod +x ./upload_repodataFiles.sh", shell=True)

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

    repodata_exists = True
    pull_repo = f"oras pull ghcr.io/{owner}/samples/{subdir}/repodata.json:latest -t \"application/json\" -o ./temp_dir"
    result = subprocess.run(pull_repo, shell=True)

    repodata_exists = True
    if result.returncode != 0:
        repodata_exists = False

    if repodata_exists:
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
            #donwload package
            pkgLink = f"https://conda.anaconda.org/{channel}/{subdir}/{pkg}"
            logging.warning(f"Downloading the tar.bz2 file from {pkgLink}")
            if (os.path.isdir(f"./temp_dir/{subdir}") == False):
                logging.warning(f"Subdir <<{subdir}>> does not exist...Creating a new subdir in filesystem...>>")
                subprocess.run(f"mkdir ./temp_dir/{subdir}", shell=True)
                list_of_dirs.append(subdir)
            urllib.request.urlretrieve(pkgLink, f"./temp_dir/{subdir}/{pkg}")

            #get name, version and hash (tag = version + hash(without .tar.bz2 extension))
            name, version, hash = pkg.rsplit('-', 2)
            tag = version + "-" + hash
            tag_resized = tag.rpartition('.tar')[0]
            tag_resized = tag_resized.replace("_", "-")

            logging.warning(f"The current Pkg name is: <<{name}>>")
            logging.warning(f"The current tag is: <<{tag_resized}>>")

            # upload the tar_bz2 file to the right url
            push_bz2 = f"oras push ghcr.io/{owner}/samples/{subdir}/{name}:{tag_resized} ./temp_dir/{subdir}/{pkg}:application/octet-stream"
            upload_url = f"ghcr.io/{owner}/samples/{subdir}/{name}:{tag_resized}"
            logging.warning(f"Uploading <<{pkg}>> (from dir: << ./temp_dir/{subdir}/ >> to link: <<{upload_url}>>")
            subprocess.run(push_bz2, shell=True)
            logging.warning(f"Package <<{pkg}>> uploaded to: <<{upload_url}>>")

            #add pkg to my tracker
            if repodata_exists:
                already_uploaded_pkgs[subdir].append(pkg)
            else:
                already_uploaded_pkgs[subdir]=(pkg)


#rename all the downloaded repodata before creating new ones with << conda index >>
logging.warning(f"renaming old repo...")
subprocess.run("./rename_new_repo_files.sh", shell=True)

#run conda index to generate all new repodata.file
logging.warning(f"build new foud files...")
subprocess.run("conda index ./temp_dir", shell=True)


# iterate over updated subdirs
dir="temp_dir"
old_repodata_filename="old_repodata.json"
new_repodata="repodata.json"
for some_dir in os.listdir(dir):
#noarch
    if (os.path.isdir(some_dir) == True):
        # go only through directories

        f = os.path.join(dir, some_dir, old_repodata_filename)
        fnew = os.path.join(dir, some_dir, new_repodata)


        if os.path.isfile(fnew) and os.path.isfile(f):
            #see if there are two different versions of the repodata json within the subdir

            #merge both json
            with open(f, "r") as read_file:
                old_version_json = json.load(read_file)
            with open(fnew, "r") as read_file:
                newLocal_version_json = json.load(read_file)
            for new_pkg in newLocal_version_json["packages"]:
                old_version_json["packages"][new_pkg] = newLocal_version_json["packages"][new_pkg]

            latest_mirror_json = old_version_json


        elif os.path.isfile(fnew):
            with open(fnew, "r") as read_file:
                latest_mirror_json = json.load(read_file)

        with open(fnew) as write_file:
            json.dump(latest_mirror_json, write_file)



logging.warning(f"Uploading all repodata.json files...")

now = datetime.now()
json_tag = now.strftime("%d%m%Y%H%M%S")
subprocess.run(f"./upload_repodataFiles.sh {owner} {json_tag}", shell=True)

logging.warning(f" All repodata.json files uploaded !!!>>")
