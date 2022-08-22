"Clean Image"

import argparse

import docker


def show_message(message, image_list):
    """
    Show message
    """
    print("==========")
    print(message)
    for i in image_list:
        print("- {}".format(i))

    if not image_list:
        print('No images found.')


def main(image_name, dont_ask_confirmation):
    """Main"""
    client = docker.from_env()

    if not image_name:
        images = {
            "ubiqube/msa2-bud": {},
            "ubiqube/msa2-db": {},
            "ubiqube/msa2-ui": {},
            "ubiqube/msa2-front": {},
            "ubiqube/msa2-sms": {},
            "ubiqube/msa2-api": {},
            "ubiqube/msa2-es": {},
            "ubiqube/msa2-alarm": {},
            "ubiqube/msa2-ai-ml": {},
            "ubiqube/msa2-kibana": {},
            "ubiqube/msa2-linuxme": {},
            "ubiqube/msa2-cerebro": {},
            "ubiqube/msa2-linuxdev": {}
        }
    else:
        images = {image_name: {}}

    for image_tag in images:
        images[image_tag]["images"] = client.images.list(name=image_tag)

        if len(images[image_tag]["images"]) < 2 and not image_name:
            print(('Images from tag: {}, have only one '
                   'image and will not be deleted').format(image_tag))

        images[image_tag]["container"] = None

        for name_container in client.containers.list(all=True):
            if image_tag in name_container.image.tags[0]:
                images[image_tag]['container'] = name_container

    image_list = {"to_delete": [], "to_keep": []}

    for image_tag in images:
        for i in images[image_tag]['images']:

            if not i.tags:
                continue

            if images[image_tag]['container'] is None or \
                    i.tags[0] not in images[image_tag]['container'].image.tags:
                image_list['to_delete'].append(i.tags[0])
            else:
                image_list['to_keep'].append(i.tags[0])

    show_message('Images to delete: ', image_list['to_delete'])
    show_message('Images being used by container: ', image_list['to_keep'])

    if image_list['to_delete']:
        show_message('Images to be deleted: ', image_list['to_delete'])

        response = 'No'

        if dont_ask_confirmation:
            response = 'yes'
        else:
            response = input(('Do you wish to continue and delete those'
                              'images? [y/N]: '))

        if response.lower() in ['yes', 'y']:
            print('Removing images...')
            for i in image_list['to_delete']:
                print("- {}".format(i))
                client.images.remove(i)
        else:
            print("==========")
            print('No images were deleted.')

    else:
        print("==========")
        print('Found no images to be deleted.')


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser(description='Clean image tool.')
    PARSER.add_argument('-y', '--yes',
                        help='Clean images without confirmation',
                        action='store_true',
                        default=False)
    PARSER.add_argument('-i', '--image', nargs='?',
                        help="Image name without tag",
                        required=False, default=None)
    ARGS = PARSER.parse_args()

    main(ARGS.image, ARGS.yes)
