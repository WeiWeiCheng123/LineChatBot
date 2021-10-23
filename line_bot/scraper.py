from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests

class Scrape:

    def __init__(self,name):
        self.name=name
        
    def get_web(self):
        response = requests.get("https://tw.stock.yahoo.com/quote/"+ self.name+ "/news")
        soup = BeautifulSoup(response.content,"html.parser")
        news = soup.find_all('div',{'class': 'Ov(h) Pend(14%) Pend(44px)--sm1024'},limit=5)
        content = ""
        if len(news) != 0:

            for new in news:
                title = new.find('a',{'class':'Fw(b) Fz(20px) Fz(16px)--mobile Lh(23px) Lh(1.38)--mobile C($c-primary-text)! C($c-active-text)!:h LineClamp(2,46px)!--mobile LineClamp(2,46px)!--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'}).getText()
                link = new.find("a")
                content += title + "\n" +link.get('href')+ "\n"

            stock_name = soup.find("h2",{"class":"Fz(24px) Fz(20px)--mobile Fw(b) C($c-primary-text) Mb(5px)"}).getText()
            return stock_name + "\n" + content
        else:
            content = "找無此股票代號"
            return content
