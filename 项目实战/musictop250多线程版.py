import requests
from bs4 import BeautifulSoup
import csv
import time
from tqdm import tqdm
from threading import Thread,Lock

'''
函数式写：
1.取url
2.解析url
3.保存文件
'''
base_url='https://music.douban.com/top250?start='
headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:80.0) Gecko/20100101 Firefox/80.0"}
urls=[base_url+str(x) for x in range(0,100,25)]

lock1=Lock()
lock2=Lock()

f=open('mu250.csv','a',encoding='utf-8')
writer=csv.writer(f)
def getUrl():
    global urls
    lock1.acquire()
    if urls==[]:
        lock1.release()
        return ''
    else:
        url=urls[0]
        del urls[0]
    lock1.release()
    return url

def get_html_content(url):
    html = requests.get(url=url, headers=headers).content
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find_all('table')
    for item in table:
        title = item.find_all(name='a', attrs={'class': 'nbg'})[0].get('title').split('-')[-1]
        s = item.find_all(name='p', attrs={'class': 'pl'})[0].text.split('/')
        s.insert(0, title)
    return s
def SaveContent(s):
    writer.writerow(s)

#TODO 线程是怎么具体运行的
#之前的多线程都是整个的函数，而这次的多线程是要只针对到某个环节
#这个是怎么写呢？
#这里有一个前提就是：只要url列表不为空，那么线程会一直执行整个流程：取url,解析url,存储数据
#python作者是用类来解决的(不知道合理性有多大，还是只是为了凑一个演示过程)
#我打算用一个函数
def all_over():
    url=getUrl()
    while url!='':
        s=get_html_content(url)
        SaveContent(s)

def main():
    t1=Thread(target=all_over)
    t2=Thread(target=all_over)
    t3=Thread(target=all_over)
    t4=Thread(target=all_over)
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()

if __name__ == '__main__':
    main()

