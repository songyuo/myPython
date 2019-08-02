import threading
import time
import schedule
import thestar
import bernama
from phnompenhpost import PhnoCrawler
from antara import AntaraCrawler


# host = "chinaaseanocean.mysql.rds.aliyuncs.com"  # 服务器
host = "chinaasean.mysql.rds.aliyuncs.com"  # 本地测试


def all_begin():

    thestar_()
    bernama_()
    phnompenhpost_()
    anrara_()


def thestar_():
    threading.Thread(target=thestar.crawl_today).start()


def bernama_():
    threading.Thread(target=bernama.crawl_today).start()


def phnompenhpost_():
    threading.Thread(target=PhnoCrawler.run).start()


def anrara_():
    threading.Thread(target=AntaraCrawler.run).start()


if __name__ == '__main__':
    all_begin()
    schedule.every(5).hours.do(thestar_)
    schedule.every(6).hours.do(bernama_)
    schedule.every().day.at('22:00').do(phnompenhpost_)
    schedule.every().day.at('22:10').do(anrara_)
    while True:
        schedule.run_pending()
        time.sleep(1)
