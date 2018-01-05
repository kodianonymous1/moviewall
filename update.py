# -*- coding: utf-8 -*-
import os,requests,urllib,urllib2,re,random,socket
import time,logging,base64,urlparse,HTMLParser,itertools
import threading,StringIO,gzip
import datetime,json,cookielib,sys
import pip
from urllib import urlencode


TMDB_API_URL = "http://api.themoviedb.org/3/"
TMDB_API_KEY = '34142515d9d23817496eeb4ff1d223d0'
__USERAGENT__ = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.97 Safari/537.11'
json_series_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'all_data_series.json')
if not (os.path.isfile(json_series_file)):
	f = open(json_series_file, 'w') 
	my_json_string=('[{"lastupdate": {"1": "2017-07-26 15:26:57"}, "tmdb": "", "title": "\u05e7\u05d0\u05e1\u05dc\u05d1\u05e0\u05d9\u05d4", "tvdb": "", "season": {"1": "2"}, "trakt": "", "imdb": "tt6517102", "year": "1982"}, {"lastupdate": {"1": "2017-07-26 15:26:57"}]')
	f.write(json.dumps(my_json_string)) 
	f.close() 
json_series_file2 = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'all_data_series2.txt')
if not (os.path.isfile(json_series_file2)):
	f = open(json_series_file2, 'w') 
	my_json_string=('[{"lastupdate": {"1": "2017-07-26 15:26:57"}, "tmdb": "", "title": "\u05e7\u05d0\u05e1\u05dc\u05d1\u05e0\u05d9\u05d4", "tvdb": "", "season": {"1": "2"}, "trakt": "", "imdb": "tt6517102", "year": "1982"}, {"lastupdate": {"1": "2017-07-26 15:26:57"}]')
	f.write(json.dumps(my_json_string)) 
	f.close()

json_movie_file = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])),'all_data.json')
if not (os.path.isfile(json_movie_file)):
	f = open(json_movie_file, 'w') 
	my_json_string=({'movies':{} })
	f.write(json.dumps(my_json_string)) 
	f.close()
def update_tv(url,page_num):
  from bs4  import BeautifulSoup
  from urlparse import urlparse
  
  
  res = requests.get(url)
 
  file = open(json_series_file, 'r') 
 
  

  db=json.loads(file.read())


  links_direct=[]
  res.raise_for_status()
  recipeSoup = BeautifulSoup(res.text, "html.parser")
  type(recipeSoup)
  all_data = recipeSoup.findAll("div", {'id':['series_list']})
  
  for li2 in all_data:
    x=20*(page_num-1)
    links = li2.findAll("div", {'class':['subtitle']})
    for link in links: 
        x=x+1
        bar_length=200
        percent = float(x) / 200
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))
        
        b=link.find('a') 
        c=b.get('href')

        res2 = requests.get(c)
        res2.encoding = 'utf-8'
        res2.raise_for_status()
    
       
      
        recipeSoup2 = BeautifulSoup(res2.text, "html.parser")

        type(recipeSoup2)
        prejson='{'+re.compile("var data_info = {(.+?) }").findall(recipeSoup2.text)[0]+'}'
        prejson=prejson.replace("'",'"')
   
        json_data=json.loads(prejson)
 
        all_data2 = recipeSoup2.findAll("div", {'class':['pageLeftPart']})
        names=recipeSoup2.findAll('h3')
        year=recipeSoup2.find("h3")

        years=  re.compile(r'\((.*?)\)', re.DOTALL |  re.IGNORECASE).findall(str(year))
       
        year="0"
        for ye in years:
          if len(ye)>2:
            year=ye

        
        link = recipeSoup2.find(itemprop="image")
        if "lsrc" in link:
          thumb=(link["lsrc"])
        else:
          thumb=(link["src"])
        
    
        
        genres=recipeSoup2.find(itemprop="genre")
        for g in genres:
          genre=(g.strip(' \t\n\r'))

        for list in all_data2:
          e=list.find('a')
          
          
          if e!=None:
           f=e.get('href')
           g=f.split('/')
           if len(g[len(g)-1])==0:
            imdb_id=(g[len(g)-2])
           else:
            imdb_id=(g[len(g)-1])
           index=  find(db,"imdb",imdb_id)
    
           sys.stdout.write("\rPercent: [{0}] {1}% ".format('Page '+ str(page_num) +'/'+ "10" , int(round(percent * 100)),'Series DB records number:'+str(len (db)) + '          '))
           sys.stdout.flush()
           if index==-1:
             tvdb_id=(tvdb_imdb(imdb_id))
             tmdb_id=(imdb_id_to_tmdb(imdb_id))
           else:
             tvdb_id=''
             tmdb_id=''
           #print(int(x/float(20)*100),'עמוד'+str(page_num), replaceHTMLCodes(json_data['title']))
           
           
            
           add_tv(imdb_id,tmdb_id,  db,str(json_data['season_id']),str(json_data['episode_id']),replaceHTMLCodes(json_data['title']),year,genre,thumb,tvdb_id)
           #my_json_string.append({'imdb': imdb_id, 'trakt': tmdb_id,'year':year.text,'title':names[0].text})


    return db

