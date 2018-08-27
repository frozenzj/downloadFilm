def se_dl_link(url):
    from selenium import webdriver as wd
    from selenium.webdriver.firefox.options import Options
    import re
    rule=r'.*id=(.*)'
    fop=Options()
    fop.add_argument('-headless')
    browser=wd.Firefox(firefox_options=fop)
    browser.get(url)
    iframeb=browser.find_element_by_tag_name('iframe')
    browser.switch_to_frame(iframeb)
    x=browser.find_element_by_xpath('//iframe')
    x=x.get_attribute('src')
    r=re.match(rule,x)
    result=r.group(1)
    return result
def re_dl_link(url):
    import requests
    from lxml import etree
    import re
    rules=r'.*id=(.*)'
    r0=requests.get(url)
    if r0.status_code==200:
        etreec=etree.HTML(r0.content)
        xpathr=etreec.xpath('//iframe/@src')
        name=etreec.xpath('//h3/text()')
        i=name[0][5:]
        r1=requests.get(xpathr[0])
        print('step 1 status_code:%s'%(r1))
    else:
        print('step 1 failed!')
    if r1.status_code==200:
        etreef=etree.HTML(r1.content)
        xpathf=etreef.xpath('//iframe/@src')
        dl_prelink=xpathf[0]
        print('step 2 link:%s'%(dl_prelink))
    else:
        print('step 2 failed!')
    g=re.match(rules,dl_prelink)
    dl_link=g.group(1)
    print('dl_link:%s'%(dl_link))
    dl=requests.get(dl_link)
    try:
        with open('C:\\yxgl\\%s.mp4'%(i),'wb') as f:
            f.write(dl.content)
        print('%s is downloaded,thx for using!'%(i))
    except:
        print('step 3 failed!')

def ts_dl(url):
    import requests
    from urllib import parse as pa
    import re
    from lxml import etree
    #1,requests find m3u8 requests link
    rule_u=r'%u([0-9A-Fa-f]{4})'
    rule_c=r'm3u8#.?(\d{2}).?'
    d={}
    #1,requests m3u8 link
    r1=requests.get(url)
    e1=etree.HTML(r1.content)
    x1=e1.xpath('//div/script/text()')
    str1=x1[1][28:-2]
    str1=pa.unquote(str1)
    str2=re.sub(rule_u,lambda m:chr(int(m.group(1),base=16)),str1)
    #test output m3u8 list
    #return str2
    str3=re.sub(rule_c,lambda m:m.group(1),str2)
    l1=str3.split('$')
    for i in range(len(l1)):
        if l1[i]=='云播在线':
            l2=l1[i+3:-1]
            l2.insert(0,'01')
    for i in range(0,len(l2),2):
        d[l2[i]]=l2[i+1]
    #return(d)
    #2,requests m3u8 link
    r2=requests.get(d1[str(num).zfill(2)])
    print(r2.content)
    #3,find #EXT-X-STREAM-INF,get real m3u8 link
    #4,requests real m3u8 link,download ts file(check if key exist)
    #5,merge all ts file into a MP4 file
