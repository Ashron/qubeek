# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 20:03:20 2017

@author: KAA
"""
"""
!!! ПРОБЛЕМА ПАРСИНГА КОДА ТИКЕРА НЕ РЕШЕНА !!!
"""

class ShareHelper:
    
#выводит двумерный масси = имя тикера + код.
#Массив, т.к. почему-то некоторые тикеры имеют два кода...
    def get_code(self, symbol):
        share = symbol.lower()
        moexakcii = ShareHelper.get_listcode(self)
        result = [[0]*moexakcii[0].count(share) for i in range(2)]
        l = len(moexakcii[0])
        n = 0
        i = 0
        while n <= 1 :
#            try:
                n = moexakcii[0].index(share,n,l)
                result[0][i] = moexakcii[0][n]
                result[1][i] = moexakcii[1][n]
                n = n+1
                i = i+1
#            except:
#                break
        return [result]

#возвращает список всех тикоеров ммвб и их коды
    def get_listcode(self): 
        from urllib.request import urlopen
        finam_symbols = urlopen('http://www.finam.ru/cache/icharts/icharts.js').readlines()
        moexakcii = finam_symbols[8].decode("utf-8")

        s = 0
        start = '": "moex-akcii/'
        s_len = len(start)
        m_1 = 0
        m_2 = 0
        midle = '","'
        m_len = len(midle)
        e = 0
        end = '": "'

        n = 0
        result = [ [0] * moexakcii.count(start) for i in range(2)]
        while n < moexakcii.count(start) :
            s = moexakcii.find(start,s,len(moexakcii))+s_len
            m_1 = moexakcii.find(midle,s,len(moexakcii))
            m_2 = m_1 + m_len
            e = moexakcii.find(end,m_2,len(moexakcii))
            result[0][n] = moexakcii[s:m_1]
            result[1][n] = moexakcii[m_2:e]
            n = n+1
        return(result)
