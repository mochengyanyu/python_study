#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/19 23:12
# @Author  : wukun
# @Site    : 
# @File    : down_music.py
# @Software: PyCharm
import requests;
import time;
import json
from bs4 import BeautifulSoup
import re
from urllib import request;
import sys

# jQuery19106136019356729143这个东西好像cookies一样,需要改进,(只是猜测,获取cookies传入后再进行下载)

incout = int(round(time.time() * 1000))
search_url = 'https://songsearch.kugou.com/song_search_v2?callback=jQuery112409653710660132317_%s&keyword=%s'
down_url = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19106136019356729143_%s&hash=%s&album_id=%s&dfid=3du5Zy3cg0Ln0VBR0q2PiYyL&mid=f8f895dcd8032b943ef58c7763f5b917&platid=4&_=%s'
str_zz = '&dfid=3du5Zy3cg0Ln0VBR0q2PiYyL&mid=f8f895dcd8032b943ef58c7763f5b917&platid=4&_=1574177791834'
session = requests.session();
down_file = 'E:\\music\\sing';
count = 0;


def down_music(keyword):
    search_url_m = search_url %(str(incout),keyword);
    print(search_url_m)
    resp = session.get(
        url=search_url_m,
        headers={
            'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }
    )

    soup = BeautifulSoup(resp.text,features='html.parser');
    zz = re.findall('\{.*\}',str(soup));
    try:
        zz_item = zz[0]
    except IndexError as e:
        print('未找到歌曲信息')
        sys.exit(0)
    music_info_json = json.loads(zz_item);
    music_list = music_info_json['data']['lists'];
    down_sing_song(music_list,keyword,resp);
    # down_mutil_song(music_list,keyword,resp);

# 下载一首
def down_sing_song(music_list,keyword,resp):
    for music_item in music_list:
        print(str(music_item))
        hash = music_item['FileHash'];
        album_id = music_item['AlbumID'];
        down_music_url = down_url % (str(incout), hash, album_id, str(incout));
        music_down_info = session.get(
            url=down_music_url,
            headers={
                'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
            },
            cookies=resp.cookies,
        )
        soup_music = BeautifulSoup(music_down_info.text, features='html.parser');
        yy = re.findall('\{.*\}', str(soup_music));
        down_real_json = json.loads(yy[0]);
        down_real_url = down_real_json['data']['play_url'];
        if len(down_real_url) != 0:
            res = request.urlopen(down_real_url);
            while True:
                data = res.read();
                if not len(data):
                    break;
                with open(down_file + '\\' + keyword + '.mp3', 'wb') as test_sing:
                    test_sing.write(data);
                test_sing.close();
                print('下载完成');
            break;



# 下载多首歌曲
def down_mutil_song(music_list,keyword,resp):
    for music_item in music_list:
        hash = music_item['FileHash'];
        album_id = music_item['AlbumID'];
        down_music_url = down_url %(str(incout),hash,album_id,str(incout));
        music_down_info = session.get(
            url=down_music_url,
            headers={
                'User-Agent': 'user-agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
            },
            cookies = resp.cookies,
        )
        soup_music = BeautifulSoup(music_down_info.text, features='html.parser');
        yy = re.findall('\{.*\}',str(soup_music));
        down_real_json = json.loads(yy[0]);
        down_real_url = down_real_json['data']['play_url'];
        global count;
        if len(down_real_url)!=0:
            res = request.urlopen(down_real_url);
            while True:
                data = res.read();
                if not len(data):
                    break;
                with open(down_file+'\\'+keyword+'-'+str(count)+'.mp3','wb') as test_sing:
                    test_sing.write(data);
                test_sing.close();
            print('下载完成')
        count+=1;

if __name__ == '__main__':
    music_name = 'you belong with me'
    down_music(music_name)