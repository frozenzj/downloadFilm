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
