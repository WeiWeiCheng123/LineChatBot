from bs4 import BeautifulSoup
from abc import ABC, abstractmethod
import requests

class Scrape:

    def __init__(self,name):
        self.name=name
    
    def real_stock(self):
        response = requests.get("https://tw.stock.yahoo.com/quote/"+ self.name+ "/news")

        return response.ok

    def get_web(self):
        response = requests.get("https://tw.stock.yahoo.com/quote/"+ self.name+ "/news")
        soup = BeautifulSoup(response.content,"html.parser")
        news = soup.find_all('div',{'class': 'Ov(h) Pend(14%) Pend(44px)--sm1024'},limit=5)
        message = ""
        news_list = []
        news_link = []
        content = []

        if response.ok:

            for new in news:
                title = new.find('a',{'class':'Fw(b) Fz(20px) Fz(16px)--mobile Lh(23px) Lh(1.38)--mobile C($c-primary-text)! C($c-active-text)!:h LineClamp(2,46px)!--mobile LineClamp(2,46px)!--sm1024 mega-item-header-link Td(n) C(#0078ff):h C(#000) LineClamp(2,46px) LineClamp(2,38px)--sm1024 not-isInStreamVideoEnabled'}).getText()
                news_content = new.find('p',{'class':'Fz(16px) Lh(24px) LineClamp(2,48px) C($c-secondary-text) M(0)'}).getText()
                link = new.find("a").get('href')
                news_list.append(title)
                news_link.append(str(link))
                content.append(news_content)

            stock_name = soup.find("h2",{"class":"Fz(24px) Fz(20px)--mobile Fw(b) C($c-primary-text) Mb(5px)"}).getText()
            return stock_name, news_list, news_link, content
        else:
            content = "找無此股票代號"
            return content