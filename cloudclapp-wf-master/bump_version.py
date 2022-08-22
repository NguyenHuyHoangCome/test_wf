import json

VERSION = None


with open('version.html') as c_version:
    VERSION = json.loads(c_version.read())

    BUILD_RELEASE = VERSION['build'].split('-')

    if len(BUILD_RELEASE) > 1:
        VERSION['build'] = "{}-{}".format(BUILD_RELEASE[0],
                                          int(BUILD_RELEASE[1]) + 1)
    else:
        VERSION['build'] = "{}".format(int(BUILD_RELEASE[0]) + 1)


with open('version.html', 'w') as c_version:
    c_version.write(json.dumps(VERSION, separators=(',', ':')))
