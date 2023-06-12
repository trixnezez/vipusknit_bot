import requests
import json
import xmltojson
import utils
import time
import csv
import random
from bs4 import BeautifulSoup

global_url = "https://krisha.kz"

# headers = {
# 	"user-agent" : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
# 	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
# }


headers = [{'headers': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'},
	{'headers': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.72 Safari/537.36'},
	{'headers': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10) AppleWebKit/600.1.25 (KHTML, like Gecko) Version/8.0 Safari/600.1.25'},
	{'headers': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'},
	{'headers': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'},
	{'headers': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36'},
	{'headers': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit/600.1.17 (KHTML, like Gecko) Version/7.1 Safari/537.85.10'},
	{'headers': 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko'},
	{'headers': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:33.0) Gecko/20100101 Firefox/33.0'},
	{'headers': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.104 Safari/537.36'}
]
 

def get_all_pages(proxy_list):
	proxies = random.choice(list(proxy_list))
	req = requests.get(url = "https://krisha.kz/prodazha/kvartiry/almaty/?page=1", headers = random.choice(headers), proxies = proxies)
	with open("data/page_1.html","w",encoding ="utf-8") as file:
			file.write(req.text)

	with open("data/page_1.html",encoding ="utf-8") as file:
		src = file.read()
	soup = BeautifulSoup(src,"lxml")
	#find("span", {"class":"pager-item-not-in-short-range"}).
	pages_count = int(soup.find("nav",{"class":"paginator"}).find_all("a")[-7].text)
	for i in range(1,pages_count+1):
		url = f"https://krisha.kz/prodazha/kvartiry/almaty/?page={i}"
		r = requests.get(url = url,headers = random.choice(headers))
		with open(f"data/page_{i}.html","w",encoding ="utf-8") as file:
			file.write(r.text)

		time.sleep(5)

	return pages_count+1


# Прокси гамно, долгий response =\
# def get_proxy():
#     url = "https://free-proxy-list.net/"
#     # формируем объект sp, получив ответ http
#     sp = BeautifulSoup(requests.get(url).content, "html.parser")
#     proxy = []
#     for row in sp.find("div", attrs={"class": "fpl-list"}).find_all("tr")[1:]:
#         tds = row.find_all("td")
#         try:
#             ip = tds[0].text.strip()
#             port = tds[1].text.strip()
#             host = f"{ip}:{port}"
#             proxy.append(host)
#         except IndexError:
#             continue
#     return proxy

def collect_data(pages_count,proxy_list):
	for page in range(1, pages_count+1):
		print(f'Обрабатывается страница № {page}')
		with open(f"data/page_{page}.html",encoding ="utf-8") as file:
			src = file.read()
			soup = BeautifulSoup(src,"lxml")
			items_divs = soup.find_all("div",{"class":"a-card"})
			#print(len(items_divs))
			urls =[]
			for item in items_divs:
				item_url = item.find("div",{"class":"a-card__header"}).find("a",{"class":"a-card__title"}).get("href")
				urls.append(item_url)
			with open("items_urls.txt","w",encoding ="utf-8") as file:
				for url in urls:
					file.write(f"{global_url}{url}\n")
			get_data(file_path="items_urls.txt",proxy_list = proxy_list)
			#print(urls)


def get_data(file_path,proxy_list):
	result_list = []
	with open(file_path,encoding ="utf-8") as file:
		urls_list = file.readlines()
		clear_urls_list =[]
		for url in urls_list:
			url = url.strip()
			clear_urls_list.append(url)
	

	for url in clear_urls_list:
		proxies = random.choice(proxy_list)
		header = random.choice(headers)
		print(f'header: {header}\n proxy: {proxies}')
		#подгружаю html 
		response = requests.get(url=url,headers=header,proxies = proxies)
		soup = BeautifulSoup(response.text,"html.parser")
		
		#подгружаю json
		script = soup.find("script",{"id":"jsdata"}).text[20:]
		script = script[:-6]
		#print(script)
		json_data = json.loads(script)
		price = json_data.get('advert').get('price')
		title = json_data.get('advert').get('title')
		square = json_data.get('advert').get('square')
		rooms = json_data.get('advert').get('rooms')
		x = json_data.get('advert').get('map').get('lon')
		y = json_data.get('advert').get('map').get('lat')
		address = json_data.get('advert').get('addressTitle')
		district = json_data.get('advert').get('address').get('district')
		category = json_data['adverts'][0].get('category').get('label')
		owner = json_data['adverts'][0].get('owner').get('title')
		owner_category = json_data['adverts'][0].get('owner').get('label').get('title')
		date = json_data['adverts'][0].get('addedAt')

		#print(price)
		#print(price,title,square,rooms,x,y,address,district,category,owner,owner_category,date)
		# for i in range(0,len(vacancies)):
		# 	urls.append(vacancies[i]['links']['desktop'])


		with open('test.csv','a',encoding ="utf-8") as file:
			writer = csv.writer(file)
			writer.writerow(
				(
					title,
					price,
					square,
					rooms,
					x,
					y,
					address,
					district,
					category,
					owner,
					owner_category,
					date
				)
			)



def main():
	proxy_list = [
		{'https': f'http://vj6eE0:p2XaGJ@212.81.39.27:9932'},
		{'https': f'http://vj6eE0:p2XaGJ@212.81.38.13:9228'},
		{'https': f'http://vj6eE0:p2XaGJ@212.81.36.134:9834'},
		{'https': f'http://vj6eE0:p2XaGJ@212.81.37.136:9924'},
		{'https': f'http://vj6eE0:p2XaGJ@212.81.38.237:9887'}
	]
	with open('test.csv','w',encoding ="utf-8") as file:
			writer = csv.writer(file)
			writer.writerow(
				(
					'Описание',
					"Цена",
					"Площадь",
					"Количество комнат",
					"x",
					"y",
					"Адрес",
					"Район",
					"Категория на сайте",
					"Владелец",
					"Категория владельца",
					"Дата обьявления"
				)
			)
	pages_count = get_all_pages(proxy_list)

	collect_data(pages_count=pages_count,proxy_list = proxy_list)


if __name__ == "__main__":
	main()
















