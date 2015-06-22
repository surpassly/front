# _*_coding:utf-8_*_
from bs4 import BeautifulSoup
reload(__import__('sys')).setdefaultencoding('utf-8') 

import re
from urllib2 import *
import urlparse

class Paper:
    def __init__(self, title, authors, companies, keywords, abstract, attach):
        self.title = title
        self.authors = authors 
        self.companies = companies
        self.keywords = keywords
        self.abstract = abstract
        self.attach = attach
        temp_companies = []
        if keywords == []:
            keywords.append("NULL")

    
    def __str__(self):
        str = self.title + '\t'
        for group in [self.authors, self.companies, self.keywords]:
            for g in group:
                str += g + '; '
            str += '\t'
        str += self.abstract + '\t'
        str += self.attach
        return str
    
    def display(self):
        str = 'title: ' + self.title + '\nauthors: '
        for a in self.authors:
            str += a + '; '
        str += '\ncompanies: '
        for c in self.companies:
            str += c + '; '
        str += '\nkeywords: '
        for k in self.keywords:
            str += k + '; '
        str += '\nabstracts: '
        str += self.abstract + '\n'
        str += self.attach + '\n===================='
        return str


def getUrlOfPapers():
    targets = []
    urls = ["http://aer.sagepub.com/content/by/year",
            "http://epa.sagepub.com/content/by/year",
            "http://edr.sagepub.com/content/by/year",
            "http://jeb.sagepub.com/content/by/year",
            "http://rer.sagepub.com/content/by/year",
            "http://rre.sagepub.com/content/by/year"]
    
    for url in urls:
        r = urlparse.urlparse(url)    
        host = r.scheme + "://" + r.netloc
        for year in range(2005, 2016):
            location = url + "/%d" % year
            doc = urlopen(location).read()
            soup = BeautifulSoup(doc)
            tds = soup.find_all("td", "proxy-archive-by-year-month")
            for td in tds:
                a = td.find("a")
                t = host + a["href"]
                print '"' + host + a["href"] + '",'
                targets.append(t)
    return targets
                
                
                
