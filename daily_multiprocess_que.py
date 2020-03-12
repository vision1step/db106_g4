import subprocess as sp
import threading
import queue

def subpro(p):
    print(f'{p} start')
    process = sp.Popen(f'python {p}', shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
    result = process.communicate()
    if process.returncode == 0:
        print(f'{p} complete')
    else:
        print(result[1])


pys = ['ltn_all_daily.py','ltn_RSS.py','cnyes_news_hightlight','news_crawler_moneydj.py','rss_crawler_moneydj.py']
q = queue.Queue()

for n in range(len(pys)):
    q.put(threading.Thread(target=subpro,args=(pys[n],)))
    q.get().start()