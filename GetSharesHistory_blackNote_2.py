from pandas import read_csv  # Чтобы упаковать результат в DateFrame
from datetime import datetime
from sharehelper import ShareHelper

#transneft-pref  :  1012
#transneft-pref  :  152697
#IN:
ticker = 'gruppa-cherkizovo-ao'
start_date_str = "01.01.2000"
end_date_str = "31.12.2017"
timeframe = 9


#--========================================
sh = ShareHelper()  
tickercode = sh.get_code(ticker)[0]
#tickercode = 20125
market=1
filetype = 'txt'

start_date = datetime.strptime(start_date_str, "%d.%m.%Y").date()
end_date = datetime.strptime(end_date_str, "%d.%m.%Y").date()



filename = (ticker+'_'+str(start_date.year)+str(start_date.month)+str(start_date.day)
                +'_'+str(end_date.year)+str(end_date.month)+str(end_date.day))

url = ('http://export.finam.ru/'
        '{0}?'              
        'market={1}'            
        '&em={2}'
        '&code={3}'
        '&apply={4}'
        '&df={5}'
        '&mf={6}'
        '&yf={7}'
        '&from={8}'
        '&dt={9}'
        '&mt={10}'
        '&yt={11}'
        '&to={12}'
        '&p={13}'           #timeframe	7 - час, 8 - день
        '&f={14}'
        '&e=.txt'
        '&cn={15}'
        '&dtf={16}'
        '&tmf={17}'
        '&MSOR={18}'
        '&mstime={19}'
        '&mstimever={20}'
        '&sep={21}'
        '&sep2={22}'
        '&datf={23}'
        '&at={24}'              
        ).format(filename+filetype,market,tickercode
                            ,ticker,0,start_date.day,start_date.month-1,start_date.year
                            ,start_date,end_date.day,end_date.month-1,end_date.year
                            ,end_date,timeframe,filename,ticker
                            ,1,1,1,'on',1,3,1,5,1)
print(url)
## стандартный DataFrame. и вывод
data = read_csv(url, header=0, index_col=0, parse_dates={'Date&Time': [0, 1]}, sep=';').sort_index()
#data.columns = ['' + i for i in ['Open', 'High', 'Low', 'Close', 'Volume']] # Заголовки столбцов
#
#from pandas import set_option
#set_option('display.max_columns', 50) # Кол-во колонок
#set_option('display.width', 500)      # и ширина поля вывода
#                                      # (чтобы при выводе не переносило широкие таблицы).

data.to_csv(filename+".csv",set = ',')

