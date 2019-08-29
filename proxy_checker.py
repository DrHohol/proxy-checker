import requests
from sys import argv
import threading
import queue as Queue

proxyList = open(argv[1], 'r').read().split('\n')
url = argv[2]

good = []
bad = []
max_threads = int(argv[3])
threads = []

def check(q):
	if not q.empty():
		try:
			prox = q.get()
			proxy = {"https":'https://'+prox}
		except: pass
		try:
			r = requests.get(url,proxies=proxy, timeout=10)
			if r.status_code == 200:
				print("%s is good"%prox)
				good.append(prox)
			else:
				print(r.status_code)
				bad.append(prox)
		except Exception as e:
			print('bad proxy %s'%prox)
			bad.append(prox)
	else: pass



def writing():
	global good,bad
	good_proxy = open('good.txt','w')
	for i in good:
		good_proxy.write(str(i)+'\n')
	good_proxy.close()
	bad_proxy = open('bad.txt','w')
	for i in bad:
		bad_proxy.write(i+'\n')


try:
	threads = []
	queuelock = threading.Lock()
	queue = Queue.Queue()
	for item in proxyList:
		queue.put(item)
	while not queue.empty():
		queuelock.acquire()
		for i in range(max_threads):
			my_thread = threading.Thread(target=check,args=(queue,),daemon=True)
			#my_thread.daemon = True
			my_thread.start()
			threads.append(my_thread)
		for i in threads:
			i.join()
		queuelock.release()
	writing()
except: exit()
