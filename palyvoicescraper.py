#!/usr/bin/env python
from bs4 import BeautifulSoup
import urllib2
import unicodedata
import io

articleItems = []

def scrape(soup):
    stories = soup.find_all(class_ = 'stories-list grid_12')[0]
    for listing in stories.find_all('li'):
            for i in listing.find_all(class_ = 'info'):
                #Extract title and link
                link = i.find(class_ = 'title').find('a')['href']
                raw_title = i.find(class_ = 'title').find('a').text
                title = unicodedata.normalize('NFKD', raw_title).encode('ascii','ignore').strip()
                
                #Extract date from byline
                byline = i.find(class_ = 'byline')
                cut = byline.text.find(u'\u2014')
                date = str(byline.text[:cut-1]).strip()
                
                #join relevant fields togther in HTML syntax
                html = '\t<li> <a href =' + link + '>' + title + ' ' + u'\u2014' + ' ' + date + '</a> </li>'
                articleItems.append(html)
                
if __name__ == '__main__':
    
    fileName = raw_input("File name: ") + '.txt'
    
    r = urllib2.urlopen('http://palyvoice.com/author/chyu15/')
    soup = BeautifulSoup(r, "html.parser")
    scrape(soup)
    
    #Check if more pages exist
    while soup.find(class_ = 'paginator paginator-more') is not None:
        nextpage = soup.find(class_ = 'paginator paginator-more').find('a')['href']
        r = urllib2.urlopen(nextpage)
        soup = BeautifulSoup(r, "html.parser")
        scrape(soup)
        
    with io.open(fileName, 'w', encoding = 'utf8') as file:
        file.write(unicode('<ul>'))
        file.write('\n'.join(articleItems))
        file.write(unicode('</ul>'))
        