import requests
import random
proxy_list = [
    {'https': f'http://adikaomarov:omowtDJjj9@109.172.5.66:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@193.234.62.114:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@46.3.171.80:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@217.171.145.185:59100'},
    {'https': f'http://adikaomarov:omowtDJjj9@79.143.19.117:59100'}
    ]


def get_proxy():
    while(True):
        proxy = random.choice(proxy_list)
        try:
            r = requests.get('http://krisha.kz', proxies = proxy,timeout = 1)
            print(r)
            if r.status_code == 200:
                print(proxy)
                return proxy
        except IOError:
            print(f'Выпал плохой прокси {proxy}')
            continue


proxies = get_proxy()
req = requests.get('https://www.python.org/',proxies = proxies)
#print(proxies)
print(req.status_code)