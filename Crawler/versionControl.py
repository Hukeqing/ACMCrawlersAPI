import requests
import json
import webbrowser

version = "v1.0.0"
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
    webbrowser.open('https://github.com/Hukeqing/ACMCrawlersAPI/releases/tag/' + laterVersion)
