from tkinter import W
import requests as req
from bs4 import BeautifulSoup
from enum import Enum

class Spider :
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }

    def get_soup(self, url) :
        html = req.get(url, headers=self.headers)
        soup = BeautifulSoup(html.text, 'html.parser')
        return soup


class JournalSpider(Spider) :
    def __init__(self, url, date) :
        self.url = url + "?date=" + date
        self.journal_list = self.get_all_journal_list()
        
    def get_journal_id(self, string) :
        idx1 = string.rfind('/') 
        id = string[idx1 - 3 : idx1]
        return id

    def get_journal_list(self, tag) :
        boxes = tag.find_all(class_ = 'rankingnews_box')
        journal_list = []
        for box in boxes :
            a = box.find('a')
            view_link = a['href']
            id = self.get_journal_id(view_link)
            name = box.find(class_='rankingnews_name').text
            comment_link = view_link.replace('popular','comment')
            journal ={
                'id' : id,
                'name' : name,
                'view_link' : view_link,
                'comment_link' : comment_link
            }
            journal_list.append(journal)

        return journal_list

        
    def get_all_journal_list(self) :
        soup = self.get_soup(self.url)
        cards = soup.find_all(class_="_officeCard")
        result = []
        for card in cards :
            journal_list = self.get_journal_list(card)
            result.extend(journal_list)
        return result 
    
    def get_journal_by_name(self, name) :
        for journal in self.journal_list :
            if journal['name'] == name :
                return journal
    
    def get_journal_by_id(self, id) :
        for journal in self.journal_list :
            if journal['id'] == id :
                return journal

    # def get_journal_info_by_date(self, date) :
    #     dated_journal_list = []
    #     for journal in self.journal_list :
    #         journal['view_link'] += '?date=' + date
    #         journal['comment_link'] += '?date=' + date
    #         dated_journal_list.append(journal)
        
    #     return dated_journal_list
        
class View :
    def print_news_list(self, news_list) :
        for news in news_list :
            self.print_news(news)

    def print_journal_list(self, journal_list) :
        for journal in journal_list :
            self.print_journal(journal)

    def print_news(self, news):
        print(f"id : {news['id']}")
        print(f"ranking : {news['ranking']}")
        print(f"title : {news['title']}")
        print(f"link : {news['link']}")
        print(f"date : {news['date']}")
        print("==================================================")

    def print_journal(self, journal) :
        print(f"id : {journal['id']}")
        print(f"name : {journal['name']}")
        print(f"view_link : {journal['view_link']}")
        print(f"comment_link : {journal['comment_link']}")
        print("==================================================")

class ScrapUtil:
    @staticmethod
    def get_formated_date(date) :
        year = date[:4:]
        month = date[4:6]
        day = date[6:8]

        sep = '.'
        return year + sep + month + sep + day



class NewsSpider(Spider) :
    def get_news_id(self, string) :
        idx1 = string.rfind('/') 
        idx2 = string.find('?') 
        id = string[idx1 + 1 : idx2]
        return id

    def get_my_news(self, elem) :

        link = elem.find('a')['href'] 
        id = self.get_news_id(link) 
        ranking = elem.find('em').text
        title = elem.find(class_="list_title").text
        news = {
            'id' : id,
            'ranking' : int(ranking),
            'title' : title,
            'link' : link
        }

        return news

    def get_rangking_list(self, url) : 
        print(url)
        soup = self.get_soup(url)
        li_list = soup.find(class_='press_ranking_list').find_all(class_='as_thumb')
        date = soup.find(class_='press_ranking_date')['data-init-date']
        my_news_list = []
        for li in li_list :
            news = self.get_my_news(li)
            news['date'] = ScrapUtil.get_formated_date(date)
            my_news_list.append(news)
        
        return my_news_list
    