def add_tv(imdb_id,tmdb,db,season,episode,title,year,genre,thumb,tvdb):
        from datetime import datetime

        now = datetime.now()
        trakt=''
        today=time.mktime(now.timetuple())

            
        video_info = {"imdb"        : imdb_id,
                  "tvdb"         : tvdb,
                  "tmdb"         : tmdb,
                  "trakt"        : trakt,

                  "year"         : year,

                  "title"        : title,
                  "season"       : {season:episode},
                  "lastupdate"   : {"1":today}}
            #video_info = dict((k, v) for (k, v) in video_info.iteritems() if v)

   

        
        index=  find(db,"imdb",imdb_id)
        
        string_long=''
        if index!=-1:
         
         if season in db[index]['season']:
          if db[index]['season'][season]<episode:
           print '\r Updating: '  +str(imdb_id) + ' At:'+str(index)
           db[index]['season'][season]=episode
         else:
           db[index]['season'][season]=episode
         big=0
         for key in db[index]['lastupdate']:
           if int(key)>big:
             big=int(key)
         db[index]['lastupdate'][big+1]=today

        else:
         print '\r Adding: ' + str(imdb_id )+ ','+str(tvdb)+','+str(tmdb)+ ' At:'+str(len(db))
         db.append(video_info)
          
def add_movie(imdb_id,tmdb,db,title,year,tvdb):
        from datetime import datetime

        now = datetime.now()
        trakt=''
        today=time.mktime(now.timetuple())

            
        video_info = {"imdb"        : imdb_id,
                  "tvdb"         : tvdb,
                  "tmdb"         : tmdb,
                  "trakt"        : trakt,

                  "year"         : year,

                  "title"        : title,
                  
                  "date"         : today}
            #video_info = dict((k, v) for (k, v) in video_info.iteritems() if v)

   

        
        index=  find(db,"imdb",imdb_id)
    
       
        if index==-1:
         db.append(video_info)
        
def imdb_id_to_tmdb(imdb_movie_id):
    params = {"external_source": "imdb_id"}
    response = _tmdb_send_request("find/%s" % imdb_movie_id,
                                  get=params)
    
    if isinstance(response, int):
        #print 'response:'+response
        if response == 401:
            print("TMDB Error: Not authorized.")
        elif response == 404:
            print("TMDB Error: IMDB id '%s' not found." % imdb_movie_id)
        else:
            print("TMDB Error: Unknown error.")
        return None

    elif not response:
        print("TMDB Error: Could not translate IMDB id to TMDB id")
        return None

    if len(response['movie_results']):
        return response['movie_results'][0]['id']
    elif  len(response['tv_results']):
        return response['tv_results'][0]['id']
    else:
       return None
def _tmdb_send_request(method, get={}, post=None):
    get['api_key'] = TMDB_API_KEY
    get = dict((k, v) for (k, v) in get.iteritems() if v)
    get = dict((k, unicode(v).encode('utf-8')) for (k, v) in get.iteritems())
    url = "%s%s?%s" % (TMDB_API_URL, method, urllib.urlencode(get))
    request = urllib2.Request(url=url,
                              data=post,
                              headers={'Accept': 'application/json',
                                       'Content-Type': 'application/json',
                                       'User-agent': __USERAGENT__})
    #try:
    response = urllib2.urlopen(request, timeout=50).read()

    #except urllib2.HTTPError as err:
    #    return err.code

    return json.loads(response)
def find(lst, key, value):
    for i, dic in enumerate(lst):
        if dic[key] == value:
            return i
    return -1
    
