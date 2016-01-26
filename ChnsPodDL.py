from requests import session
from bs4 import BeautifulSoup
import re

#Code to grab most recent lesson page links
"""
pages = range(1, 22)
links_list = []

for page in pages:
    result = requests.get('https://chinesepod.com/library/latest/?page=' + str(page))
    c = result.content
    soup = BeautifulSoup(c, 'lxml')
    links = soup.find_all(href=re.compile("lessons"))[::2]
    for link in links:
        links_list.append(link.get('href')+'\n')

f = open("links_file.txt", 'wb')
for item in links_list:
    f.write(item.encode('utf-8'))
f.close()
"""

with open("links_file.txt", 'rb') as f:
    lesson_links = f.readlines()

payload = {
    'email': '...',
    'password': '...',
    'code': '',
    'url': ''
}

with session() as c:
    c.post('https://chinesepod.com/accounts/signin', data=payload)

for link in lesson_links:
    response = c.get('https://chinesepod.com' + link.strip())
    soup2 = BeautifulSoup(response.text, 'lxml')
    soupy = soup2.find(href=re.compile("chinesepod_"))
    name = soupy.get('href')
    file_name01 = name[name.find('chinesepod_'):].replace('pr.mp3', 'pb.mp3')
    file_name02 = file_name01.replace('pb.mp3', '.pdf')

    raw_dl_links = soup2.find_all(href=re.compile("redirect"))
    dl_links = [link.get('href') for link in raw_dl_links]

    m = c.get('https://chinesepod.com' + dl_links[1])
    with open('D:\Chinese\ChinesePod\Temp\\'+file_name01, "wb") as mp3:
        mp3.write(m.content)
    mp3.close()

    p = c.get('https://chinesepod.com' + dl_links[3])
    with open('D:\Chinese\ChinesePod\Temp\\'+file_name02, "wb") as pdf:
        pdf.write(p.content)
    pdf.close()