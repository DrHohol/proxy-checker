import requests as r
from sys import argv

lisst = open(argv[1], 'r').read().split('\n')
urle = input('Url for check:  ')
timeout = input('Timeout for proxies  ')
url = 'http://' + urle
s = r.Session()
good = open('good_proxy.txt', 'w')
bad = open('bad_proxy.txt', 'w')

def check():
	for item in lisst:
		proxy = {'https': 'http://'+item}
		try:
			dort = s.get(url, proxies=proxy, timeout=int(timeout))
			if dort.status_code == 200: good.write(item + '\n') and print('good  ' + item)
			else:  bad.write(item + '\n') and print('bad   ' + item + '  ' + dort.status_code)
		except Exception as e:
			print('something wrong    '  + item)
			bad.write(item + '\n')
			pass
	print('Finished')
try:
	check()
except KeyboardInterrupt:
	print("\nExit")