# -*- coding: utf-8 -*-
"""
Created on Wed May 31 23:02:22 2017

@author: KAA
"""

"""
Выгрузка истории котировок акций ММВБ с портала Финам
"""
"""
Example Export Link:
http://export.finam.ru/
        MTLRP_170101_171231.csv?market=1
        &em=80745
        &code=MTLRP
        &apply=0
        &df=1
        &mf=0
        &yf=2017
        &from=01.01.2017
        &dt=31
        &mt=11
        &yt=2017
        &to=31.12.2017
        &p=7
        &f=MTLRP_170101_171231
        &e=.txt
        &cn=MTLRP
        &dtf=1
        &tmf=1
        &MSOR=1
        &mstime=on
        &mstimever=1
        &sep=1
        &sep2=1
        &datf=1
        &at=1
        
Имя параметра   Назначение	Пример
market          Номер рынка	5
em              Номер инструмента	86
code            Тикер инструмента	GBPUSD
df              Начальная дата, номер дня (1-31)	1
mf              Начальная дата, номер месяца (0-11)	11
yf              Начальная дата, год	2014
from            Начальная дата	01.12.2014
dt              Конечная дата, номер дня	6
mt              Конечная дата, номер месяца	11
yt              Конечная дата, год	2014
to              Конечная дата	06.12.2014
f               Имя сформированного файла	GBPUSD_141201_141206
p               Таймфрейм	2
e               Расширение сформированного файла	.csv
cn              Имя контракта	GBPUSD
dtf             Номер формата дат	1
tmf             Номер формата времени	3
MSOR            Время свечи (0 - open; 1 - close)	1
mstime          Московское время	on
mstimever       Коррекция часового пояса	1
sep             Разделитель полей	3
sep2            Разделитель разрядов	1
datf            Формат записи в файл	5
at              Нужны ли заголовки столбцов	1        
"""

from urllib.request import urlopen # Импортировали библиотеку для работы с адресами и запросами Internet.
url = "http://export.finam.ru/MTLRP_170101_171231.txt?market=1&em=80745&code=MTLRP&apply=0&df=1&mf=0&yf=2017&from=01.01.2017&dt=31&mt=11&yt=2017&to=31.12.2017&p=7&f=MTLRP_170101_171231&e=.txt&cn=MTLRP&dtf=1&tmf=1&MSOR=1&mstime=on&mstimever=1&sep=3&sep2=1&datf=5&at=1"
f = urlopen(url)   # Открыли соединение.
data1 = f.read()   # Прочитали данные.
f.close()          # Закрыли соединение.

print(data1[:500]) # Первые 500 символов полученных данных.


# форматирование
from pandas import read_csv  # Чтобы упаковать результат в 
# стандартный DataFrame.
data = read_csv(url, header=0, index_col=0, parse_dates={'Date&Time': [0, 1]}, sep=';').sort_index()
data.columns = ['' + i for i in ['Open', 'High', 'Low', 'Close', 'Volume']] # Заголовки столбцов

from pandas import set_option
set_option('display.max_columns', 50) # Кол-во колонок
set_option('display.width', 500)      # и ширина поля вывода
                                      # (чтобы при выводе не переносило широкие таблицы).

print(data.head())  # Вывели первые строки набора данных.


# формирование строки с произвольными параметрами
from urllib.parse import urlencode
from datetime import datetime
periods = {'tick': 1, 'min': 2, '5min': 3, '10min': 4, '15min': 5, '30min': 6, 
                                   'hour': 7, 'daily': 8, 'week': 9, 'month': 10}
FINAM_URL = "http://export.finam.ru/table.csv?"
market = 1
start_date_str = "01.01.2016"
end_date_str = "31.12.2017"
start_date = datetime.strptime(start_date_str, "%d.%m.%Y").date()
end_date = datetime.strptime(end_date_str, "%d.%m.%Y").date()
period = 1
symbol_code = 80745
symbol = "MTLRP"
# Формируем строку с параметрами запроса:
params = urlencode([('market', 5), ('em', symbol_code), ('code', symbol),
                   ('df', start_date.day), ('mf', start_date.month - 1), ('yf', start_date.year),
                   ('from', start_date_str),
                   ('dt', end_date.day), ('mt', end_date.month - 1), ('yt', end_date.year),
                   ('to', end_date_str),
                   ('p', period), ('f', "table"), ('e', ".csv"), ('cn', symbol),
                   ('dtf', 1), ('tmf', 3), ('MSOR', 1), ('mstime', "on"), ('mstimever', 1),
                   ('sep', 3), ('sep2', 1), ('datf', 5), ('at', 1)])

url = FINAM_URL + params # Полная строка адреса со всеми параметрами.
# Соединяемся с сервером, получаем данные и выполняем их разбор:
#data = read_csv(url, header=0, index_col=0, parse_dates={'Date&Time': [0, 1]}, sep=';').sort_index()
data.columns = ['' + i for i in ['Open', 'High', 'Low', 'Close', 'Volume']] # Заголовки столбцов
print(data.head())

finam_symbols = urlopen('http://www.finam.ru/cache/icharts/icharts.js').readlines()
print(finam_symbols)

str_id = str(finam_symbols[0])  
str_code = str(finam_symbols[2])

start = str(str_code).find("[\'") + 2
end = str_code.find("\']")
names = str_code[start : end].split('\',\'')
ids = str_id[str_id.find('[') + 1 : str_id.find(']')].split(',')
if symbol in names: # Если искомый тикер symbol имеется в списке names.
    k = 0
    for i, name in enumerate(names):
        if name == symbol:
            k = i
            break
    symbol_code = ids[k]
    print(symbol_code)
else:
    raise Exception("%s not found\r\n" % symbol)