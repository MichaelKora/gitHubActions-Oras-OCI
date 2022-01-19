import json
import urllib.request
import sys
import subprocess
import logging

import urllib.request
from functions import *

#argument: github Owner
owner = sys.argv[1]

#shell script to create the needed file structure for conda_index
subprocess.run("chmod +x ./prep_conda_index.sh", shell=True )

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
    subprocess.run("./prep_conda_index.sh", shell=True)

    #download every found packages (tar.bz2 files) of a specific subdir
    for pkg in found_packages:
        pkgLink = f"https://conda.anaconda.org/{chanel}/{subdir}/{pkg}"
        logging.warning(f"Downloading the tar.bz2 file from {pkgLink}")

        urllib.request.urlretrieve(pkgLink, filename=pkg)

        # change the name and adapt the tag
        len_pkg = len (pkgname)
        tag = pkg[len_pkg: ]

        extension = ".tar.bz2"
        len_extsn = len (extension)

        len_tag= len(tag) - len_extsn
        tag_resized = tag [1:len_tag]

        #replace all "_" with "-"
        tag_resized = tag_resized.replace("_", "-")
        logging.warning(f"The current tag is: <<{tag_resized}>>")

        # upload the tar_bz2 file to the right url
        push_bz2 = f"oras push ghcr.io/{owner}/samples/{subdir}{pkgname}/:{tag_resized} ./{pkg}:application/octet-stream"
        upload_url = f"ghcr.io/{owner}/samples/{subdir}/{pkgname}/:{tag_resized}"
        logging.warning(f"Uploading <<{pkg}>> to link: <<{upload_url}>>")
        subprocess.run(push_bz2, shell=True)
        logging.warning(f"Package <<{pkg}>> uploaded to: <<{upload_url}>>")

    #run "conda index" to update the repodata.json file
    subprocess.run("./run_conda_index.sh", shell=True)

    #upload the repodata.json file to the right url
    json_url = f"ghcr.io/{owner}/samples/{subdir}"
    push_json = f"oras push ghcr.io/{owner}/samples/{subdir} ./temp_dir/noarch/repodata.json:application/vnd.unknown.layer.v1+txt"
    logging.warning(f"Uploading repodata.json to <<{json_url}>>")
    subprocess.run(push_json, shell=True)
    logging.warning(f"File repodata.json upload to: <<{json_url}>>")


    # delete bz2 and temp_dir
    subprocess.run("./deletefiles.sh", shell=True)


#/<name>/<arch>/repodata.json
#und /<name>/<arch>/<package>
#<name> -> irgendein Name
#<arch> -> linux-64, osx-64, win-64, noarch
#und <package> wäre jetzt z.b. xtensor-0.20.4-h1231312.tar.bz2
