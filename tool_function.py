import os
from datetime import datetime


def mkpath_check(diry):
    if not os.path.exists(diry):
        os.mkdir(diry)


def mkfile_check(file_dir, file_for):
    if not os.path.exists(file_dir):
        with open(file_dir, 'w', encoding='utf-8') as f:
            if file_for == 'log':
                crawl_log = "Initialization': Crawler log start at %s" % (str(datetime.now().date())) + ';'
                f.write(crawl_log)
            elif file_for == 'data':
                news_data = "Initialization: Crawler start at %s" % (str(datetime.now().date())) + ';'
                f.write(news_data)
            f.close()


def str_to_timestamp(t_str):
    dt_obj = datetime.strptime(t_str, "%Y/%m/%d %H:%M")
    result = datetime.timestamp(dt_obj)
    return result
