import json
import urllib.request

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

def compare2Lists ( newList, oldList):
    result = []
    for item in newList:
        if item not in oldList:
            result.append(item)
    return result
