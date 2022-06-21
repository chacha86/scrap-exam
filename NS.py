import requests as req
from bs4 import BeautifulSoup

class Spider :
    def __init__(self) :
        self.headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
        }

    def get_soup(self, url) :
        html = req.get(url, headers=self.headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup


class JournalSpider(Spider) :

    def get_journal_id(self, string) :
        idx1 = string.rfind('/') 
        id = string[idx1 - 3 : idx1]
        return id

    def get_journal_list(self, tag) :
        boxes = tag.find_all(class_ = 'rankingnews_box')
        journal_list = []
        for box in boxes :
            a = box.find('a')
            link = a['href']
            id = self.get_journal_id(link)
            name = box.find(class_='rankingnews_name')

            journal ={
                'id' : id,
                'name' : name,
                'link' : link
            }
            journal_list.append(journal)

        return journal_list

        
    def get_all_journal_list(self, url) :
        soup = self.get_soup(url)
        cards = soup.find_all(class_="_officeCard")
        result = []
        for card in cards :
            journal_list = self.get_journal_list(card)
            result.extend(journal_list)
        return result 
    
class ArticleSpider(Spider) :
    def get_article_id(string) :
        idx1 = string.rfind('/') 
        idx2 = string.find('?') 
        id = string[idx1 + 1 : idx2]
        return id

    def get_my_article(self, elem) :

        domain = "https://n.news.naver.com"
        href = elem.find('a')['href'] 

        link = domain + href 
        id = self.get_article_id(link) 
        ranking = elem.find('em').text
        title = elem.find(class_="list_title").text
        
        article = {
            'id' : id,
            'ranking' : int(ranking),
            'title' : title,
            'link' : link
        }

        return article

    def get_rangking_list(self, url) : 
        soup = self.get_soup(url)
        li_list = soup.find(class_='press_ranking_list').find_all('li')
        my_articles = []
        for li in li_list :
            article = self.get_my_article(li)
            my_articles.append(article)
        
        return my_articles
