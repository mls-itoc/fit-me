# coding: utf-8
import requests
import re
import os
import csv
from pyquery import PyQuery as pq

def create_order():
    f = open("order.csv", "w")
    for year in range(9,16):
        dom = pq(requests.get("http://baseball-data.com/{0}/lineup/c.html".format(year)).text.encode('utf-8'))
        for tr in dom('.lineup tr').items():
            vals = []
            tds = tr.children('td')
            for td in [td for td in tds]:
                if len(td.getchildren()) == 0:
                    vals.append(td.text)
                else:
                    vals.append(td.getchildren()[0].text)
            if len(vals) > 0:
                month_day = re.split('[月|日]',vals[0])[:2]
                vals.remove(vals[0])
                vals.insert(0, month_day[1])
                vals.insert(0, month_day[0])
                vals.insert(0, str(2000+year))
                f.write('"' + '","'.join(vals) + '"')
                f.write('\n')
    f.close()

def create_result():
    def writeline(f, id, year, response_text):
        dom = pq(response_text)
        vals = re.split('[月|日|　]', dom(id).html())
        vals.insert(0, str(year))

        index = 0
        for td in dom('.score table tr')[0]:
            if td.text == "R":
                for tr in dom('.score table tr')[1:3]:
                    team_src = tr.getchildren()[0].getchildren()[0].attrib.get('src')
                    vals.insert(3, os.path.splitext(os.path.basename(team_src))[0])
                    img_src = tr.getchildren()[index].getchildren()[0].attrib.get('src')
                    vals.insert(4, os.path.splitext(os.path.basename(img_src))[0])
            index += 1

        score1 = vals[4]
        score2 = vals[6]
        if vals[3] == 'chiroshima':
            if score1 > score2:
                vals.insert(len(vals), "1")
            elif score1 < score2:
                vals.insert(len(vals), "0")
            else:
                vals.insert(len(vals), "")
        else:
            if score1 > score2:
                vals.insert(len(vals), "0")
            elif score1 < score2:
                vals.insert(len(vals), "1")
            else:
                vals.insert(len(vals), "")

        f.write('"' + '","'.join(vals) + '"')
        f.write('\n')

    def output(url, f, id, year, code):
        count = 1
        response = requests.get(url.format(year,code,count))
        while response.status_code == 200:
            response.encoding = "Shift_JIS"
            writeline(f, '.data-' + id + ' span', year, response.text)
            count += 1
            response = requests.get(url.format(year,code,count))

    f = open("result.csv", "w")
    for year in range(2009,2016):
        print("year=>"+str(year))
        # 公式戦
        for code in ["SC", "GC", "TC", "CD", "CY"]:
            print("  code=>"+code)
            output("http://2689web.com/{0}/{1}/{1}{2}.html", f, 'ce', year, code)
        # 交流戦
        for code in ["CH", "CF", "CM", "CL", "CB", "CE"]:
            print("  code=>"+code)
            output("http://2689web.com/{0}/inter/{1}{2}.html", f, 'in', year, code)
    f.close()

def ml_data():
    def key(row):
        return "{0}-{1}-{2}".format(row[0],row[1],row[2])
    table = {}
    for row in csv.reader(open('order.csv', 'r')):
        row.insert(len(row), "")
        table[key(row)] = row[3:]
    for row in csv.reader(open('result.csv', 'r')):
        if key(row) in table:
            val = table[key(row)]
            val[len(val)-1] = row[11]
    f = open("ml_data.csv", "w")
    f.write("１番,２番,３番,４番,５番,６番,７番,８番,９番,結果\n")
    for row in table.values():
        if row[len(row)-1] != '':
            f.write('"' + '","'.join(row) + '"')
            f.write('\n')
    f.close()

# create_order()
# create_result()
ml_data()
