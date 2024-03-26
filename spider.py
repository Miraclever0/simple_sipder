import urllib.request
from bs4 import BeautifulSoup
import re
from queue import *
from save2table import saveExcel,saveCsv
import json
import threading
# from tqdm import tqdm

url_queue = Queue()
detail_queue = Queue()
result = []
repeat_set = set()
lock = threading.Lock()

def getHtml(url):
    html = 0
    with urllib.request.urlopen(url) as response:
        html = response.read()
    return html

def getNextPage(html):
    next_page = ""
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        if link.get_text() == "下一页":
            next_page =link.get("href")
    return next_page

def getSubPage(html):
    detail_page = []
    soup = BeautifulSoup(html, 'html.parser')
    for link in soup.find_all('a'):
        link_str = link.get("href")
        if (type(link_str) != str):
            continue
        if re.search(r'www\.chinatruck\.org\/product\/truck\/\d+.+\.html$', link_str):
            detail_page.append(link_str)
    return detail_page

def getDetails(html):
    soup = BeautifulSoup(html, 'html.parser')
    detail_dict = {}
    table_div = soup.find_all('div')
    
    for temp_div in table_div:
        div_class = temp_div.get("class")
        if (type(div_class) != list):
            continue
        # print(div_class)
        if "car-name" in temp_div.get("class"):
            detail_dict["名称"] = temp_div.get_text()
        if "cspz-cont" in temp_div.get("class"):
            for temp_list in temp_div.find_all('li'):
                li_str = temp_list.get_text()
                if re.search(r'(.+)[:：] ?(.+)', li_str):
                    temp_key = re.sub(r'[:：] ?.+', '', li_str)
                    temp_value = re.sub(r'.+[:：] ?', '', li_str)
                    detail_dict[temp_key] = temp_value

    for prag in soup.find_all('p'):
        prag_str = prag.get_text()
        if re.search(r'(.+)[:：] ?(.+)', prag_str):
            temp_key = re.sub(r'[:：] ?.+', '', prag_str)
            temp_value = re.sub(r'.+[:：] ?', '', prag_str)
            detail_dict[temp_key] = temp_value
    return detail_dict

def remove_duplicate(temp_list):
    new_list = []
    for temp in temp_list:
        if temp not in new_list:
            new_list.append(temp)
    return new_list

def formatDetails(src_list, trg_dict):
    for temp_dict in src_list:
        for key in temp_dict.keys():
            trg_dict[key] = []
    for temp_dict in src_list:
        for key, value in trg_dict.items():
            if key in temp_dict:
                trg_dict[key].append(temp_dict[key])
            else:
                trg_dict[key].append("")

def getResult():
    detail_url = ""
    while(detail_queue.qsize() > 0):
        with lock:
            detail_url = detail_queue.get()
        if detail_url != "":
            print(detail_url)
            detail_html = getHtml(detail_url)
            temp_dict = getDetails(detail_html)
            result.append(temp_dict)
    return

if __name__ == "__main__":
    url = "https://www.chinatruck.org/product/s0_b0_t0_m0_e0_c1.html"
    url_queue.put(url)

    html = getHtml(url)
    temp_list = []
    result_list = []
    result_dict = {}
    next_page = url
    while (next_page not in repeat_set):
    # for i in range(0,1):
        repeat_set.add(next_page)
        sub_list = getSubPage(html)
        temp_list += sub_list
        next_page = getNextPage(html)
        html = getHtml(next_page)
        print("next_page: ", next_page)

    detail_list = remove_duplicate(temp_list)
    for detail_page in detail_list:
        detail_queue.put(detail_page)

    threads = []
    for i in range(0,10):
        t = threading.Thread(target=getResult)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    formatDetails(result, result_dict)
    saveCsv(result_dict, 'output.csv')