nba_data_crawler
================

http://pan.baidu.com/s/1qWAxLA8

http://pan.baidu.com/s/1i3vIWXv


table

CREATE TABLE `gamelog` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `game_id` bigint(20) DEFAULT NULL,
  `quarter` int(11) DEFAULT NULL,
  `time_sec` int(11) DEFAULT NULL,
  `time_min_sec` varchar(32) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  `status` int(11) DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

CREATE TABLE `playbyplay` (
  `game_id` bigint(20) NOT NULL,
  `date` int(11) NOT NULL,
  `content` text NOT NULL,
  `status` int(11) NOT NULL,
  `away_team` varchar(128) DEFAULT NULL,
  `home_team` varchar(128) DEFAULT NULL,
  `quarter_count` int(11) DEFAULT NULL,
  `away_score` int(11) DEFAULT NULL,
  `home_score` int(11) DEFAULT NULL,
  PRIMARY KEY (`game_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;



# coding: utf-8

import sqlite3
import mysql.connector

def main():

    mysql_conf = {
        'host': 'localhost',
        'port': 3306,
        'database': 'nba',
        'user': 'root',
        'password': '',
        'charset': 'utf8',
        'use_unicode': True,
    }

    mysql_conn = mysql.connector.connect(**mysql_conf)
    mysql_cur = mysql_conn.cursor()

    print('connect to mysql')

    sqlite_conn = sqlite3.connect('data.db')
    sqlite_conn.text_factory = str
    sqlite_cur = sqlite_conn.cursor()

    print('connect to sqlite')

    select_sql = 'select game_id, date, content from playbyplay where status = 1 order by game_id;'
    sqlite_cur.execute(select_sql)

    sqlite_res = sqlite_cur.fetchall()

    for item in sqlite_res:
        insert_sql = 'insert into playbyplay (game_id, date, content, status) values(%s, %s, %s, 1)'
        mysql_cur.execute(insert_sql, (item[0], item[1], item[2]))
        mysql_conn.commit()
        print('insert: ', item[0])

    sqlite_cur.close()
    sqlite_conn.close()

    mysql_cur.close()
    mysql_conn.close()


if __name__ == '__main__':
    main()
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
# coding: utf-8


import mysql.connector
from bs4 import BeautifulSoup as bs

def main():
    mysql_conf = {
        'host': 'localhost',
        'port': 3306,
        'database': 'nba',
        'user': 'root',
        'password': '',
        'charset': 'utf8',
        'use_unicode': True,
    }

    mysql_conn = mysql.connector.connect(**mysql_conf)
    mysql_cur = mysql_conn.cursor()

    print('connect to mysql')

    error_game_id = []

    while True:

        #select_sql = 'select game_id, date, content from playbyplay where status = 1 order by game_id limit 100;'
        select_sql = 'select game_id, date, content from playbyplay where  game_id = 221024026 order by game_id limit 100;'
        mysql_cur.execute(select_sql)

        select_res = mysql_cur.fetchall()

        if not select_res:
            print("===> table is empty")
            break

        for item in select_res:

            game_id = item[0]
            game_date = item[1]
            game_content = item[2].encode('utf-8')
            quarter = 1
            game_score = ''

            print('game_id: ', game_id)
            print('game_date: ', game_date)

            soup = bs(game_content)

            matchup_id = 'matchup-nba-' + str(game_id)
            matchup = soup.find('div', {'id': matchup_id, 'class': 'matchup'})
            matchup_away = matchup.find('div', {'class': 'team away'})
            away_score = matchup_away.find('span').text

            matchup_home = matchup.find('div', {'class': 'team home'})
            home_score = matchup_home.find('span').text

            table = soup.find('table', {'class': 'mod-data'})

            thead = [thead.extract() for thead in table.findAll('thead')]
            teams = thead[0].findChildren('th', {'width':'40%'})
            away_team, home_team = [team.string.title() for team in teams]

            print("away_team: ", away_team, away_score)
            print("home_team: ", home_team, home_score)

            plays = table.findAll('tr')

            quarter_end = True
            try:
                for play in plays:

                    tds = play.findAll('td')

                    if len(tds) == 4:
                        if ':' in tds[0].text and '-' in tds[2].text:

                            if game_score == tds[2].text:
                                continue
                            else:
                                game_score = tds[2].text

                            quarter_end = False
                            game_time = tds[0].text
                            game_quarter = quarter
                            game_away_score, game_home_score = game_score.split('-')

                            print('play_info: ', game_quarter, game_time, game_away_score, game_home_score)


                            # insert_sql = 'insert into gamelog (game_id, quarter, time_min_sec, away_score, home_score) values(%s, %s, %s, %s, %s)'
                            # mysql_cur.execute(insert_sql, (game_id, game_quarter, game_time, game_away_score, game_home_score))
                            # mysql_conn.commit()

                    elif len(tds) == 2:
                        if tds[1].text == 'End Game':
                            print('End Game')
                            break

                        min, sec = tds[0].text.split(':')
                        if min == '0' and sec == '00' and not quarter_end:

                            quarter += 1
                            quarter_end = True

            except:
                error_game_id.append(game_id)
                continue


            print('quarter_count: ', quarter)

            # update_sql = 'update playbyplay set away_team=%s, home_team=%s, quarter_count=%s, away_score=%s, home_score=%s, status=2 where game_id=%s'
            # mysql_cur.execute(update_sql, (away_team, home_team, quarter, away_score, home_score, game_id))
            # mysql_conn.commit()

            print('test')

    print('done')
    mysql_cur.close()
    mysql_conn.close()
    print('error_game_id', error_game_id)



if __name__ == '__main__':
    main()