def first_substring(strings, substring):
    return min(i for i, string in enumerate(strings) if substring in string)
    
def tvdb_imdb(imdb):
   
   url = 'http://thetvdb.com/api/GetSeriesByRemoteID.php?imdbid=%s' % imdb

   result = request(url, timeout='50')
   
    
   try:
     tvdb=parseDOM(result, 'seriesid')[0]
   except:
    return ''
   return tvdb
def parseDOM(html, name=u"", attrs={}, ret=False):
    # Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen

    if isinstance(html, str):
        try:
            html = [html.decode("utf-8")] # Replace with chardet thingy
        except:
            html = [html]
    elif isinstance(html, unicode):
        html = [html]
    elif not isinstance(html, list):
        return u""

    if not name.strip():
        return u""

    ret_lst = []
    for item in html:
        temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
        for match in temp_item:
            item = item.replace(match, match.replace("\n", " "))

        lst = []
        for key in attrs:
            lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
            if len(lst2) == 0 and attrs[key].find(" ") == -1:  # Try matching without quotation marks
                lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

            if len(lst) == 0:
                lst = lst2
                lst2 = []
            else:
                test = range(len(lst))
                test.reverse()
                for i in test:  # Delete anything missing from the next list.
                    if not lst[i] in lst2:
                        del(lst[i])

        if len(lst) == 0 and attrs == {}:
            lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
            if len(lst) == 0:
                lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

        if isinstance(ret, str):
            lst2 = []
            for match in lst:
                attr_lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
                if len(attr_lst) == 0:
                    attr_lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
                for tmp in attr_lst:
                    cont_char = tmp[0]
                    if cont_char in "'\"":
                        # Limit down to next variable.
                        if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
                            tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

                        # Limit to the last quotation mark
                        if tmp.rfind(cont_char, 1) > -1:
                            tmp = tmp[1:tmp.rfind(cont_char)]
                    else:
                        if tmp.find(" ") > 0:
                            tmp = tmp[:tmp.find(" ")]
                        elif tmp.find("/") > 0:
                            tmp = tmp[:tmp.find("/")]
                        elif tmp.find(">") > 0:
                            tmp = tmp[:tmp.find(">")]

                    lst2.append(tmp.strip())
            lst = lst2
        else:
            lst2 = []
            for match in lst:
                endstr = u"</" + name

                start = item.find(match)
                end = item.find(endstr, start)
                pos = item.find("<" + name, start + 1 )

                while pos < end and pos != -1:
                    tend = item.find(endstr, end + len(endstr))
                    if tend != -1:
                        end = tend
                    pos = item.find("<" + name, pos + 1)

                if start == -1 and end == -1:
                    temp = u""
                elif start > -1 and end > -1:
                    temp = item[start + len(match):end]
                elif end > -1:
                    temp = item[:end]
                elif start > -1:
                    temp = item[start + len(match):]

                if ret:
                    endstr = item[end:item.find(">", item.find(endstr)) + 1]
                    temp = match + temp + endstr

                item = item[item.find(temp, item.find(match)) + len(temp):]
                lst2.append(temp)
            lst = lst2
        ret_lst += lst

    return ret_lst