class CommentSpider(Spider):

    class CommentPage(Enum) :
        NoneStatistics = 0,
        ExistStatistics = 1
    def __init__(self) :
        self.domain = 'https://n.news.naver.com'                

    def set_domain(self, url) :
        self.domain = url

    def get_comment_type(self, char_fold) :

        if char_fold == None : 
            return self.CommentPage.NoneStatistics
        else :
            return self.CommentPage.ExistStatistics
        
    def get_comment_info(self, url) :
        page = self.get_soup(url)
        comment_link_tag = page.find(id='comment_count')

        link_url = self.get_comment_link(comment_link_tag)
        page = self.get_soup(link_url)

        char_fold = page.find(class_='u_cbox_chart_fold')
        comment_type = self.get_comment_type(char_fold) 
        print('comment_type', comment_type)
        if comment_type == self.CommentPage.NoneStatistics : 
            return None
             
        cnts = self.get_comment_cnts(page)
        sexes = self.get_comment_sexes(page)
        ages = self.get_comment_ages(page)

        comment_info = {
            'cnt' : cnts,
            'sex' : sexes,
            'age' : ages
        }

        return comment_info

    def get_comment_link(self, link_tag) :
        link = link_tag['href']
        if self.domain != None :
            return self.domain + link
        
    def get_comment_cnts(self, page) :
        cnt = int(page.find(class_='u_cbox_count_info').find(class_='u_cbox_info_txt').text)
        return cnt

    def get_comment_sexes(self, page) :
        male = page.find(class_='u_cbox_chart_sex').find(class_='u_cbox_chart_progress u_cbox_chart_male') \
            .find(class_='u_cbox_chart_per')
        female = page.find(class_='u_cbox_chart_sex').find(class_='u_cbox_chart_progress u_cbox_chart_female') \
            .find(class_='u_cbox_chart_per')

        sex_info = {
            'male' : male,
            'female' : female
        }

        return sex_info
    
    def get_comment_ages(self, page) :
        age_tags = page.find(class_='u_cbox_chart_age').find_all(class_='u_cbox_chart_progress')
        
        age_info = {}
        for age in age_tags :
            age_txt = age.find(class_='u_cbox_chart_cnt').text
            age_per = age.find(class_='u_cbox_chart_per').text
            age_info[age_txt] = age_per
        
        return age_info 

class MyScraper() :
    def __init__(self, url, date) :
        self.journal = JournalSpider(url, date)
        self.news = NewsSpider()
        self.comment = CommentSpider()

    def get_news_list(self, journal_url) :
        news_list = self.news.get_rangking_list(journal_url)
        return news_list 

    def get_all_journal(self) :
        return self.journal.get_all_journal_list()

    def get_journal_by_name(self, name) :
        return self.journal.get_journal_by_name(name)
    
    def get_news_by_journal(self, journal) :
        return self.news.get_rangking_list(journal['view_link'])

    def get_news_with_comment_rank(self,journal) :
        return self.get_news_list(journal['comment_link'])

    def get_news_with_view_rank(self,journal) :
        return self.get_news_list(journal['view_link'])

    # def get_news_by_date(self, date) :
    #     journal_list = self.journal.get_journal_info_by_date(date)
    #     # news_list_all = []
    #     # for journal in journal_list :
    #     #     news_list = self.get_news_with_comment_rank(journal)
    #     #     news_list_all.extend(news_list)
    #     # return news_list_all
    #     return journal_list

    def get_comment_info_of_news(self, news) :
        return self.comment.get_comment_info(news['link'])
    
    def get_comment_infos_of_journal(self, journal) :
        comment_info_list = []
        for news in self.news.get_rangking_list(journal) :
            comment = self.get_comment_info_of_news(news)
            comment_info_list.append(comment)
        return comment_info_list

    def get_ranking_difference(self, list1, list2) :
        list1.sort(key = lambda element : element['id'])
        list2.sort(key = lambda element : element['id'])
        accu_list = []
        for item1, item2 in zip(list1, list2) :
            accu_list.append(abs(item1['ranking'] - item2['ranking']))
        return accu_list

    def get_accuracy(self,list1, list2):
        ac_list = self.get_ranking_difference(list1, list2)
        result = []
        for ac in ac_list :
            result.append(100 - (5 * ac))
        
        return sum(result) / len(result)

        
