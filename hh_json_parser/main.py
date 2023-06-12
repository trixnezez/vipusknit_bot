import requests
import json
import xmltojson
import utils
import time
import csv
from datetime import datetime
import random
import urllib
import shutil
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
 
 
 
global_url = 'https://almaty.hh.kz/search/vacancy?area=160&professional_role=84&professional_role=116&professional_role=36&professional_role=157&professional_role=125&professional_role=156&professional_role=160&professional_role=10&professional_role=150&professional_role=25&professional_role=165&professional_role=96&professional_role=164&professional_role=104&professional_role=112&professional_role=113&professional_role=148&professional_role=114&professional_role=121&professional_role=124&professional_role=20&search_field=name&search_field=company_name&search_field=description&clusters=true&enable_snippets=true&ored_clusters=true&search_period=30&hhtmFrom=vacancy_search_list'

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

def check_for_bad_words(str):
    with open("bad.json","r")  as bad:
        bad_words = json_load(bad)
    res_str = str.split(0)
    for word in res_str:
        if word in bad_words:
            if bad_words[word]==True:
                return true


def check_pri(pri):
	for id in pri_dict['data']:
		if id["id"] == pri:
			return id['name']
	return None


def get_proxy():									#Проверка прокси на валидность
	while(True):
		proxy = random.choice(proxy_list)
		try:
			r = requests.get('http://hh.kz')
			#print(r)
			if r.status_code == 200:						#Возвращаем прокси в случае успешного статуса ответа
				#print(proxy)
				return proxy
		except IOError:
			print(f'Выпал плохой прокси {proxy}')
			continue								#Перебираем прокси в случае не валидности


def get_all_pages(city_name,city_url):					#Функция сбора количества страницц
 
	req = requests.get(url = city_url, headers = random.choice(headers))
	#print(req)
	with open(f"{city_name}_Data/page_0.html","w",encoding ="utf-8") as file:
		file.write(req.text)													#Делаем запрос на первую страницу поиска
 
	with open(f"{city_name}_Data/page_0.html",encoding ="utf-8") as file:
		src = file.read()
	soup = BeautifulSoup(src,"lxml")
	#find("span", {"class":"pager-item-not-in-short-range"}).
	try:
		pages_count = int(soup.find("div",{"class":"pager"}).find_all("a")[-2].text)	#Вытаскиваем количество страниц
	except:
		pages_count = 1
	for i in range(1,pages_count):			#Записываем все ссылки на страницы поиска вакансий в файл 
		url = city_url + f'&page={i}'
		r = requests.get(url = url,headers = random.choice(headers))
		with open(f"{city_name}_data/page_{i}.html","w",encoding ="utf-8") as file:
			file.write(r.text)
	print(f'Вытащил страницы поиска {city_name}')
	return pages_count

 
 
 
def collect_data(city_name, city_url, pages_count, file_name):		#функция сбора ссылок на вакансии со страниц поиска
	for page in range(0, pages_count):
		if page == pages_count:
			print(f'Последняя ссылка страницы {page}')
		print(f'Обрабатывается страница № {page}')
		urls = []
		pris = []
		with open(f"{city_name}_Data/page_{page}.html",encoding ="utf-8") as html_file:
																							#подгружаю html 
			soup = BeautifulSoup(html_file,"html.parser")		
			script = soup.find("template",{"id":"HH-Lux-InitialState"}).text
 
			#подгружаю json
			json_data = json.loads(script)
			searchResults = json_data.get('vacancySearchResult')
 
			vacancies = searchResults['vacancies']
 			#закидываю ссылки на вакансии и их специальность в лист
			for i in range(0,len(vacancies)):
				urls.append(vacancies[i]['links']['desktop'])
				pris.append(vacancies[i]['professionalRoleIds'][0]['professionalRoleId'][0])

		get_data(urls = urls,pris = pris,file_name = file_name)		#Запускаю функцию сбора данных с сылок на вакансии
 

 
