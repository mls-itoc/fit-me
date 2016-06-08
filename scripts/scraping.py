# coding: utf-8
import requests
import re
from pyquery import PyQuery as pq

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
            vals[0] = "{0}/{1}/{2}".format(2000+year,month_day[0],month_day[1])
            f.write('"' + '","'.join(vals) + '"')
            f.write('\n')
f.close()
