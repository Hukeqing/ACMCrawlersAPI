import requests
import re
from Crawlers.basic import crawlerRes


def get_solved(username, **kwargs):
    res = crawlerRes("hdu", False)
    response = requests.get("http://acm.hdu.edu.cn/userstatus.php", params={"user": username})
    # print(response.text)
    solved = re.search(r"<tr><td>Problems Solved</td><td align=center>(?P<solved>\d+)</td></tr>", response.text)
    res.set_solved(solved.groupdict()["solved"])
    submissions = re.search(r"<p align=left><script language=javascript>.+?</script><br></p>", response.text)
    # print(re.findall(r"p\(\d+,\d+,\d+\)", submissions.group()))
    for item in re.findall(r"p\(\d+,\d+,\d+\)", submissions.group()):
        res.add_submission(int(item[2:6]))
    # print(res.solved, res.submissions, len(res.submissions))
    return res


if __name__ == '__main__':
    ans = get_solved("GSDXHKQ")
    print(ans.get_solved(), ans.get_submissions(), sep='\n')
