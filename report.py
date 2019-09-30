# -*- coding: utf-8 -*-

from selenium import webdriver
import sys, json, time, traceback

reload(sys)
sys.setdefaultencoding('utf-8')

iedriver = "bin\IEDriverServer_Win32_3.9.0.exe"
browser = None

def home():
    global browser
    browser = webdriver.Ie(iedriver)
    browser.get("http://localhost:8080/report.htm")
    browser.maximize_window()


def dismiss_welcome_popup():
    try:
        popupbox = browser.find_element_by_id('popupbox')
        browser.find_element_by_css_selector('div#popupbox input.pop_button').click()
    except:
        print('popupbox not exists!')


def query_personal_credit_report():
    content = browser.find_elements_by_xpath('//body/div/div/table/tbody/tr[2]/td')[0]

    meta = content.find_elements_by_xpath('./table[1]/tbody/tr[2]/td')
    meta_list = []
    for m in meta:
        ms = m.text.strip().split('：')
        meta_list.append([ms[0].strip(), ms[1].strip()])
    print json.dumps(meta_list, encoding = 'utf-8', ensure_ascii=False)

    person = content.find_elements_by_xpath('./table[2]/tbody/tr[1]/td')
    person_list = []
    for p in person:
        ps = p.text.strip().split('：')
        if len(ps) is 2:
            person_list.append([ps[0].strip(), ps[1].strip()])
        else:
            person_list.append([ps[0].strip()])
    print json.dumps(person_list, encoding = 'utf-8', ensure_ascii=False)

    credit_loan = content.find_elements_by_xpath('./table[4]/tbody/tr[3]/td/table/tbody/tr/td/table/tbody/tr')
    credit_loan_list = []
    for c in credit_loan:
        cl = c.find_elements_by_tag_name('td')
        credit_loan_element = []
        credit_loan_list.append(credit_loan_element)
        for cls in cl:
            credit_loan_element.append(cls.text.strip())
    print json.dumps(credit_loan_list, encoding = 'utf-8', ensure_ascii=False)

    credit_details = content.find_elements_by_xpath('./ol[1]/li')
    cds = []
    for cd in credit_details:
        cds.append(cd.text.strip())
    print json.dumps(cds, encoding = 'utf-8', ensure_ascii=False)
    

    inquiry_history = content.find_elements_by_xpath('./table[7]/tbody/tr[position()>2 and position()<last()]')
    ih_list = []
    for i in inquiry_history:
        ih = i.find_elements_by_tag_name('td')
        ih_element = []
        ih_list.append(ih_element)
        for ihs in ih:
            ih_element.append(ihs.text.strip())
    print json.dumps(ih_list, encoding = 'utf-8', ensure_ascii=False)
    

def query_report():
    try:
        home()
        #dismiss_welcome_popup()
        query_personal_credit_report()
    except Exception as e:
        traceback.print_exc(file=sys.stderr)

    browser.quit()
    return


if __name__ == '__main__':
    query_report()

#End
