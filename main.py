import requests
import csv
import io
import datetime
#import psycopg2
import json


'''
def connect():
    config = json.load(open('config.json'))

    return psycopg2.connect(
         dbname   = config['database']
        ,user     = config['user']
        ,password = config['password']
        ,host     = config['host']
        ,port     = config['port']
    )
'''


def downloadSheetAsCsv():
    sheet_id = '1_BkMcHbeAGuMVearIuEiICOV6ae6VJUQ0QYOv9uCM9A'
    url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&id={sheet_id}&gid=0'

    req = requests.get(url)
    req.encoding = 'utf-8'

    return req.text


"""
def updateEvent(connection, date, description):
    cur = connection.cursor()
    cur.execute('''
        INSERT INTO events (date, description)
        VALUES (%s, %s)
        ON CONFLICT (date) DO UPDATE
          SET description = excluded.description;
    ''', (date, description))
    connection.commit()
"""


if __name__ == '__main__':
    #connection = connect()

    csv_str = downloadSheetAsCsv()
    data = csv.reader(io.StringIO(csv_str), delimiter=',')
    data.__next__() # skip first row

    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    html_segment = ''
    for row in data:
        dateStr = row[0]
        date = datetime.datetime.strptime(dateStr, '%Y-%m-%d')
        descr = row[1]

        if len(descr) == 0: continue
        if date < today: continue

        dateFmt = datetime.datetime.strftime(date, '%Y-%m-%d')
        html_segment += f'<tr><td>{dateFmt}</td><td>{descr}</td></tr>'
        #updateEvent(connection, date, descr)

    with open('index_template.html') as f:
        html_template = f.read()

    with open('index.html', 'w') as f:
        f.write(html_template.replace('{{EVENTS}}', html_segment))
