# gitHubActions-Oras-OCI
This project is about dowloading packages; building them using conda-index and uploading both of the repodata.json file and the downloaded packages.
The package has to be on https://conda.anaconda.org/.

To do so you just have to add the details of the package in the input_file.json data and the push the modifications to your GitHub repository.
This pipeline is using GitHub actions and is triggered after you push the your modifications.

Here some Hints:
	#git push
		git add .
		git commit -m"comment"
		git push