def get_data(urls, pris, file_name):
 
	for i,url in enumerate(urls):			#Собираем информацию с каждой ссылки
		irl = pris[i]
		try:
			response = requests.get(url=url,headers=random.choice(headers))
			soup = BeautifulSoup(response.text,"html.parser")
			try:
				item_name = soup.find("div",{"class":"main-content"}).find("h1",{"data-qa":"vacancy-title"}).text.strip()
			except:
				item_name = None
			try:
				item_salary = soup.find("div",{"class":"main-content"}).find("div",{"data-qa":"vacancy-salary"}).text.strip()
			except:
				item_salary = None
	 
			# try:
			# 	item_exp = soup.find("div",{"class":"main-content"}).find("span",{"data-qa":"vacancy-experience"}).text.strip()
			# except:
			# 	item_exp = 'E3'
	 
			try:
				company_name = soup.find("div",{"class":"main-content"}).find("span",{"class":"vacancy-company-name"}).find("span").text.strip()
			except:
				company_name = None
	 
			try:
				if soup.find("div",{"class":"main-content"}).find("p",{"class":"vacancy-creation-time-redesigned"}):
					date = soup.find("div",{"class":"main-content"}).find("p",{"class":"vacancy-creation-time-redesigned"}).text.strip()
				else:
					date = soup.find("div",{"class":"main-content"}).find("p",{"class":"vacancy-creation-time"}).text.strip()
			except:
				date = None
	 
			try:
				if soup.find("div",{"class":"main-content"}).find("span",{"data-qa":"vacancy-view-raw-address"}):
					address = soup.find("div",{"class":"main-content"}).find("span",{"data-qa":"vacancy-view-raw-address"}).text
				elif soup.find("div",{"class":"main-content"}).find("div",{"class":"vacancy-company-bottom"}).find("p", {"data-qa":"vacancy-view-location"}):
					address = soup.find("div",{"class":"main-content"}).find("div",{"class":"vacancy-company-bottom"}).find("p", {"data-qa":"vacancy-view-location"}).text
				elif soup.find("div",{"class":"main-content"}).find("div",{"class":"block-employer--jHuyqacEkkrEkSl3Yg3M"}):
					address = soup.find("div",{"class":"main-content"}).find("div",{"class":"block-employer--jHuyqacEkkrEkSl3Yg3M"}).find("p", {"data-qa":"vacancy-view-location"}).text
			except:
				address = None
	 
			try:
				zanyatost = soup.find("div",{"class":"main-content"}).find("p",{"data-qa":"vacancy-view-employment-mode"}).find("span").text.strip()
			except:
				zanyatost = None
	 
			try:
				zanyatost2 = soup.find("div",{"class":"main-content"}).find("p",{"data-qa":"vacancy-view-employment-mode"}).text.split(',')[0]
			except:
				zanyatost2 = None
	 
			try:
				bloko_tags = soup.find("div",{"class":"main-content"}).find("div",{"class":"vacancy-description"}).find("div", {"class":"bloko-tag-list"}).find_all("span", {"class":"bloko-tag__section"})
				bloko_tags_info = ''
				for i in range(len(bloko_tags)):
					bloko_tags_info += bloko_tags[i].text
					bloko_tags_info += ';'
			except:
				bloko_tags_info = None

			mera = None
			specialization = check_pri(irl)
			#Проверяем на наличие ошибок 
			if item_name == 'E1' and item_salary == 'E2' and company_name =='E4':
				with open('Errors_log.csv','a',encoding ="utf-8") as file:
					writer = csv.writer(file)
					writer.writerow(
						(
							i,
							url,
							soup,
						)
					)
			else:		#или записываем в файл
				with open(file_name,'a',encoding ="utf-8") as file:
					writer = csv.writer(file)
					writer.writerow(
						(
							item_name,
							irl,
							item_salary,
							company_name,
							date,
							address,
							zanyatost,
							zanyatost2,
							bloko_tags_info,
							url,
							mera,
							specialization

						)
					)
 
		except:
			print('conn error')
 
 
def main():
	date = datetime.now().strftime('%d_%m_%Y_%H_%M_S') 			#Определяю время запуска парсера
	with open('Cities.json',encoding = "utf-8") as file:			#Подгружаю json-файл с ссылками городов
		data = json.load(file)
		data = data.get('cities')

	for city_name, city_url in data.items():							#Для каждого городаа запускаю итерацию
		file_name = f'vacancies/{city_name}_vacancies_{date}.csv'
		with open(file_name,'w',encoding ="utf-8") as file:				#Создаю csv файл с датой запуска парсера
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
		pages_count = get_all_pages(city_name = city_name, city_url = city_url ) #Проверяю количество страниц дял парсинга
		collect_data(city_name = city_name, city_url = city_url, pages_count=pages_count,file_name = file_name)		#Функия сбора данных с каждой страницы поиска
		shutil.copyfile(file_name, f'hh_{city_name}_vacancies.csv')



if __name__ == "__main__":
	main()
