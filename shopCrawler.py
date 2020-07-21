#-*- coding:utf-8 -*-
from selenium import webdriver
import pyautogui
from bs4 import BeautifulSoup
import time
import json

search_keyword_array = ['강남구 네일샵', '강동구 네일샵', '서울 강서구 네일샵', '강북구 네일샵', '관악구 네일샵', '서울 구로구 네일샵',
                        '금천구 네일샵', '노원구 네일샵', '마포구 네일샵', '동대문구 네일샵', '도봉구 네일샵', '동작구 네일샵',
                        '서대문구 네일샵', '서초구 네일샵', '송파구 네일샵', '성북구 네일샵', '성동구 네일샵', '종로구 네일샵',
                        '중랑구 네일샵', '양천구 네일샵', '영등포구 네일샵', '은평구 네일샵']

# 내려받은 chromedriver의 위치
driver = webdriver.Chrome('./driver/chromedriver')

# 웹 자원 로드를 위해 3초까지 기다린다.
driver.implicitly_wait(3)

# url접근
driver.get('https://map.kakao.com')
driver.implicitly_wait(2)

shop_name_list = []
shop_addr_list = []
shop_hp_list = []

page_no = 1
result_json_array = []

max_point = len(search_keyword_array)
start_point = 0
now_state = ""

global crawling_start

def crawling_start(keyword_index):

    global now_state

    driver.find_element_by_id("search.keyword.query").send_keys(str(search_keyword_array[keyword_index]))
    now_state = str(search_keyword_array[keyword_index])

    driver.implicitly_wait(1)
    driver.find_element_by_id("search.keyword.query").send_keys("\n")
    driver.implicitly_wait(3)

    if keyword_index == 0:

        target_section = driver.find_element_by_id("dimmedLayer")
        print(' --------- find dimmedLayer --------- ')
        target_section.click()
        print(' --------- click dimmedLayer --------- ')
        driver.implicitly_wait(1)
        detail_section = driver.find_element_by_id("info.search.place.list")
        print(' --------- find placeList --------- ')
        detail_section.click()
        print(' --------- click placeList --------- ')
        driver.implicitly_wait(1)

    if keyword_index != 0 and keyword_index % 5 == 0:
        print('---- rest-time ----')
        time.sleep(2)

    init_more_btn = driver.find_element_by_id("info.search.place.more")
    init_more_btn.click()
    driver.implicitly_wait(3)
    time.sleep(1)

    init_page_btn = driver.find_element_by_id("info.search.page.no1")
    init_page_btn.click()

    if keyword_index != 0 and len(str(search_keyword_array[keyword_index])) != 0:
        crawling_relay()


crawling_start(0)

def result():

        print('resulting_start')
        global shop_name_list, shop_addr_list, shop_hp_list, page_no, result_json_array
        global now_state, start_point, max_point


        print(len(shop_name_list))
        print(shop_name_list)
        print(len(shop_addr_list))
        print(shop_addr_list)
        print(len(shop_hp_list))
        print(shop_hp_list)

        for i in range(len(shop_name_list)):
                data = {}
                data[shop_name_list[i]] = {
                        'shop_addr': shop_addr_list[i],
                        'shop_hp': shop_hp_list[i]
                }
                json_data = json.dumps(data, ensure_ascii=False)
                result_json_array.append(json_data)

        with open("/Users/hwang-yongjae/Desktop/crawling_shopinfo_result/"+now_state+".json", "w", encoding='utf-8') as make_file:
            json.dump(json.dumps(result_json_array), make_file, indent="\t")

        for elem in result_json_array:
                print(elem)


        driver.find_element_by_id("search.keyword.query").clear()
        time.sleep(0.3)
        shop_name_list = []
        shop_addr_list = []
        shop_hp_list = []
        page_no = 1
        result_json_array = []

        if start_point == max_point:
            print('finish-crawling-pjt')
            return

        if start_point < max_point:
            start_point = start_point + 1
            crawling_start(int(start_point))


def crawling_relay():

            global page_no

            if page_no == 1:

                print('page_no : 1')
            else:
                print('page_number : '+str(page_no))
                page_btn = driver.find_element_by_id("info.search.page.no" + str(page_no))
                page_btn.click()
            time.sleep(0.1)
            driver.implicitly_wait(3)

            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            shop_info_all_cnt = int(soup.find('em', {'id': 'info.search.place.cnt'}).text.replace(',', ''))

            shop_info_section = soup.find('ul', {'id': 'info.search.place.list'})
            shop_info_list_name = shop_info_section.select('strong.tit_name a.link_name')

            shop_info_list_addr = shop_info_section.select('div.info_item div.addr p[data-id=address]')

            shop_info_list_hp = shop_info_section.select('div.info_item span.phone')

            tmp_section_shop_cnt = 0
            for shop_name in shop_info_list_name:
                    shop_name_list.append(shop_name.text)
                    print(len(shop_name_list))
                    print(shop_name.text)
                    tmp_section_shop_cnt = tmp_section_shop_cnt + 1

            for shop_addr in shop_info_list_addr:
                    shop_addr_list.append(shop_addr.text)
                    print(shop_addr.text)

            for shop_hp in shop_info_list_hp:
                    shop_hp_list.append(shop_hp.text)
                    print(shop_hp.text)

            if tmp_section_shop_cnt < 15:
                    result()
                    return

            if int(len(shop_name_list)) < shop_info_all_cnt:
                    page_no = page_no + 1

                    if page_no != 1 and page_no % 5 == 1:
                            next_btn = driver.find_element_by_id("info.search.page.next")
                            next_btn.click()
                            page_no = 1
                            driver.implicitly_wait(1)

                    crawling_relay()


print('start point')

try:
   crawling_relay()
   driver.implicitly_wait(5)
except ValueError:
   print(format(text))
