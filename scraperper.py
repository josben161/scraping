import whoosh
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup, AndGroup
import urllib.request as urllib2
from lxml import cssselect, html
import urllib.request as urllib2
import re

def getlinksfromurl(URL):
    response = urllib2.urlopen(URL)
    htmlString = response.read()
    stringreal = htmlString.decode()
    dochtml = html.fromstring(htmlString)
    select = cssselect.CSSSelector("a")
    links = [el.get('href') for el in select(dochtml)]
    updated_links = []
    eh = 'https:'
    for link in links:
        if link[0:6] == eh:
            updated_links.append(link)
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', stringreal)
    return updated_links, emails

updated_links, emails = getlinksfromurl('https://sydney.edu.au/engineering/study-engineering-and-it.html')
#https://sydney.edu.au/engineering/study-engineering-and-it.html
new_queue = []
for i in updated_links:
    if len(new_queue) <= 99:
        new_queue.append(i)


def getemailsandcontentfromurl(URL):
    response = urllib2.urlopen(URL)
    htmlString = response.read()
    stringreal = htmlString.decode()
    dochtml = html.fromstring(htmlString)
    emails = re.findall(r'[\w\.-]+@[\w\.-]+', stringreal)
    return URL, stringreal, emails

i = 0
combined =[]
for new in new_queue:
    i = i+1
    URLsub, stringreal, emailssub = getemailsandcontentfromurl(new)
    pingping = ["replaced"]
    if emailssub == []:
        emailssub = pingping
    results = (URLsub, stringreal, emailssub)
    combined.append(results)
#print(combined)    
    
#CREATE THE DATABASE

schema = Schema(title=ID(stored=True), content=TEXT(stored=True), emails=TEXT (stored = True), )
ix = create_in(".", schema)

writer = ix.writer()

for text in combined:
    writer.add_document(title = text[0],
                        content = text[1],
                        emails = text[2])

writer.commit(optimize=True)

#print(combined[1])
#for i in combined:
#    text = i[0]
#    content = i[1]
#    emails = i[2]
#    #print(text)
#    #print(content)
#    print(emails)

#Creating the Search
searcher = ix.searcher()
parser = MultifieldParser(["title", "path", "content"], schema = ix.schema, group=OrGroup)
stringquery = parser.parse("internship")
print ("this is our parsed query: " + str(stringquery))
results = searcher.search(stringquery)
print ("search 1 result:")
print (results)
for r in results:
    print (r)
    