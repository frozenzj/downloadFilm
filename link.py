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

def ts_dl(url,num=1):
    import requests
    from lxml import etree
    from urllib import parse as pa
    import re
    import os
#    url='https://www.yunbtv.com/play/38577-1-38.html'
    #1,requests find m3u8 requests link
    d1={}
    tsl=[]
    tsn=[]
    rule_u=r'%u([0-9A-Fa-f]{4})'
    rule_c=r'(m3u8#.{1}|iqiyi#.{1})(\d{2}).{1}'
    r1=requests.get(url)
    e1=etree.HTML(r1.content)
    x1=e1.xpath('//div/script/text()')
    str1=x1[1][28:-2]
    str1=pa.unquote(str1)
    str2=re.sub(rule_u,lambda m:chr(int(m.group(1),base=16)),str1)
    str3=re.sub(rule_c,lambda m:m.group(2),str2)
    l1=str3.split('$')
#    print(l1)
    for i in range(len(l1)):
        if l1[i]=='云播在线':
            l2=l1[i+3:-1]
            l2.insert(0,'01')
    for i in range(0,len(l2),2):
        d1[l2[i]]=l2[i+1]
#    return d1
    #2,requests m3u8 link
    mlink=d1[str(num).zfill(2)]
    r2=requests.get(mlink)
#    return mlink,r2.text
    #3,find #EXT-X-STREAM-INF,get real m3u8 link
    mlink=mlink.rsplit('/',1)[0]
    mlist1=r2.text
    if '#EXTM3U' not in mlist1:
        raise BaseException('not m3u8 link!!!')
    if '#EXT-X-STREAM-INF' in mlist1:
        mlist1=mlist1.splitlines()
        for i in mlist1:
            if '.m3u8' in i:
                mlink_f=mlink+'/'+i
#                print(mlink_f)
                r3=requests.get(mlink_f)
                mlink_sp=mlink_f.rsplit('/',1)[0]
                ts_text=r3.text
    if '#EXTINF' in mlist1:
        ts_text=mlist1

    #4,requests real m3u8 link,download ts file(check if key exist)
#    return ts_text
    ts_text_s=ts_text.splitlines()
    for i in ts_text_s:
        if '.ts' in i:
            tsl.append(mlink_sp+'/'+i)
            tsn.append(i)
#    return tsl
#    for i in range(len(tsl)):
    for i in range(10):
        tempr=requests.get(tsl[i])
        with open(os.path.join('C:/Users/CFSS-FS/tsfile',tsn[i]),'ab') as f:
            f.write(tempr.content)
            f.flush()
    #5,merge all ts file into a MP4 file
    cmd='copy /b * new.tmp'
    os.chdir('C:/Users/CFSS-FS/tsfile')
    os.system(cmd)
    os.rename('new.tmp','第%s集.mp4'%(str(num)))
