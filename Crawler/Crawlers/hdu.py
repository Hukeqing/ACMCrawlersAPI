import requests
import re
from Crawler.basic import crawlerRes


def get_solved(username: str) -> crawlerRes:
    res = crawlerRes('hdu', username=username, sync=False)
    response = requests.get('http://acm.hdu.edu.cn/userstatus.php', params={'user': username})
    data = re.search(
        r'<tr><td>ProblemsSolved</td><tdalign=center>(?P<solved>\d+)</td></tr><tr><td>Submissions</td><tdalign=center>('
        r'?P<submissions>\d+)</td></tr>.+?<palign=left><scriptlanguage=javascript>(?P<submissionsList>.+?)</script><br></p><h3>',
        response.text.replace(' ', '').replace('\n', '').replace('\t', '').replace('\r', ''))
    res.set_solved(int(data.groupdict()['solved']))
    res.submissions = int(data.groupdict()['submissions'])
    # print(re.findall(r'p\(\d+,\d+,\d+\)', submissions.group()))
    for item in re.findall(r'p\(\d+,\d+,\d+\)', data.groupdict()['submissionsList']):
        res.add_solved_list(int(item[2:6]))
    # print(res.solved, res.submissions, len(res.submissions))
    return res


if __name__ == '__main__':
    ans = get_solved('GSDXHKQ')
    print(ans.get_solved(), ans.get_solved_lists(), sep='\n')
