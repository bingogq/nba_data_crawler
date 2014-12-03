# coding: utf-8


import datetime
import sqlite3
import urllib2
import time

def create_table():
    conn = sqlite3.connect('data.db')

    sql = """CREATE TABLE sbweek
( start TEXT NOT NULL,
  content TEXT NOT NULL);"""

    conn.execute(sql)
    conn.close()

def main():
    # start_date_str = '20021006'

    start_date_str = '20140105'
    end_date_str = '20141123'

    start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d')
    week_date = datetime.timedelta(weeks=1)

    url_prefix = 'http://scores.espn.go.com/nba/format/sbweek?start='

    conn = sqlite3.connect('data.db')


    while True:
        
        if start_date > end_date:
            break

        url_date = start_date.strftime('%Y%m%d')
        url = url_prefix + url_date

        print(url)

        content = urllib2.urlopen(url).read()

        sql = "INSERT INTO sbweek (start,content) VALUES (?, ?);"
        conn.execute(sql, (url_date, content))
        conn.commit()

        time.sleep(1.5)
        start_date += week_date


    conn.close()


if __name__ == '__main__':
    # create_table()
    main()