def request(url, close=True, redirect=True, error=False, proxy=None, post=None, headers=None, mobile=False, limit=None, referer=None, cookie=None, output='', timeout='30'):
    #try:
        #control.log('@@@@@@@@@@@@@@ - URL:%s' % url)
        handlers = []

        if not proxy == None:
            handlers += [urllib2.ProxyHandler({'http':'%s' % (proxy)}), urllib2.HTTPHandler]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)

        if output == 'cookie2' or output == 'cookie' or output == 'extended' or not close == True:
            cookies = cookielib.LWPCookieJar()
            handlers += [urllib2.HTTPHandler(), urllib2.HTTPSHandler(), urllib2.HTTPCookieProcessor(cookies)]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)

        try:
            if sys.version_info < (2, 7, 9): raise Exception()
            import ssl; ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            handlers += [urllib2.HTTPSHandler(context=ssl_context)]
            opener = urllib2.build_opener(*handlers)
            opener = urllib2.install_opener(opener)
        except:
            pass

        try: headers.update(headers)
        except: headers = {}
        if 'User-Agent' in headers:
            pass
        elif not mobile == True:
            #headers['User-Agent'] = agent()
            headers['User-Agent'] =randomagent()
        else:
            headers['User-Agent'] = 'Apple-iPhone/701.341'
        if 'Referer' in headers:
            pass
        elif referer == None:
            headers['Referer'] = '%s://%s/' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)
        else:
            headers['Referer'] = referer
        if not 'Accept-Language' in headers:
            headers['Accept-Language'] = 'en-US'
        if 'Cookie' in headers:
            pass
        elif not cookie == None:
            headers['Cookie'] = cookie

        if redirect == False:
            class NoRedirection(urllib2.HTTPErrorProcessor):
                def http_response(self, request, response): return response

            opener = urllib2.build_opener(NoRedirection)
            opener = urllib2.install_opener(opener)

            try: del headers['Referer']
            except: pass

        request = urllib2.Request(url, data=post, headers=headers)

        try:
            response = urllib2.urlopen(request, timeout=int(timeout))
        except urllib2.HTTPError as response:
            log("AAAA- CODE %s|%s " % (url, response.code))
            if response.code == 503:
                if 'cf-browser-verification' in response.read(5242880):
                    control.log("CF-OK")

                    netloc = '%s://%s' % (urlparse.urlparse(url).scheme, urlparse.urlparse(url).netloc)
                    cf = cache.get(cfcookie, 168, netloc, headers['User-Agent'], timeout)
                    headers['Cookie'] = cf
                    request = urllib2.Request(url, data=post, headers=headers)
                    response = urllib2.urlopen(request, timeout=int(timeout))
                elif error == False:
                    return

            elif response.code == 307:
                control.log("AAAA- Response read: %s" % response.read(5242880))
                control.log("AAAA- Location: %s" % (response.headers['Location'].rstrip()))
                cookie = ''
                try: cookie = '; '.join(['%s=%s' % (i.name, i.value) for i in cookies])
                except: pass
                headers['Cookie'] = cookie
                request = urllib2.Request(response.headers['Location'], data=post, headers=headers)
                response = urllib2.urlopen(request, timeout=int(timeout))
                #control.log("AAAA- BBBBBBB %s" %  response.code)

            elif error == False:
                print ("Response code",response.code, response.msg,url)
                return

        if output == 'cookie':
            try: result = '; '.join(['%s=%s' % (i.name, i.value) for i in cookies])
            except: pass
            try: result = cf
            except: pass

        elif output == 'response':
            if limit == '0':
                result = (str(response.code), response.read(224 * 1024))
            elif not limit == None:
                result = (str(response.code), response.read(int(limit) * 1024))
            else:
                result = (str(response.code), response.read(5242880))

        elif output == 'chunk':
            try: content = int(response.headers['Content-Length'])
            except: content = (2049 * 1024)
            if content < (2048 * 1024): return
            result = response.read(16 * 1024)

        elif output == 'extended':
            try: cookie = '; '.join(['%s=%s' % (i.name, i.value) for i in cookies])
            except: pass
            try: cookie = cf
            except: pass
            content = response.headers
            result = response.read(5242880)
            return (result, headers, content, cookie)

        elif output == 'geturl':
            result = response.geturl()

        elif output == 'headers':
            content = response.headers
            return content

        else:
            if limit == '0':
                result = response.read(224 * 1024)
            elif not limit == None:
                result = response.read(int(limit) * 1024)
            else:
                result = response.read(5242880)

        if close == True:
            response.close()

        return result
def randomagent():
    BR_VERS = [
        ['%s.0' % i for i in xrange(18, 43)],
        ['37.0.2062.103', '37.0.2062.120', '37.0.2062.124', '38.0.2125.101', '38.0.2125.104', '38.0.2125.111', '39.0.2171.71', '39.0.2171.95', '39.0.2171.99', '40.0.2214.93', '40.0.2214.111',
         '40.0.2214.115', '42.0.2311.90', '42.0.2311.135', '42.0.2311.152', '43.0.2357.81', '43.0.2357.124', '44.0.2403.155', '44.0.2403.157', '45.0.2454.101', '45.0.2454.85', '46.0.2490.71',
         '46.0.2490.80', '46.0.2490.86', '47.0.2526.73', '47.0.2526.80'],
        ['11.0']]
    WIN_VERS = ['Windows NT 10.0', 'Windows NT 7.0', 'Windows NT 6.3', 'Windows NT 6.2', 'Windows NT 6.1', 'Windows NT 6.0', 'Windows NT 5.1', 'Windows NT 5.0']
    FEATURES = ['; WOW64', '; Win64; IA64', '; Win64; x64', '']
    RAND_UAS = ['Mozilla/5.0 ({win_ver}{feature}; rv:{br_ver}) Gecko/20100101 Firefox/{br_ver}',
                'Mozilla/5.0 ({win_ver}{feature}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{br_ver} Safari/537.36',
                'Mozilla/5.0 ({win_ver}{feature}; Trident/7.0; rv:{br_ver}) like Gecko']
    index = random.randrange(len(RAND_UAS))
    return RAND_UAS[index].format(win_ver=random.choice(WIN_VERS), feature=random.choice(FEATURES), br_ver=random.choice(BR_VERS[index]))
