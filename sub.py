import os, sys, requests, time, re, zipfile
from bs4 import BeautifulSoup as bs

class Sub_Files_On_Internet:                             #subtitle files on the net
    def __init__(self,index, name, link):
        self.index=index
        self.title=name
        self.link=link
        #self.comments=cooments

class inFolder:
    """movies on my computer"""
    def __init__(self, name, modTime ):
        self.name=name
        self.Time=time.time()-modTime

def sort(y):
    """sort by newest"""

    for i in range(len(y)):
        for j in range(i+1, len(y)):
            if y[i].Time>y[j].Time:
                y[i], y[j]=y[j], y[i]




data=[]


movie=re.compile(r'.*\.(mp4|mkv|avi)')


for files in os.listdir(sys.argv[1]):

    if movie.search(files):
        x=inFolder(files, os.stat(sys.argv[1]+files).st_mtime )
        data.append(x)

sort(data)

for i in range(int(sys.argv[2])):
    print(data[i].name)



for i in range(int(sys.argv[2])):
    internet_Data=[]
    re=requests.get("http://subscene.com/subtitles/title?q="+data[i].name)              #uses subscene.com
    soup=bs(re.text, "html.parser" )

    internet=soup.find_all(class_="a1")

    num=0
    for link in internet:
        if link.a.span.contents[0].string.strip()=='English':
            num=num+1
            #Sub_Files_On_Internet
            internet_Data.append( Sub_Files_On_Internet(num, str(link.find_all('span')[1].contents[0]).strip() ,  link.find('a').get('href')))
            #2 is name, #3 is link

    print("\n")

    for j in range(10):
        print(internet_Data[j].index, end="  ")
        print(internet_Data[j].title)
    print("\n")

    a=int(input("      select any one   "))


    re2=requests.get("http://subscene.com"+internet_Data[a-1].link)
    soup2=bs(re2.text, "html.parser")
    download=soup2.find(class_="download").find('a').get("href")
    re3=requests.get("http://subscene.com"+download)

    playFile = open(sys.argv[1]+data[int(sys.argv[2])-1].name+".zip", 'wb')
    for chunk in re3.iter_content(100000):
        playFile.write(chunk)
    playFile.close()
    time.sleep(1)
    exampleZip = zipfile.ZipFile(sys.argv[1]+data[int(sys.argv[2])-1].name+".zip")
    exampleZip.extractall(sys.argv[1])
    exampleZip.close()
    os.unlink(sys.argv[1]+data[int(sys.argv[2])-1].name+".zip")


