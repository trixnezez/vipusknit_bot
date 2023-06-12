import requests
import json
import xmltojson
import utils
import shutil
import time
import csv
import random
import urllib
from datetime import datetime
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
 
 
 
global_url = 'https://enbek.kz'
proxy_list = [
    {'https': f'http://adikaomarov:omowtDJjj9@79.143.19.77:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@79.143.19.87:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@79.143.19.75:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@79.143.19.78:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@79.143.19.81:59100'}
    ]
 
headers = [{'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'},
    {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'},
    {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'},
    {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'},
    {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36'}
]

with open('professionalroles.json') as pri_file:
    pri_dict = json.load(pri_file)


def check_pri(pri):
    for id in pri_dict['data']:
        if id["id"] == pri:
            return id['name']
    return None

 
def get_proxy():
    while True:
        proxy = random.choice(proxy_list)
        print(proxy)
        try:
            r = requests.get('http://enbek.kz', proxies=proxy)
            if r.status_code == 200:
                return proxy
        except requests.exceptions.ProxyError as e:
            print(f"Произошла ошибка подключения через прокси: {e}")
            continue
        except requests.exceptions.RequestException as e:
            print(f"Произошла ошибка запроса: {e}")
            continue
        except Exception as e:
            print(f"Произошла неизвестная ошибка: {e}")
            continue
            

def check_for_bad_words(str):
    with open("bad.json","r")  as bad:
        bad_words = json_load(bad)
    res_str = str.split(0)
    for word in res_str:
        if word in bad_words:
            if bad_words[word]==True:
                return true

def get_all_pages(city_name, city_url):
 
    req = requests.get(url = city_url, headers = random.choice(headers))
    #print(req)
    with open(f"{city_name}_Data/page_1.html","w",encoding ="utf-8") as file:
        file.write(req.text)
 
    with open(f"{city_name}_Data/page_1.html",encoding ="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src,"lxml")
    #find("span", {"class":"pager-item-not-in-short-range"}).
    try:
        pages_count = int(soup.find("ul",{"class":"pagination"}).find_all("button")[-2].text)
    except:
        pages_count=1
    for i in range(2,pages_count):
        url = city_url + f'&page={i}'
        r = requests.get(url = url,headers = random.choice(headers))
        with open(f"{city_name}_Data/page_{i}.html","w",encoding ="utf-8") as file:
            file.write(r.text)
    print('Вытащил страницы поиска')
    return pages_count
 
def collect_data(city_name, city_url, pages_count, file_name):
    for page in range(1, pages_count):
        print(f'Обрабатывается страница № {page}')
        urls = []
        with open(f"{city_name}_Data/page_{page}.html",encoding ="utf-8") as html_file:
            #подгружаю html 
            soup = BeautifulSoup(html_file,"lxml")
            # print(soup.text)
            url_list = soup.find("div",{"class":"col-lg-8"}).find_all("a",{"class":"stretched"})
            #print(url_list)
            # f = open("testnote.txt","w")
            # results_str = '\n'.join([str(result) for result in url_list])
            # f.write(results_str)
            for i in url_list:
                #print(i)
                if i.get('href'):
                    href = i.get('href')
                    urls.append(href)
                # if i['href'][0:12] == '/ru/вакансия':
                #     urls.append(i['href'])
                #     print(i['href'])
            
            # print(urls)
        with open("items_urls.txt","w",encoding ="utf-8") as file:
            for url in urls:
                file.write(f"{global_url}{url}\n")
                # print(url)
        get_data(file_path="items_urls.txt", file_name=file_name)
 
 
def get_data(file_path, file_name):
    result_list = []
    with open(file_path,"r",encoding ="utf-8") as file:
        urls_list = file.readlines()
        clear_urls_list =[]
        for url in urls_list:
            url = url.strip()
            clear_urls_list.append(url)
    # print(clear_urls_list)
 
    for i,url in enumerate(clear_urls_list):

            print(f'url №{i}')
            try:
                response = requests.get(url=url,headers=random.choice(headers))
                soup = BeautifulSoup(response.text,"lxml")
                try:
                    title = soup.find("div",{"class":"col-lg-9"}).find("h4",{"class":"title"}).find("strong").text.strip()
                except:
                    title = None

                try:
                    pri = soup.find("div",{"class":"category mb-2"}).text.strip()
                except:
                    pri = None


                try:
                    price = soup.find("div",{"class":"price"}).text.strip()
                except:
                    price = None

                # try:
                #     #ul_block = soup.find("div", {"class":"col-lg-9","class":"!align-items-center"})#.find("div",{"class":"d-lg-flex"}).find_all('li')
                #     ul_block = soup.select_one('div.d-lg-flex:not(.align-items-center)').find_all('li')
                #     opit = ul_block[4].select_one('span:not(.label)').text.strip()
                # except:
                #     opit = None
                company_name = ''
                try:
                    company_name = soup.find("div", {"class":'company-box'}).find("a").text.strip()
                    
                except:
                    company_name = None
                
                try:
                    date = soup.find("div", {"class":"col-lg-9 order-0"}).find("ul",{"class":"info small mb-2"}).find("li").text.strip()
                except:
                    date = "e6"

                try:
                    opt1 =''
                    opt2 = ''
                    #ul_block = soup.find("div", {"class":"col-lg-9","class":"!align-items-center"})#.find("div",{"class":"d-lg-flex"}).find_all('li')
                    text_blocks = soup.find("div",{"class":"col-lg-9"}).find("div",{"class":"text"}).find_all("div",{"class":"single-line"})
                    for i in text_blocks:
                        address_block = i.find("div",{"class":"label"}).text
                        # print (i)
                        # print('checl')
                        if "Место работы" in address_block:
                            opt1 = i.find("div",{"class":"value"}).text.strip()
                            # print ('get_it')
                            break
                        elif  "Адрес" in address_block:
                            opt2 = i.find("div",{"class":"value"}).text.strip()
                            # print('get it')
                            break
                        # if i.select('div:-soup-contains("Место работы")') and i.find("div",{"class":"label"}).text.strip() != "Обязанности":
                        #     opt1 = i.find("div",{"class":"value"}).text.strip()
                        #     print ('get_it')
                        #     break
                        # elif i.select('div:-soup-contains("Адрес")') and i.find("div",{"class":"label"}).text.strip() != "Обязанности":
                        #     opt2 = i.find("div",{"class":"value"}).text.strip()
                        #     print('get it')
                        #     break
                    # if text_blocks.select('div:-soup-contains("Место работы")')!=None:
                    #     label_arr = 
                    # opt1 = text_blocks.select('div:-soup-contains("Адрес")')

                    if opt1 =='' and opt2=='':
                        res_opt = 'Адреса нет'
                    elif opt1 !='' and opt2=='':
                        res_opt = opt1
                    elif opt2 !='' and opt1=='':
                        res_opt = opt2
                    else:
                        res_opt = soup.find("div", {"class":"item-list pea"}).find("li",{"class":"location"}).text.strip

                except:
                    res_opt = None  

                try:
                    #ul_block = soup.find("div", {"class":"col-lg-9","class":"!align-items-center"})#.find("div",{"class":"d-lg-flex"}).find_all('li')
                    ul_block = soup.select_one('div.d-lg-flex:not(.align-items-center)').find_all('li')
                    graphik_rabot = ul_block[1].select_one('span:not(.label)').text.strip()
                except:
                    graphik_rabot = None

                if graphik_rabot =='полный рабочий день':
                    graphik_rabot = 'полный день'
                elif graphik_rabot =='посменный':
                    graphik_rabot = 'сменный график'
                elif graphik_rabot == 'неполный рабочий день' or graphik_rabot == 'неполная рабочая неделя':
                    graphik_rabot = 'гибкий график'


                try:
                    #ul_block = soup.find("div", {"class":"col-lg-9","class":"!align-items-center"})#.find("div",{"class":"d-lg-flex"}).find_all('li')
                    ul_block = soup.select_one('div.d-lg-flex:not(.align-items-center)').find_all('li')
                    tip_zanyatosti = ul_block[0].select_one('span:not(.label)').text.strip()
                except:
                    tip_zanyatosti = None   
                if tip_zanyatosti == 'постоянная':
                    tip_zanyatosti = 'Полная занятость'
                elif tip_zanyatosti == 'временная':
                    tip_zanyatosti = 'Проектная работа'
                elif tip_zanyatosti =='сезонная':
                    tip_zanyatosti ='Проектная работа'




                abilities = ''
                try:
                    opt1 =''
                    #ul_block = soup.find("div", {"class":"col-lg-9","class":"!align-items-center"})#.find("div",{"class":"d-lg-flex"}).find_all('li')
                    text_blocks = soup.find("div",{"class":"col-lg-9"}).find("div",{"class":"text"}).find_all("div",{"class":"single-line"})
                    for i in text_blocks:
                        if i.select('div:-soup-contains("Профессиональные навыки")'):
                            opt1 = i.find_all("a")
                            for j in opt1:
                                abilities = j.text.strip()
                    # if text_blocks.select('div:-soup-contains("Место работы")')!=None:
                    #     label_arr = 
                    # opt1 = text_blocks.select('div:-soup-contains("Адрес")')
                except:
                    abilities = None

                try:
                    mera = ''
                    opt1 =''
                    #ul_block = soup.find("div", {"class":"col-lg-9","class":"!align-items-center"})#.find("div",{"class":"d-lg-flex"}).find_all('li')
                    text_blocks = soup.find("div",{"class":"col-lg-9"}).find("div",{"class":"text"}).find_all("div",{"class":"single-line"})
                    for i in text_blocks:
                        mera_block = i.find("div",{"class":"label"}).text
                        if mera_block and "Мера содействия" in mera_block:
                            mera = i.find("div",{"class":"value"}).text

                        # if i.select('div:-soup-contains("Мера содействия")'):
                        #     opt1 = i.find("value").text
                        #     for j in opt1:
                        #         mera = j.text.strip()
                    # if text_blocks.select('div:-soup-contains("Место работы")')!=None:
                    #     label_arr = 
                    # opt1 = text_blocks.select('div:-soup-contains("Адрес")')
                except:
                    mera = None
                
                # try:
                #     bloko_tags = soup.find("div",{"class":"main-content"}).find("div",{"class":"vacancy-description"}).find("div", {"class":"bloko-tag-list"}).find_all("span", {"class":"bloko-tag__section"})
                #     bloko_tags_info = ''
                #     for i in range(len(bloko_tags)):
                #         bloko_tags_info += bloko_tags[i].text
                #         bloko_tags_info += ';'
                # except:
                #     bloko_tags_info = 'E9'
                
                # if check_for_bad_words(title)==True or check_for_bad_word(abilities)==True: 
                    # continue

                specialization = check_pri(pri)
                if title == 'E1' and price == 'E2' and opit == 'E3' and company_name =='E4':
                    print('Ошибочка ', url)
                    with open('Errors_log.csv','a',encoding ="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (
                                i,
                                url,
                                soup,
                            )
                        )
                else:
                    with open(file_name,'a',encoding ="utf-8") as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (
                                title,
                                pri,
                                price,
                                company_name,
                                date,
                                res_opt,
                                graphik_rabot,
                                tip_zanyatosti,
                                abilities,
                                url,
                                mera,
                                specialization
                            )
                        )
            except:
                print('conn error')
 
 
def main():
    date = datetime.now().strftime('%d_%m_%Y_%H_%M_S')
    with open('Cities.json',encoding = "utf-8") as file:
        data = json.load(file)
        data = data.get('cities')
    for city_name, city_url in data.items():
        file_name = f'Vacancies/{city_name}_vacancies_{date}.csv'
        with open(file_name,'w',encoding ="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                (
                        'Должность',
                        'professionalroleid',
                        "Зарплата",
                        "Компания",
                        "Дата обьявления",
                        "Район",
                        "Тип занятости",
                        "Тип занятости2",
                        "Ключевые навыки",
                        "Ссылка",
                        "Мера содействия занятости",
                        "Специальность"
                )
            )
        print(city_url)
        pages_count = get_all_pages(city_name = city_name, city_url = city_url )
        print(pages_count)
        collect_data(city_name = city_name, city_url = city_url,pages_count=pages_count,file_name = file_name)
        shutil.copyfile(file_name, f'enbek_{city_name}_vacancies.csv')
 
 
if __name__ == "__main__":
    main()
 