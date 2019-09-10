import requests
import csv
import re
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from pylab import rcParams
from bs4 import BeautifulSoup 
url = "https://www.hubertiming.com/results/2017GPTR10K"
r = requests.get(url)
soup = BeautifulSoup(r.content,'html5lib')
# quotes = []
# print(soup.title) 
text =  soup.get_text()
# print(text)
# all_links = soup.find_all("a")
# for link in all_links:
#     print(link.get("href"))
rows = soup.find_all('tr')
# print(rows[:10])
for row in rows:
    row_td = row.find_all('td')
# print(row_td)
type(row_td)
str_cells = str(row_td)
cleantext = BeautifulSoup(str_cells, "lxml").get_text()
# print(cleantext)
list_rows = []
for row in rows:
    cells = row.find_all('td')
    str_cells = str(cells)
    clean = re.compile('<.*?>')
    clean2 = (re.sub(clean, '',str_cells))
    list_rows.append(clean2)
# print(clean2)
type(clean2)
df = pd.DataFrame(list_rows)
df.head(10)

df1 = df[0].str.split(',', expand=True)
df1.head(10)
# print(df1)

col_labels = soup.find_all('th')
all_header = []
col_str = str(col_labels)
cleantext2 = BeautifulSoup(col_str, "lxml").get_text()
all_header.append(cleantext2)
# print(all_header)
df2 = pd.DataFrame(all_header)
df2.head()
df3 = df2[0].str.split(',', expand=True)
df3.head()
frames = [df3, df1]

df4 = pd.concat(frames)
df4.head(10)
# print(df4)

df5 = df4.rename(columns=df4.iloc[0])
df5.head()
# print(df5)
# df5.info()
# df5.shape

df6 = df5.dropna(axis=0, how='any')
# print(df6)
df7 = df6.drop(df6.index[0])
df7.head()
# print(df7)

time_list = df7[' Chip Time'].tolist()
# print(time_list)
# You can use a for loop to convert 'Chip Time' to minutes

time_mins = []
for i in time_list:
    # print(i)
    try:
        h, m, s = str(i).split(':')
    except:
        m,s = str(i).split(':')
        h = 0
    math = (int(h) * 3600 + int(m) * 60 + int(s))/60
    time_mins.append(math)
# print(time_mins)
# for i in time_mins:
#     print(i)
df7['Runner_mins'] = time_mins
df7.head()
df7.describe(include=[np.number])
# print(df7)

rcParams['figure.figsize'] = 15, 5
df7.boxplot(column='Runner_mins')
plt.grid(True, axis='y')
plt.ylabel('Chip Time')
plt.xticks([1], ['Runners'])
x = df7['Runner_mins']
ax = sns.distplot(x, hist=True, kde=True, rug=False, color='m', bins=25, hist_kws={'edgecolor':'black'})


f_fuko = df7.loc[df7[' Gender']==' F']['Runner_mins']
m_fuko = df7.loc[df7[' Gender']==' M']['Runner_mins']
sns.distplot(f_fuko, hist=True, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Female')
sns.distplot(m_fuko, hist=False, kde=True, rug=False, hist_kws={'edgecolor':'black'}, label='Male')
plt.legend()
plt.show()
g_stats = df7.groupby(" Gender", as_index=True).describe()
print(g_stats)