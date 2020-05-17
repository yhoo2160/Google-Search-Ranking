#SEO爬蟲
#python3
#需要BeautifulSoup4套件

import requests
from bs4 import BeautifulSoup
import time
import math

all_flag = 0
#下面這行設定要搜尋的關鍵字
key_word_list=["關鍵字1","關鍵字2","關鍵字3","關鍵字4","關鍵字5"]
#下面這行設定要匹配的目標網域(部分即可)
target_url="你家網頁的網域"
key_word_cnt = 0
all_res_list = []
sep = '&sa=U'

#外迴圈跑關鍵字
while all_flag == 0:
    res_list = []
    key_word = key_word_list[key_word_cnt]

    flag_stop = 0
    page = 0
    i = 0
    
    #內迴圈跑每個關鍵字的頁面
    while flag_stop == 0 :
        j = i
        page_index = page * 100
        addr = "https://www.google.com.tw/search?q="+key_word+"&num=100&start="+str(page_index)
        res = requests.get(addr)
        soup = BeautifulSoup(res.text, "lxml")

        #暫存並檢視搜尋結果
        for result in soup.find_all("h3", class_="r"):
            res_list.append([])
            res_list[i].append(i)
            
            try:
                res_list[i].append(result.find("a").get_text())
            except AttributeError:
                res_list[i].append("BLANK OR ERROR")
                print("text blank i="+str(i))
            
            try:
                #修改下面這行可以切換要比對網址或是其他欄位
                tmp_txt = result.find("a").get("href").replace("/url?q=","")
                tmp_txt2 = tmp_txt.split(sep, 1)[0]
                res_list[i].append(tmp_txt2)
                #判斷如果匹配目標網域的話就記錄到結果
                #並設定停止flag
                if tmp_txt.find(target_url) != -1:
                    flag_stop = 1
                    cnt = i
            except AttributeError:
                res_list[i].append("BLANK OR ERROR")
                print("herf blank i="+str(i))
            
            i = i + 1
    
        if (i == j):
            flag_stop = 1
        else:
            page = page + 1
        
        #time.sleep(3)

    #拼湊輸出文字
    if res_list[cnt][2].find(target_url) == -1 :
        rtn_text = ("總共:"+str(i)+"筆搜尋結果，未找到符合"+target_url+"網域的結果。")
        all_res_list.append([])
        all_res_list[key_word_cnt].append(key_word)
        all_res_list[key_word_cnt].append(rtn_text)
    else:
        res_page = math.floor(cnt/10)+1
        res_no = cnt + 1 - (res_page-1)*10
        rtn_text = ("在第"+str(res_page)+"頁，第"+str(res_no)+"筆。")
        all_res_list.append([])
        all_res_list[key_word_cnt].append(key_word)
        all_res_list[key_word_cnt].append(rtn_text)
        all_res_list[key_word_cnt].append(res_list[cnt][1])
        all_res_list[key_word_cnt].append(res_list[cnt][2])
        
    
    
    #輸出結果
    #也可以呼叫all_res_list[]取得較詳細的網頁標題與網址
    print(key_word+":"+rtn_text)
    
    if key_word_cnt == len(key_word_list) - 1:
        all_flag = 1
    else:
        key_word_cnt = key_word_cnt + 1
        #time.sleep(30)