def log(message):

        print(message)
def update_page_data(url,page_num):
  from bs4 import BeautifulSoup
  from urlparse import urlparse

  
  res = requests.get(url)
  file = open(json_movie_file, 'r') 
 
  
  
  db=json.loads(file.read())

  links_direct=[]
  res.raise_for_status()
  recipeSoup = BeautifulSoup(res.text, "html.parser")
  type(recipeSoup)
  all_data = recipeSoup.findAll("div", {'id':['movie_list']})
  
  for li2 in all_data:
    x=20*(page_num-1)
    links = li2.findAll("div", {'class':['subtitle']})
    for link in links: 
        x=x+1
        bar_length=200
        percent = float(x) / 200
        hashes = '#' * int(round(percent * bar_length))
        spaces = ' ' * (bar_length - len(hashes))
        

        b=link.find('a') 
        c=b.get('href')

        res2 = requests.get(c)
        res2.raise_for_status()
        recipeSoup2 = BeautifulSoup(res2.text, "html.parser")
        type(recipeSoup2)
        all_data2 = recipeSoup2.findAll("div", {'class':['pageLeftPart']})
        names=recipeSoup2.findAll('h3')
        year=recipeSoup2.findAll("strong")[0].text
        sys.stdout.write("\rPercent: [{0}] {1}% {2}".format('Page '+ str(page_num) +'/'+ "10" , int(round(percent * 100)),'Movies DB records number:'+str(len (db)) + '          '))
        sys.stdout.flush()
        for list in all_data2:
          e=list.find('a')
          #f=e.get('href')
          
          if e!=None:
           f=e.get('href')
           g=f.split('/')
           if len(g[len(g)-1])==0:
            imdb_id=(g[len(g)-2])
           else:
            imdb_id=(g[len(g)-1])
           index=  find(db,"imdb",imdb_id)
    
           
           if index==-1:
             tvdb_id=(tvdb_imdb(imdb_id))
             tmdb_id=(imdb_id_to_tmdb(imdb_id))

             print '\r Adding:'+imdb_id + ','+str(tmdb_id)+','+str(tvdb_id)+' At:' + str(len (db))
             add_movie(imdb_id,tmdb_id,db,names[0].text,year,tvdb_id)
           #my_json_string.append({'imdb': imdb_id, 'trakt': tmdb_id,'year':year.text,'title':names[0].text})

    
    return db
def replaceHTMLCodes(txt):
    txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
    txt = HTMLParser.HTMLParser().unescape(txt)
    txt = txt.replace("&quot;", "\"")
    txt = txt.replace("&amp;", "&")
    return txt
def update_series():

    all_json_string=[]
    for i in range(1,11):
      
      url='http://www.subscenter.info/he/view/'+str(i)

      all_json_string=(update_tv(url,i))

      
    
      file = open(json_series_file,'w') 
 
      file.write(json.dumps(all_json_string)) 
      file.close()

def update_movies():
    all_json_string=[]
    for i in range(1,11):
      
      url='http://www.subscenter.info/he/view/'+str(i)
     
      all_json_string=(update_page_data(url,i))
      

	  
      file = open(json_movie_file,'w') 
 
      file.write(json.dumps(all_json_string)) 
  
 
      file.close()
try: 
  from bs4  import BeautifulSoup
except:
  pip.main(['install', 'BeautifulSoup'])
try:
  import requests
except:
  pip.main(['install', 'requests'])


print "Updating Movies"
update_movies()

print "All Done"