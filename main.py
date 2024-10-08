import requests
import time
import re

# 全名 用來檢查是否登入成功
name = ''
# cookie
ccuSSO = ''
TGC = ''
JSESSIONID = ''
cookies = {'ccuSSO': ccuSSO, 'TGC': TGC, 'JSESSIONID': JSESSIONID}
# header
# UA必須跟瀏覽器一樣!!
useragent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
headers = {'User-Agent': useragent}
# url
portal_url = 'https://portal.ccu.edu.tw/sso_index.php'
ec2_url = 'https://portal.ccu.edu.tw/ssoService.php?service=./test_eCourse2.php&linkId=0037&para='
event_url = 'https://portal.ccu.edu.tw/ssoService.php?service=/test_Lib_iActivity_Apply.php&linkId=0060&para='
refresh_url = 'https://portal.ccu.edu.tw/ajax/refresh_time_ajax.php'
# session
session = requests.session()
session.cookies.update(cookies)
session.headers.update(headers)

while True:
    localtime = time.localtime()
    nowtime = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
    print(nowtime)
    refresh_session = session.post(refresh_url)
    portal = session.get(portal_url)
    portal_html = portal.content.decode('UTF-8')
    if re.search(name, portal_html):
        print('單一入口登入確認')
    else:
        print('單一入口被登出')
        print(session.cookies)
        # with open('writeSomeShit.txt', 'w', encoding='UTF-8') as f:
        # f.write(f'portal:  {nowtime}')
        # f.write(portal_html)
        break

    ec2 = session.get(ec2_url)
    ec2_html = ec2.content.decode('UTF-8')
    if re.search(name, ec2_html):
        print('EC2登入成功')
        print(f'MoodleSession: {session.cookies['MoodleSession']}')
    else:
        print('EC2登入失敗')
        print(session.cookies)
        # with open('writeSomeShit.txt', 'w', encoding='UTF-8') as f:
        # f.write(f'ec2:  {nowtime}')
        # f.write(ec2_html)
        break

    event = session.get(event_url)
    event_html = event.content.decode('UTF-8')
    if re.search(name, event_html):
        print('活動登入成功')
        print(f'sessionid: {session.cookies['sessionid']}')
    else:
        print('活動登入失敗')
        print(session.cookies)
        # with open('writeSomeShit.txt', 'w', encoding='UTF-8') as f:
        # f.write(f'event:  {nowtime}')
        # f.write(event_html)
        break

    time.sleep(500)

# ec2
# https://portal.ccu.edu.tw/ssoService.php?service=./test_eCourse2.php&linkId=0037&para=
# 活動
# https://portal.ccu.edu.tw/ssoService.php?service=/test_Lib_iActivity_Apply.php&linkId=0060&para=
