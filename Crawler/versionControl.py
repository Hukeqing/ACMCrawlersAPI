import requests
import json
import webbrowser

version = "v2.0.0"
dataVersion = "2.0"
laterVersion = ""


def update():
    global laterVersion
    url = 'https://api.github.com/repos/Hukeqing/ACMCrawlersAPI/releases/latest'
    response = requests.get(url)
    versionData = json.loads(response.text)
    try:
        laterVersion = versionData['tag_name']
        if laterVersion != version:
            return True
    except Exception:
        return False
    return False


def get_new_version():
    if laterVersion == "":
        update()
    webbrowser.open('https://hukeqing.github.io/ACMCrawlersAPI/index.html')


def version_fun(argv):
    if argv[1] == 'download':
        pass
    elif argv[1] == 'install':
        pass
    elif argv[1] == 'uninstall':
        pass
    exit(0)


def data_version(data):
    return '{"version": "2.0","user": [' + data + ']}'
