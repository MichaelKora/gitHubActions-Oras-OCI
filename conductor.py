import json
import urllib.request
import sys
import subprocess

import urllib.request
from functions import *

#github variables
owner = sys.argv[1]
#tocken = sys.argv[1]

#https://conda.anaconda.org/robostack-experimental/linux-aarch64/repodata.json
#https://conda.anaconda.org/$CHANNEL/$SUBDIR/repodata.json

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

    #download every found packages (tar.bz2 files)
    for pkg in found_packages:
        pkgLink = f"https://conda.anaconda.org/{chanel}/{subdir}/{pkg}"


        urllib.request.urlretrieve(pkgLink, filename=pkg)

        #run conda script to move the tar.bz2 file in the proper place
        #and then run the "conda index" to produce the repodata.json
        subprocess.run("chmod +x ./conda_index.sh", shell=True )
        subprocess.run("./conda_index.sh", shell=True)

        # change the name and adapt the tag
        len_pkg = len (pkgname)
        tag = pkg[len_pkg: ]

        extension = ".tar.bz2"
        len_extsn = len (extension)

        len_tag= len_pkg - len_extsn
        tag_resized = tag [:len_tag]

        #replace all "_" with "-"
        tag_resized = tag_resized.replace("_", "-")


        # upload the files(bz2 and the repodata) to the subdir and tag

            #bz2: oras push ghcr.io/{owner}/samples/{pkgname}:{tag_resized} ./{pkg}:application/octet-stream
        push_bz2 = f"oras push ghcr.io/{owner}/samples/{pkgname}:{tag_resized} ./{pkg}:application/octet-stream"
        subprocess.run(push_bz2, shell=True)

            #json oras push ghcr.io/{owner}/samples/{pkgname}:{tag_resized} ./temp_dir/noarch/repodata.json:application/vnd.unknown.layer.v1+txt
        push_json = f"oras push ghcr.io/{owner}/samples/{pkgname}:{tag_resized} ./temp_dir/noarch/repodata.json:application/vnd.unknown.layer.v1+txt"
        subprocess.run(push_json, shell=True)


        # delete bz2 and temp_dir
        subprocess.run("chmod +x ./deletefiles.sh", shell=True)
        subprocess.run("./deletefiles.sh", shell=True)
