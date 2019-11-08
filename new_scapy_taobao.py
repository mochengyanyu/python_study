#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/11/8 17:06
# @Author  : wukun
# @Site    : 
# @File    : new_scapy_taobao.py
# @Software: PyCharm

import requests
import re
import sys;
from bs4 import BeautifulSoup;
import json;

class tao_bao(object):

    def __init__(self,username):
        # 淘宝登录的URL
        self.login_url = "https://login.taobao.com/member/login.jhtml"
        # 登陆前的验证,以获取cookie用于后续的登陆操作
        self.st_url = 'https://login.taobao.com/member/vst.htm?st={st}'
        # 淘宝登陆用户名
        self.username = username
        #header信息  (设置几个基本就可以的了，没必要设置这么多)
        self.loginHeaders = {
            'Host':'login.taobao.com',
            'Connection':'keep-alive',
            'Content-Length':'3357',
            'Cache-Control':'max-age=0',
            'Origin':'https://login.taobao.com',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Content-Type':'application/x-www-form-urlencoded',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Referer':'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.6',
        }
        #可重复使用的ua,可以使用抓包软件在实现一次登陆之后获得
        self.ua = '121#qGdlkCr4Q8llVlmmxV1HllXYMahfKujV9lbvxeP5oOZAAbrn3gx5lwLYAcFfKujVllgm+aAZLPhHA3rnE9jIlwXYLa+xNvo9lGuYZ7pIKM9STQrJEmD5lwLYAcfdK5jVVmgY+zP5KMlVA3rnEkD5bwLYOcMYsOSs2QQVBIbvsbc9MtFPD0rOasVbbZ3glWfopCibkZ0T83Smbgi0CeIAFtZfkQWXnjxSpqLbCZeTM35O3piDkeHXmo60bZienqC9pCibCZ0T83BhbZs0keHaF9FbbZsbnjxSpXsbMqAT881abgi0CvIPB9vkCWE0qnG9ptnCC6748u/mZwwAYXG9t5c5YvqrBcstlQljAcvq9J572byqRbpQTvFGk0BNLRGnla9/w5c7oQhnVs8n9FB/6HJejcXN2/yHhPgzIMnsPZKUHr00I0zN+2QxWzjmorY0V9WJY63Wo7X8Ln6bWajGHY92/HUeoqJ3Cag1VKLfYnTRkDWeTEwBncMqEKSsvaYtjZAiOmWfAdkq1gHkn4Jcrz7N8oxjOk1OYN+Uad7p2HaSejvTWTKTFlOG62RgF+gdRyHn8lXUjwKuo68EVrRjo9JS2gpYjCzqaEFvS8p9vpl5qrT/0sd7YXh+tbLYkUkWrp3RsLVNxI7ltwebPyaAVAVh7rWiryrReqXZEuPor/mGuHNrQlAAG21p13pll6Q8a/5JpRtodWdgpT87gqscEixjIr3c8dkFHtd3ua+4hT4VdjBxo6Q4FtMTAzTX7Vrfp1Da6oXEpWwcfomzwjL8G7T0hhkPSYr7NR0weOtX6TMUoFef+qCpMeHre64CWArcgN3ZXkUDlkZPI64048RdgZbQmIfQR35MC4PCaIoV8SJOKbSpnpgZPSXC3xHXQbC7TYVIhf1cVftpNVmBwXNQ1fM5dtrnoye4nmIFLENEqdoZwf5D0oiEli560sJhzzep6TSkayr4FJgquvoNirmPCDYIdteW7tjB0snKcGReZbHkD2/Z8DNQy8ldjc81nHq6ZdaiD+CWf8TAxMDu0RkLgHQAkWkgukAK'
        #将你输入的密码经过算法计算后提交,暂时不知道如何从js中获取,只能用笨方法从正确登陆后的表单中提取了
        self.TPL_password2 = '7fa8d58e31d14ec66bcdf4b494e4335f641f864d99a037e93db9d106f39d3baf48aa0f0cb207c57dbaa923255d94b841c21d9bd8ebc4989f0cad70c78409e3d72a554bccddec8e73f6f36177cf3ca7caa73c17bf6330a19ffe9c2afb4dbaa9c8128efaf257883850a82adfda66bdba2f72ba0d7af3874224cc81b07102f4d916'
        #POST提交页面时所提交的表单数据
        self.post = {
            'TPL_username':self.username,
            'TPL_password': '',
            'ncoSig': '',
            'ncoSessionid': '',
            'ncoToken': '35afb8c178caecc65d4db8d0cdcf55cb63316049',
            'slideCodeShow': 'false',
            'useMobile': 'false',
            'lang': 'zh_CN',
            'newlogin': '0',
            'loginsite': '0',
            'TPL_redirect_url': "https://i.taobao.com/my_taobao.htm?",
            'from': 'tb',
            'fc': 'default',
            'style': 'default',
            'css_style': '',
            'keyLogin': 'false',
            'qrLogin': 'true',
            'newMini': 'false',
            'newMini2': 'false',
            'tid': '',
            'loginType': '3',
            'minititle': '',
            'minipara': '',
            'pstrong': '',
            'sign': '',
            'need_sign': '',
            'isIgnore': '',
            'full_redirect': '',
            'sub_jump': '',
            'popid': '',
            'callback': '',
            'guf': '',
            'not_duplite_str ': '',
            'need_user_id': '',
            'poy': self.TPL_password2,
            'gvfdcname': '10',
            'gvfdcre':'68747470733A2F2F6C6F67696E2E74616F62616F2E636F6D2F6D656D6265722F6C6F676F75742E6A68746D6C3F73706D3D61317A30392E322E3735343839343433372E372E3333633532653864725951795A5926663D746F70266F75743D7472756526726564697265637455524C3D6874747073253341253246253246627579657274726164652E74616F62616F2E636F6D25324674726164652532466974656D6C6973742532466C6973745F626F756768745F6974656D732E68746D253346',
            'from_encoding': '',
            'sub': '',
            'TPL_password_2':self.TPL_password2,
            'loginASR':'1',
            'loginASRSuc':'1',
            'allp': '',
            'oslanguage': 'zh-CN',
            'sr': '1920*1080',
            'osVer': 'windows|6.1',
            'naviVer': 'chrome|64.03282186',
            'osACN': 'Mozilla',
            'osAV': '5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36',
            'osPF': 'Win32',
            'appkey': '00000000',
            'nickLoginLink': '',
            'mobileLoginLink': 'https://login.taobao.com/member/login.jhtml?redirectURL=https://buyertrade.taobao.com/trade/itemlist/list_bought_items.htm?&useMobile=true',
            'showAssistantLink': '',
            'um_token': 'HV01PAAZ0b8705a865692b795aaf7d1b0022d8c0',
            'ua': self.ua
        }
        #设置cookie
        self.cookies = {}
        #请求登录
        print('-------请求登陆-------')

    def _get_st_token_url(self):
        response = requests.post(self.login_url, self.post, self.loginHeaders,cookies=self.cookies)
        content = response.content.decode('gbk')
        st_token_url_re = re.compile(r'<script src=\"(.*)\"><\/script>');
        match_url = st_token_url_re.findall(content)
        if match_url:
            st_token_url = match_url[0]
            return st_token_url
        else:
            print('请检查是否匹配成功')

    def _get_st_token(self):
        st_token_url = self._get_st_token_url();
        st_response = requests.get(st_token_url)
        st_response_content = st_response.content.decode('gbk')
        st_token_re = re.compile(r'"data":{"st":"(.+)"}')
        match_st_token_list = st_token_re.findall(st_response_content)
        if match_st_token_list:
            st = match_st_token_list[0]
            return st
        else:
            print('请检查是否匹配成功')


    def login_by_st(self):
        st = self._get_st_token()
        st_url =self.st_url.format(st=st)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
            'Host': 'login.taobao.com',
            'Connection': 'Keep-Alive'
        }
        response = requests.get(st_url, headers=headers)
        content = response.content.decode('gbk')
        # 这一步是必须要做的,获取cookies，为以后的访问做准备
        self.cookies = response.cookies
        # 检测结果，看是否登录成功
        pattern = re.compile('top.location.href = "(.*?)"', re.S)
        match = re.search(pattern, content)
        if match:
            print(u'登录网址成功')
            return match
        else:
            print(u'登录失败')
            return False

    def login(self):
        try:
            verified_url = self.login_by_st()
        except TimeoutError as e:
            print('链接超时');

    def visit_page(self,product_name):
        cookies = self.cookies;
        resp_page = requests.get(
            url = 'https://s.taobao.com/search?q=%s'%(product_name),
            cookies = cookies,
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:35.0) Gecko/20100101 Firefox/35.0',
                'Referer': 'https://login.taobao.com/member/login.jhtml',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Connection': 'Keep-Alive'
            }
        );
        soup = BeautifulSoup(resp_page.text,features='html.parser');
        script_list = soup.findAll("script");
        str_data='';
        for item in script_list:
            str_contex_data = re.findall('g_page_config = \{.*\}',str(item));
            if len(str_contex_data)!=0 :
                str_data = str_contex_data;

        new_str_list = re.findall('\{.*\}',str_data[0]);
        json_data = new_str_list[0];
        #转json格式
        json_data_new = json.loads(json_data);
        pro_list = json_data_new['mods']['itemlist']['data']['auctions'];
        with open('E:\\scapy\\test.txt', 'w',encoding='utf-8') as rd:
            for pro_item in pro_list:
                dict_data = dict(pro_item)
                if 'view_sales' in dict_data.keys():
                    str_rd = '店铺:%s 店铺地址: %s  产品名称:%s  category:%s 价格: %s  销量:%s  订单成交数 %s' %(pro_item['nick'],pro_item['item_loc'],pro_item['raw_title'],pro_item['category'],pro_item['view_price'],pro_item['comment_count'],pro_item['view_sales']);
                    print(str_rd)
                    rd.write(str_rd);
                else:
                    str_rd = '店铺:%s 店铺地址: %s  产品名称:%s  category:%s 价格: %s  销量:%s ' % (
                    pro_item['nick'], pro_item['item_loc'], pro_item['raw_title'], pro_item['category'],
                    pro_item['view_price'], pro_item['comment_count']);
                    print(str_rd);
                    rd.write(str_rd);
        rd.close();

if __name__ == '__main__':
    user_name = sys.argv[1];
    tb = tao_bao(user_name);
    tb.login();
    product_name = '女装';
    tb.visit_page(product_name);
