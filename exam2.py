from NS import MyScraper, View, JournalSpider, Spider

url = 'https://news.naver.com/main/ranking/popularDay.naver'
sc = MyScraper(url, '20200619')
url2 = 'https://news.naver.com/main/ranking/popularMemo.naver'
sc2 = MyScraper(url2, '20200619')
view = View()

# news = sc.get_all_news()
# view.print_news_list(news)

# jlist = sc.get_all_journal()
# view.print_journal_list(jlist)

# j = sc.get_journal_by_name('뉴스타파')
# view.print_journal(j)
# news_list = sc.get_news_by_journal(j)
# view.print_news_list(news_list)

# news_list1 = sc.get_all_news()
# news_list2 = sc2.get_all_news()

# print(sc.get_accuracy(news_list1, news_list2)) # 오차율 16%...

# view.print_news_list(news_list)
# journal = sc.get_journal_by_name('MBC')
# news_list = sc.get_news_with_comment_rank(journal)
# view.print_news_list(news_list)
# cinfo = sc.get_comment_info_of_news(news_list[0])
# print(cinfo)

sp = Spider()
soup = sp.get_soup('https://n.news.naver.com/article/comment/214/0001204141')
print(soup.find(id='cbox_module'))