def getInfoOfPapers():
    urls = ["http://edr.sagepub.com/content/vol34/issue1/",
"http://edr.sagepub.com/content/vol34/issue2/",
"http://edr.sagepub.com/content/vol34/issue3/",
"http://edr.sagepub.com/content/vol34/issue4/",
"http://edr.sagepub.com/content/vol34/issue5/",
"http://edr.sagepub.com/content/vol34/issue6/",
"http://edr.sagepub.com/content/vol34/issue7/",
"http://edr.sagepub.com/content/vol34/issue8/",
"http://edr.sagepub.com/content/vol34/issue9/",
"http://edr.sagepub.com/content/vol35/issue1/",
"http://edr.sagepub.com/content/vol35/issue2/",
"http://edr.sagepub.com/content/vol35/issue3/",
"http://edr.sagepub.com/content/vol35/issue4/",
"http://edr.sagepub.com/content/vol35/issue5/",
"http://edr.sagepub.com/content/vol35/issue6/",
"http://edr.sagepub.com/content/vol35/issue7/",
"http://edr.sagepub.com/content/vol35/issue8/",
"http://edr.sagepub.com/content/vol35/issue9/",
"http://edr.sagepub.com/content/vol36/issue1/",
"http://edr.sagepub.com/content/vol36/issue2/",
"http://edr.sagepub.com/content/vol36/issue3/",
"http://edr.sagepub.com/content/vol36/issue4/",
"http://edr.sagepub.com/content/vol36/issue5/",
"http://edr.sagepub.com/content/vol36/issue6/",
"http://edr.sagepub.com/content/vol36/issue7/",
"http://edr.sagepub.com/content/vol36/issue8/",
"http://edr.sagepub.com/content/vol36/issue9/",
"http://edr.sagepub.com/content/vol37/issue1/",
"http://edr.sagepub.com/content/vol37/issue2/",
"http://edr.sagepub.com/content/vol37/issue3/",
"http://edr.sagepub.com/content/vol37/issue4/",
"http://edr.sagepub.com/content/vol37/issue5/",
"http://edr.sagepub.com/content/vol37/issue6/",
"http://edr.sagepub.com/content/vol37/issue7/",
"http://edr.sagepub.com/content/vol37/issue8/",
"http://edr.sagepub.com/content/vol37/issue9/",
"http://edr.sagepub.com/content/vol38/issue1/",
"http://edr.sagepub.com/content/vol38/issue2/",
"http://edr.sagepub.com/content/vol38/issue3/",
"http://edr.sagepub.com/content/vol38/issue4/",
"http://edr.sagepub.com/content/vol38/issue5/",
"http://edr.sagepub.com/content/vol38/issue6/",
"http://edr.sagepub.com/content/vol38/issue7/",
"http://edr.sagepub.com/content/vol38/issue8/",
"http://edr.sagepub.com/content/vol38/issue9/",
"http://edr.sagepub.com/content/vol39/issue1/",
"http://edr.sagepub.com/content/vol39/issue2/",
"http://edr.sagepub.com/content/vol39/issue3/",
"http://edr.sagepub.com/content/vol39/issue4/",
"http://edr.sagepub.com/content/vol39/issue5/",
"http://edr.sagepub.com/content/vol39/issue6/",
"http://edr.sagepub.com/content/vol39/issue7/",
"http://edr.sagepub.com/content/vol39/issue8/",
"http://edr.sagepub.com/content/vol39/issue9/",
"http://edr.sagepub.com/content/vol40/issue1/",
"http://edr.sagepub.com/content/vol40/issue2/",
"http://edr.sagepub.com/content/vol40/issue3/",
"http://edr.sagepub.com/content/vol40/issue4/",
"http://edr.sagepub.com/content/vol40/issue5/",
"http://edr.sagepub.com/content/vol40/issue6/",
"http://edr.sagepub.com/content/vol40/issue7/",
"http://edr.sagepub.com/content/vol40/issue8/",
"http://edr.sagepub.com/content/vol40/issue9/",
"http://edr.sagepub.com/content/vol41/issue1/",
"http://edr.sagepub.com/content/vol41/issue2/",
"http://edr.sagepub.com/content/vol41/issue3/",
"http://edr.sagepub.com/content/vol41/issue4/",
"http://edr.sagepub.com/content/vol41/issue5/",
"http://edr.sagepub.com/content/vol41/issue6/",
"http://edr.sagepub.com/content/vol41/issue7/",
"http://edr.sagepub.com/content/vol41/issue8/",
"http://edr.sagepub.com/content/vol41/issue9/",
"http://edr.sagepub.com/content/vol42/issue1/",
"http://edr.sagepub.com/content/vol42/issue2/",
"http://edr.sagepub.com/content/vol42/issue3/",
"http://edr.sagepub.com/content/vol42/issue4/",
"http://edr.sagepub.com/content/vol42/issue5/",
"http://edr.sagepub.com/content/vol42/issue6/",
"http://edr.sagepub.com/content/vol42/issue7/",
"http://edr.sagepub.com/content/vol42/issue8/",
"http://edr.sagepub.com/content/vol42/issue9/",
"http://edr.sagepub.com/content/vol43/issue1/",
"http://edr.sagepub.com/content/vol43/issue2/",
"http://edr.sagepub.com/content/vol43/issue3/",
"http://edr.sagepub.com/content/vol43/issue4/",
"http://edr.sagepub.com/content/vol43/issue5/",
"http://edr.sagepub.com/content/vol43/issue6/",
"http://edr.sagepub.com/content/vol43/issue7/",
"http://edr.sagepub.com/content/vol43/issue8/",
"http://edr.sagepub.com/content/vol43/issue9/",
"http://edr.sagepub.com/content/vol44/issue1/",
"http://edr.sagepub.com/content/vol44/issue2/",
"http://edr.sagepub.com/content/vol44/issue3/",
"http://edr.sagepub.com/content/vol44/issue4/"]
    
    output = open('edr', 'w')

    for url in urls:
        print url
        r = urlparse.urlparse(url)    
        host = r.scheme + "://" + r.netloc  # 得到host用于组合url
        doc = urlopen(url).read()
        soup = BeautifulSoup(doc)
        papers = soup.find_all("li", attrs={"class": re.compile(".*toc-cit")})
        for paper in papers:
            a = paper.find("a", rel="abstract") 
            if not a:
                continue
            title = paper.find("h4", "cit-title-group").text.strip().replace('\n', '')
            # print title
            attach = paper.find("cite").text.replace('\n', '').replace('  ', '').strip() 
            # print attach
            detail_url = host + a["href"]  # authors, companies, keywords, abstract
            doc = urlopen(detail_url).read()
            soup = BeautifulSoup(doc)
            authors = []
            authors_bs = paper.find_all("span", "cit-auth cit-auth-type-author")
            for author in authors_bs:
                authors.append(author.text.strip())
            # print authors
            companies = []
            companies_bs = soup.find_all("address")
            for company in companies_bs:
                company_raw = company.text.replace('\n', '').replace('  ', '').strip()
                if company_raw[0] in ['1', '2', '3', '4', '5', '6', '7', '8']:
                    companies.append(company_raw[1:])
                else:
                    companies.append(company_raw[1:])
            # print companies
            abstract_bs = soup.find("div", "section abstract")
            if abstract_bs:
                abstract_raw = abstract_bs.p.text
            else:
                abstract_raw = soup.find("p", id="p-1").text
            abstract = abstract_raw.replace('\n', '').replace('  ', '')
            # print abstract
            keywords = []
            keywords_bs = soup.find_all("li", "kwd")
            for keyword in keywords_bs:
                keywords.append(keyword.text)
            # print keywords
            p = Paper(title, authors, companies, keywords, abstract, attach)
            print p.display()
            output.write(str(p) + '\n')
    
    output.close()

            
        
#getUrlOfPapers()    
getInfoOfPapers()
    
    
    



            
            
        
