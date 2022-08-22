## clean_images.py
### What is for?
This script should be used to clear images related to MSA and are not being
used in a running container.

If only one image is found for a particular container, no image will be
deleted.

### Install requirements
`$ pip install -r requirements.txt`

### Run clean command
`$ python clean_image.py`

## create_image
### What is for?
This script will tag images from a docker-compose file

`$ ./release_tag -f <docker-compose.yml> -t TAG_NAME [-p]`
