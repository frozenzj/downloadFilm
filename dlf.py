#import selenium
#from selenium import webdriver as wd
#import selenium.webdriver.common.keys as Keyss
#from selenium.webdriver.firefox.options import Options
#fop=Options()
#fop.add_argument('-headless')
#browser=wd.Firefox()
##browser=wd.Firefox(firefox_options=fop)
#browser.get('http://www.15yc.com')
#Input=browser.find_element_by_name('wd')
#Input.send_keys('死侍')
#Input.send_keys(Keyss.Keys.ENTER)
#browser.switch_to_window(browser.window_handles[1])
#browser.implicitly_wait()
#Ele1=browser.find_element_by_class_name('movie-item')
#Ele1.click()
#browser.switch_to_window(browser.window_handles[2])
#Ele2=browser.find_element_by_class_name('dslist-group-item')
#Ele2.click()
#browser.switch_to_window(browser.window_handles[3])
#Ele3=browser.find_element_by_class_name('dplayer-video dplayer-video-current')
#header={'Host':'www.juduoba.com','User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8','Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2','Accept-Encoding': 'gzip, deflate','Cookie': 'UM_distinctid=165124d21a242b-0aab4e71efaf43-4c312b7b-100200-165124d21a4fc; CNZZDATA1260308835=1116222658-1533606379-%7C1533789987; bdshare_firstime=1533785210103','Connection':'keep-alive'}
#========================================================
#========================================================
def crawfilm_htm(mode,step_start=None,step_end=None):
    import requests
    heads={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    if mode=='test':
        h='http://www.juduoba.com/show/1.html'
        r=requests.get(h,headers=heads)
        l=crawfilm_list(r.content)
        return l
    elif mode=='range':
        i=0
        final_l=[]
        for i in range(step_start,step_end):
            h='http://www.juduoba.com/show/%s.html'%(str(i))
            r=requests.get(h,headers=heads,allow_redirects=False)
            if r.status_code==301:
                break
            else:
                r.encoding='utf-8'
                l=crawfilm_list(r.content)
                l.insert(0,i)
#                print(i)
                final_l.append(l)
        return final_l

def crawfilm_list(responseC):
    from lxml import etree
    r=responseC.decode('utf-8','ignore')
    e1=etree.HTML(r)
    i=0
    media_detail=[]
    l=e1.xpath('//h1[@class="movie-title"]/span/text()')
    l.append(e1.xpath('string(//ol[@class="breadcrumb"]/li[2]/a)'))
    l.append(e1.xpath('//h1[@class="movie-title"]/text()')[0])
    for i in range(1,8):
        media_detail.append(e1.xpath('string(//tbody/tr[%s]/td[2])'%(str(i))))
    l.extend(media_detail)
    return l
#    media_type=e1.xpath('//ol[@class="breadcrumb"]/li[2]/a/text()')     #media_type
#    media_name=e1.xpath('//h1[@class="movie-title"]/text()')            #media_name
#    media_year=e1.xpath('//h1[@class="movie-title"]/span/text()')       #media_year
#    media_dtitle=e1.xpath('//tbody/tr/td/span/text()')
#    media_detail=e1.xpath('//tbody/tr/td/text()')
#    media_detail[6]=media_detail[6]+e1.xpath('//tbody/tr/td/a/text()')[0]
