import json

VERSION = None


with open('front/version.html') as f_version:
    VERSION = json.loads(f_version.read())

    BUILD_RELEASE = VERSION['build'].split('-')

    if len(BUILD_RELEASE) > 1:
        VERSION['build'] = "{}-{}".format(BUILD_RELEASE[0],
                                          int(BUILD_RELEASE[1]) + 1)
    else:
        VERSION['build'] = "{}".format(int(BUILD_RELEASE[0]) + 1)


with open('front/version.html', 'w') as f_version:
    f_version.write(json.dumps(VERSION, separators=(',', ':')))
