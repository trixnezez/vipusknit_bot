import requests
import json
import xmltojson
import utils
import time
import csv
from datetime import datetime
import random
import urllib
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
 
 
 
global_url = 'https://enbek.kz'
proxy_list = [
    {'https': f'http://adikaomarov:omowtDJjj9@109.172.5.66:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@193.233.62.114:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@46.3.170.80:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@217.171.146.185:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@79.143.19.127:59100'}
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
 
 
 
def get_proxy():
    while(True):
        proxy = random.choice(proxy_list)
        try:
            r = requests.get('http://hh.kz', proxies = proxy)
            #print(r)
            if r.status_code == 200:
                #print(proxy)
                return proxy
        except IOError:
            print(f'Выпал плохой прокси {proxy}')
            continue


def get_all_pages():
 
    req = requests.get(url = global_url, headers = random.choice(headers),proxies = get_proxy())
    #print(req)
    with open("IT_Data/page_0.html","w",encoding ="utf-8") as file:
        file.write(req.text)
 
    with open("IT_Data/page_0.html",encoding ="utf-8") as file:
        src = file.read()
    soup = BeautifulSoup(src,"lxml")
    #find("span", {"class":"pager-item-not-in-short-range"}).
    pages_count = int(soup.find("div",{"class":"pager"}).find_all("a")[-2].text)
    for i in range(1,pages_count):
        url = f"https://almaty.hh.kz/search/vacancy?area=160&clusters=true&enable_snippets=true&ored_clusters=true&professional_role=84&professional_role=116&professional_role=36&professional_role=157&professional_role=125&professional_role=156&professional_role=160&professional_role=10&professional_role=150&professional_role=25&professional_role=165&professional_role=73&professional_role=96&professional_role=164&professional_role=104&professional_role=112&professional_role=113&professional_role=148&professional_role=114&professional_role=121&professional_role=124&professional_role=20&search_period=30&hhtmFrom=vacancy_search_list&page={i}"
        r = requests.get(url = url,headers = random.choice(headers),proxies = get_proxy())
        with open(f"IT_data/page_{i}.html","w",encoding ="utf-8") as file:
            file.write(r.text)
    print('Вытащил страницы поиска')
    return pages_count
 
def collect_data(pages_count, file_name):
    for page in range(0, pages_count):
        if page == pages_count:
            print(f'Последняя ссылка страницы {page}')
        print(f'Обрабатывается страница № {page}')
        urls = []
        with open(f"IT_Data/page_{page}.html",encoding ="utf-8") as html_file:
            #подгружаю html 
            soup = BeautifulSoup(html_file,"html.parser")
            script = soup.find("template",{"id":"HH-Lux-InitialState"}).text
 
            #подгружаю json
            json_data = json.loads(script)
            searchResults = json_data.get('vacancySearchResult')
 
            vacancies = searchResults['vacancies']
 
            for i in range(0,len(vacancies)):
                urls.append(vacancies[i]['links']['desktop'])
 
 
        with open("items_urls.txt","w",encoding ="utf-8") as file:
            for url in urls:
                file.write(f"{url}\n")
        get_data(file_path="items_urls.txt", file_name=file_name)
 
 
def get_data(file_path, file_name):
    result_list = []
    with open(file_path,encoding ="utf-8") as file:
        urls_list = file.readlines()
        clear_urls_list =[]
        for url in urls_list:
            url = url.strip()
            clear_urls_list.append(url)
 
 
    for i,url in enumerate(clear_urls_list):
        
            print(f'url №{i}')
            response = requests.get(url=url,headers=random.choice(headers),proxies = get_proxy())
            soup = BeautifulSoup(response.text,"html.parser")
 
 
            try:
                item_name = soup.find("div",{"class":"main-content"}).find("h1",{"data-qa":"vacancy-title"}).text.strip()
            except:
                item_name = 'E1'
 
            try:
                item_salary = soup.find("div",{"class":"main-content"}).find("div",{"data-qa":"vacancy-salary"}).text.strip()
            except:
                item_salary = 'E2'
 
            try:
                item_exp = soup.find("div",{"class":"main-content"}).find("span",{"data-qa":"vacancy-experience"}).text.strip()
            except:
                item_exp = 'E3'
 
            try:
                company_name = soup.find("div",{"class":"main-content"}).find("span",{"class":"vacancy-company-name"}).find("span").text.strip()
            except:
                company_name = 'E4'
 
            try:
                if soup.find("div",{"class":"main-content"}).find("p",{"class":"vacancy-creation-time-redesigned"}):
                    date = soup.find("div",{"class":"main-content"}).find("p",{"class":"vacancy-creation-time-redesigned"}).text.strip()
                else:
                    date = soup.find("div",{"class":"main-content"}).find("p",{"class":"vacancy-creation-time"}).text.strip()
            except:
                date = 'E5'
 
            try:
                if soup.find("div",{"class":"main-content"}).find("span",{"data-qa":"vacancy-view-raw-address"}):
                    address = soup.find("div",{"class":"main-content"}).find("span",{"data-qa":"vacancy-view-raw-address"}).text
                elif soup.find("div",{"class":"main-content"}).find("div",{"class":"vacancy-company-bottom"}).find("p", {"data-qa":"vacancy-view-location"}):
                    address = soup.find("div",{"class":"main-content"}).find("div",{"class":"vacancy-company-bottom"}).find("p", {"data-qa":"vacancy-view-location"}).text
                elif soup.find("div",{"class":"main-content"}).find("div",{"class":"block-employer--jHuyqacEkkrEkSl3Yg3M"}):
                    address = soup.find("div",{"class":"main-content"}).find("div",{"class":"block-employer--jHuyqacEkkrEkSl3Yg3M"}).find("p", {"data-qa":"vacancy-view-location"}).text
            except:
                address = 'Алматы'
 
            try:
                zanyatost = soup.find("div",{"class":"main-content"}).find("p",{"data-qa":"vacancy-view-employment-mode"}).find("span").text.strip()
            except:
                zanyatost = 'E7'
 
            try:
                zanyatost2 = soup.find("div",{"class":"main-content"}).find("p",{"data-qa":"vacancy-view-employment-mode"}).text.lstrip(', ')
            except:
                zanyatost2 = 'E8'
 
            try:
                bloko_tags = soup.find("div",{"class":"main-content"}).find("div",{"class":"vacancy-description"}).find("div", {"class":"bloko-tag-list"}).find_all("span", {"class":"bloko-tag__section"})
                bloko_tags_info = ''
                for i in range(len(bloko_tags)):
                    bloko_tags_info += bloko_tags[i].text
                    bloko_tags_info += ';'
            except:
                bloko_tags_info = 'E9'

            if item_name == 'E1' and item_salary == 'E2' and item_exp == 'E3' and company_name =='E4':
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
                            item_name,
                            item_salary,
                            item_exp,
                            company_name,
                            date,
                            address,
                            zanyatost,
                            zanyatost2,
                            bloko_tags_info,
                            url
                        )
                    )
 
 
 
def main():
    date = datetime.now().strftime('%d_%m_%Y_%H_%M_S')
    file_name = f'IT_vacancies_{date}.csv'
    with open(file_name,'w',encoding ="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                    'Должность',
                    "Зарплата",
                    "Опыт",
                    "Компания",
                    "Дата обьявления",
                    "Район",
                    "Тип занятости",
                    "Тип занятости2",
                    "Ключевые навыки",
                    "Ссылка"
            )
        )
    pages_count = get_all_pages()
    collect_data(pages_count=pages_count,file_name = file_name)
 
 
if __name__ == "__main__":
    main()
 