import json
import urllib.request
import sys
import subprocess
import logging
import os
from datetime import datetime

import urllib.request
from functions import *

#argument: github Owner
owner = sys.argv[1]
list_of_dirs = []
#shell script to create the needed file structure for conda_index
subprocess.run("chmod +x ./conda_index_create.sh", shell=True )

#delete files after running it
subprocess.run("chmod +x ./run_conda_index.sh", shell=True)

chanel = ""
subdir = ""
pkgname = ""
oldLink = ""
last_link = ""
with open("input_file.json", "r") as read_file:
    input_data = json.load(read_file)

subprocess.run("mkdir temp_dir", shell=True)

#go through entire set of entries in the input_data.json file
for entry in input_data:
    chanel = entry["chanel"]
    subdir = entry["subdir"]

    newLink = f"https://conda.anaconda.org/{chanel}/{subdir}/repodata.json"
    downloaded_repodata = downloadFile(oldLink, newLink)

    pkgname = entry ["package"]

    found_packages = findPackages(downloaded_repodata, pkgname)


    for pkg in found_packages:
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

logging.warning(f"Uploading all repodata.json files to...")

noarch_needed = "no"
if 'noarch' in list_of_dirs :
    print("Yes,  package <noarch> exists : " , list_of_dirs)
    noarch_needed = "yes"

#json_tag=""
now = datetime.now()
json_tag = now.strftime("%d%m%Y%H%M%S")
subprocess.run(f"./run_conda_index.sh {owner} {json_tag} {noarch_needed}", shell=True)

logging.warning(f" All repodata.json files uploaded !!!>>")
