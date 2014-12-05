# coding: utf-8

import sqlite3
from bs4 import BeautifulSoup as bs


def main():
    conn = sqlite3.connect('data01.db')
    cur = conn.cursor()

    #sql = 'select game_id, date, content from playbyplay limit 1;'
    sql = 'select game_id, date, content from playbyplay where game_id = "240221017";'
    cur.execute(sql)

    res = cur.fetchall()

    for item in res:
        game_id = item[0]
        game_date = item[1]
        game_content = item[2]

        print(game_content)

        print('game_id: ', game_id)

        soup = bs(game_content, from_encoding='utf-8')
        table = soup.find('table', {'class': 'mod-data'})

        thead = [thead.extract() for thead in table.findAll('thead')]
        teams = thead[0].findChildren('th', {'width':'40%'})
        away_team, home_team = [team.string.title() for team in teams]

        print("away_team: ", away_team)
        print("home_team: ", home_team)

        plays = table.findAll('tr')

        quarter = 1

        for play in plays:
            tds = play.findAll('td')

            #print(play(text=True))

            if len(tds) == 4:
                if ':' in tds[0].text and '-' in tds[2].text:
                    game_time = tds[0].text
                    game_score = tds[2].text
                    game_quarter = quarter
                    print('play_info: ',game_quarter, game_time, game_score)

            elif len(tds) == 2:
                if tds[1].text == 'End Game':
                    print('End Game')
                    break


                min,sec = tds[0].text.split(':')
                if min == '0' and sec == '00':
                    quarter += 1

        print('done')






if __name__ == '__main__':
    main()
