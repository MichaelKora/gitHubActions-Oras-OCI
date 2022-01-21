import json
import urllib.request
import sys
import subprocess
import logging
import os
from datetime import datetime

import urllib.request
from functions import *

#initializations & make files executable
owner = sys.argv[1]
list_of_dirs = []
subprocess.run("mkdir temp_dir", shell=True)
subprocess.run("chmod +x ./conda_index_create.sh", shell=True )
subprocess.run("chmod +x ./run_conda_index.sh", shell=True)
subprocess.run("chmod +x ./rename_new_repo_files.sh", shell=True)

chanel = ""
subdir = ""
pkgname = ""
oldLink = ""
last_link = ""
latest_mirror_json = ""
#latest_packages = {}

#import json files
with open("input_file.json", "r") as read_file:
    input_data_json = json.load(read_file)

with open("current_state.json", "r") as read_file:
    already_uploaded_pkgs = json.load(read_file)


#go through entire set of entries in the input_data.json file
for entry in input_data_json:
    chanel = entry["chanel"]
    subdir = entry["subdir"]

#see if there is already something on the registry that can pulled
    subdir_already_exists = True
    #get packages of this subdir which are already uploaded
# uploaded_pkg = already_uploaded_pkgs[subdir]

    newLink = f"https://conda.anaconda.org/{chanel}/{subdir}/repodata.json"
    downloaded_repodata_dic = downloadFile(oldLink, newLink)

    pkgname = entry ["package"]

    found_packages = set (findPackages(downloaded_repodata_dic, pkgname))


    #subdir has some pkgs already downloaded the last time
    if subdir in already_uploaded_pkgs.keys():
        last_uploaded_pkgs_for_subdir = set (already_uploaded_pkgs[subdir])
        new_packages_set = found_packages - last_uploaded_pkgs_for_subdir

    #the subdir is new and havent been uploaded the last time
    else:
        new_packages_set = found_packages
        subdir_already_exists = False

    if not len(new_packages_set):
        logging.warning(f"no new packages for {subdir} ")
    else:
        logging.warning(f"new packages found for {subdir}")

        #for new_pkg in new_packages_set:
        #    already_uploaded_pkgs[subdir].append(new_pkg)


        for pkg in new_packages_set:
            #donwload package
            pkgLink = f"https://conda.anaconda.org/{chanel}/{subdir}/{pkg}"
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
            #add the upoaded packet in my local tracker
            already_uploaded_pkgs[subdir].append(new_pkg)

    if subdir_already_exists:
    #pull latest version of the repodata
        pull_repo = f"oras pull ghcr.io/{owner}/samples/{subdir}/repodata.json:latest -t \"application/json\" -o ./temp_dir"
    #oras pull ghcr.io/michaelkora/samples/linux-aarch64/repodata.json:20.01.2022-11.18.59 -t "application/json"
        subprocess.run(pull_repo, shell=True)

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

        f = os.path.join(directory, filename, old_repodata_filename)
        fnew = os.path.join(directory, filename, new_repodata)


        if os.path.isfile(fnew) and os.path.isfile(f):
            #see if there are two different versions of the repodata json within the subdir

            #merge both json
            with open(f, "r") as read_file:
                old_version_json = json.load(read_file)
            with open(fnew, "r") as read_file:
                newLocal_version_json = json.load(read_file)
            for new_pkg in newLocal_version_json["packages"].keys():
                old_version_json["packages"][new_pkg] = newLocal_version_json["packages"][new_pkg]

            latest_mirror_json = old_version_json


        elif os.path.isfile(fnew):
            with open(fnew, "r") as read_file:
                latest_mirror_json = json.load(read_file)

        with open("repodata.json", "w") as write_file:
            json.dump(latest_mirror_json, write_file)





logging.warning(f"Uploading all repodata.json files...")
noarch_needed = "no"
if 'noarch' in list_of_dirs :
    print("Yes,  package <noarch> exists : " , list_of_dirs)
    noarch_needed = "yes"

#json_tag=""
now = datetime.now()
json_tag = now.strftime("%d%m%Y%H%M%S")
subprocess.run(f"./run_conda_index.sh {owner} {json_tag} {noarch_needed}", shell=True)

logging.warning(f" All repodata.json files uploaded !!!>>")
