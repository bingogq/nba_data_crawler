# coding: utf-8



import datetime



def main():
    start_date_str = '20021006'
    end_date_str = '20141123'

    start_date = datetime.datetime.strptime(start_date_str, '%Y%m%d')
    end_date = datetime.datetime.strptime(end_date_str, '%Y%m%d')
    week_date = datetime.timedelta(weeks=1)

    url_prefix = 'http://scores.espn.go.com/nba/scoreboard?date='

    while True:
        if start_date > end_date:
            print(start_date)
            print(end_date)
            break

        url_date = start_date.strftime('%Y%m%d')

        # @todo:


        start_date += week_date

if __name__ == '__main__':
    main()