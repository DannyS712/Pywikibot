import pywikibot
import pymysql
import os
import re

conn = pymysql.connect(
    host=os.environ['MYSQL_HOST'],
    user=os.environ['MYSQL_USERNAME'],
    password=os.environ['MYSQL_PASSWORD'],
    database='enwiki_p',
    charset='utf8',
)

with conn.cursor() as cur:
    cur.execute('use enwiki_p')
    cur.execute("SELECT DISTINCT cl_to FROM categorylinks WHERE cl_from IN (select page_id from page where page_namespace = 118) and cl_to not like '%AfC%' and cl_to not like '%raft%' and cl_to not like '%Pages%' and cl_to not like '%pages%' and cl_to not like '%edirect%' and cl_to not like '%CS1%' and cl_to not like '%deletion%' and cl_to not like '%rticles%' and cl_to not like '%emplate%' and cl_to not like '%with%' and cl_to not like '%tracking%'")
    drafts = cur.fetchall()
#    print( drafts )

drafts = '\n'.join( map(str, drafts) )
drafts = re.sub(r"\(+b'(.*?)',\)+(, )?", r"* [[:Category:\1]]", drafts )
drafts = re.sub(r'\(+b"(.*?)",\)+(, )?', r"* [[:Category:\1]]", drafts )
drafts = drafts.replace( '_', ' ')
print( drafts )

site = pywikibot.Site('test', 'wikipedia')
page = pywikibot.Page(site, 'User:DannyS712 bot/DBR')
page.text = drafts
page.save( summary = 'Task 28: Update database report', minor = False )
