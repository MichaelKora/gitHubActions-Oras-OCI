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

#shell script to create the needed file structure for conda_index
subprocess.run("chmod +x ./conda_index_create.sh", shell=True )

#shell script that actually run the conda index command
subprocess.run("chmod +x ./run_conda_index.sh", shell=True )

#delete files after running it
subprocess.run("chmod +x ./deletefiles.sh", shell=True)

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

    #run conda script to move the tar.bz2 file in the proper place
    #and then run the "conda index" to produce the repodata.json
#2    if (print (os.path.isdir(f"temp_dir/{subdir}")) == True):
#2       subprocess.run(f"./conda_index_create.sh {subdir}", shell=True)


    for pkg in found_packages:
        #donwload package
        pkgLink = f"https://conda.anaconda.org/{chanel}/{subdir}/{pkg}"
        logging.warning(f"Downloading the tar.bz2 file from {pkgLink}")
        if (os.path.isdir(f"./temp_dir/{subdir}" == False):
            subprocess.run(f"mkdir ./temp_dir{subdir}", shell=True)
        urllib.request.urlretrieve(pkgLink, f"./temp_dir/{subdir}/{pkg}")
#        urllib.request.urlretrieve(pkgLink, filename=pkg)

        #get name, version and hash (tag = version + hash(without .tar.bz2 extension))
        name, version, hash = pkg.rsplit('-', 2)
        tag = version + "-" + hash
        tag_resized = tag.rpartition('.tar')[0]
        tag_resized = tag_resized.replace("_", "-")

        logging.warning(f"The current Pkg name is: <<{name}>>")
        logging.warning(f"The current tag is: <<{tag_resized}>>")

        # upload the tar_bz2 file to the right url
        push_bz2 = f"oras push ghcr.io/{owner}/samples/{subdir}/{name}:{tag_resized} ./{pkg}:application/octet-stream"
        upload_url = f"ghcr.io/{owner}/samples/{subdir}/{name}:{tag_resized}"
        logging.warning(f"Uploading <<{pkg}>> to link: <<{upload_url}>>")
        subprocess.run(push_bz2, shell=True)
        logging.warning(f"Package <<{pkg}>> uploaded to: <<{upload_url}>>")

    #run "conda index" to update the repodata.json file
    #subprocess.run("./run_conda_index.sh", shell=True)

    #upload the repodata.json file to the right url
#json_url = f"ghcr.io/{owner}/samples/{subdir}:1.0"
#push_json = f"oras push ghcr.io/{owner}/samples/{subdir}/repodata.json:1.0 ./temp_dir/noarch/repodata.json:application/vnd.unknown.layer.v1+txt"
logging.warning(f"Uploading all repodata.json files to...")
#subprocess.run(push_json, shell=True)

now = datetime.now()
json_tag = dt_string = now.strftime("%d.%m.%Y-%H.%M.%S")
subprocess.run(f"./deletefiles.sh {owner} {json_tag}", shell=True)

logging.warning(f" All repodata.json files uploaded !!!>>")


    # delete bz2 and temp_dir
#    subprocess.run("./deletefiles.sh", shell=True)
