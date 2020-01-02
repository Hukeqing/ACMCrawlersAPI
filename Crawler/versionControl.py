import requests
import json
import webbrowser

version = "v1.1.1"
dataVersion = "1.0"
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
        exit(0)
    elif argv[1] == 'install':
        exit(0)
    elif argv[1] == 'uninstall':
        exit(0)
