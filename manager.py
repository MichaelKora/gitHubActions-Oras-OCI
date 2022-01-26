from functions import *

class Manager:
    def __init__(self, owner):
        self.owner = owner
        self.channel = ""
        self.subdir = ""
        self.pkg = ""

    def resetValues(channel,subdir):
        self.channel = channel
        self.subdir = subdir

    def resetPkg(pkg):
        self.pkg = pkg

    def downloadbz2 ():
        #donwload package
        pkgLink = f"https://conda.anaconda.org/{self.channel}/{self.subdir}/{self.pkg}"
        logging.warning(f"Downloading the tar.bz2 file from {pkgLink}")
        if (os.path.isdir(f"./temp_dir/{self.subdir}") == False):
            logging.warning(f"Subdir <<{self.subdir}>> does not exist...Creating a new subdir in filesystem...>>")
            subprocess.run(f"mkdir ./temp_dir/{self.subdir}", shell=True)
            list_of_dirs.append(self.subdir)
        urllib.request.urlretrieve(pkgLink, f"./temp_dir/{self.subdir}/{self.pkg}")

    def push_pkg():
        #get name, version and hash (tag = version + hash(without .tar.bz2 extension))
        name, version, hash = self.pkg.rsplit('-', 2)
        tag = version + "-" + hash
        tag_resized = tag.rpartition('.tar')[0]
        tag_resized = tag_resized.replace("_", "-")

        logging.warning(f"The current Pkg name is: <<{name}>>")
        logging.warning(f"The current tag is: <<{tag_resized}>>")

        # upload the tar_bz2 file to the right url
        push_bz2 = f"oras push ghcr.io/{self.owner}/samples/{self.subdir}/{name}:{tag_resized} ./temp_dir/{self.subdir}/{self.pkg}:application/octet-stream"
        upload_url = f"ghcr.io/{self.owner}/samples/{self.subdir}/{name}:{tag_resized}"
        logging.warning(f"Uploading <<{self.pkg}>> (from dir: << ./temp_dir/{self.subdir}/ >> to link: <<{upload_url}>>")
        subprocess.run(push_bz2, shell=True)
        logging.warning(f"Package <<{self.pkg}>> uploaded to: <<{upload_url}>>")

    def prepare():
        #rename all the downloaded repodata before creating new ones with << conda index >>
        logging.warning(f"renaming old repo...")
        #subprocess.run("./rename_new_repo_files.sh", shell=True)
        rename_new_repo_files()
        #run conda index to generate all new repodata.file
        logging.warning(f"build new foud files...")
        subprocess.run("conda index ./temp_dir", shell=True)

    def push_repodata():
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
        upload_repodataFiles (self.owner, json_tag)
        #subprocess.run(f"./upload_repodataFiles.sh {owner} {json_tag}", shell=True)

        logging.warning(f" All repodata.json files uploaded !!!>>")
