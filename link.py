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
