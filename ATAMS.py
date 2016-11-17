from ConfigParser import SafeConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
import time

# config
# I set a direct path variable for chromedriver for Windows. For Mac, I install chromedriver to usr/bin (no need for this path variable)
# path = xxx/chromedriver
config = SafeConfigParser()
config.read('info.ini')
classname = eval(config.get("info", 'CLASSNAME'), {}, {})
username = config.get('info', 'USERNAME')
password = config.get('info', 'PASSWORD')
email_user = config.get('info', 'EMAIL_USER')
email_pass = config.get('info', 'EMAIL_PASS')
path = config.get('info', 'PATH')
url = config.get('info', 'URL')
br = webdriver.Chrome()     # for Mac
br = webdriver.Chrome(executable_path = path) # for Windows
removelist=[]

# email
def send_msg(username, password, subj, msg):
    s = smtplib.SMTP('smtp.gmail.com:587')
    s.starttls()
    s.ehlo
    s.login(username, password)
    headers = ["From: " + username, "Subject: " + subj, "To: " + username]
    headers = "\r\n".join(headers)
    s.sendmail(username, username, headers + "\r\n\r\n" + msg)
    print 'Email sent!\n'
    s.quit()

# remove
def remove(removelist, classname):
    # write back
    for x in removelist:
        classname.remove(x)
    config.set('info', 'CLASSNAME', '[' + ', '.join('"' + item + '"' for item in classname) + ']')
    with open('info.ini', 'w') as configfile: config.write(configfile)
    classname = eval(config.get("info", 'CLASSNAME'), {}, {})

# initializing
print 'Getting URL'
br.get(url)
print 'Sending username and password'
br.find_element_by_id('username').send_keys(username)
br.find_element_by_id('password').send_keys(password)
print 'Logging in'
br.find_element_by_xpath("//*[@id='loginCol1']/div[3]/button").click()
print 'Navigating to "My Record"'
br.find_element_by_xpath("//*[contains(text(), 'My Record')]").click()
print 'Navigating to "Search Class Schedule"\n'
br.find_element_by_xpath("//*[@id='portletContent_u42l1n120']/div/ul/li[2]/a[1]").click()

# start
def check(classname):
    for i in xrange(0, len(classname)):
        br.switch_to.default_content()
        print 'Submitting'
        br.switch_to.frame('Pluto_92_ctf3_2929_tw_frame')
        #br.switch_to.frame(1)   # need switch to access form
        time.sleep(1)
        br.find_element_by_xpath("//div[3]/form/input[2]").click()

        coursename = classname[i].split('-')[0]
        coursesection = classname[i].split('-')[1]
        coursenumber = classname[i].split('-')[2]
        name = coursename+"-"+coursesection+"-"+coursenumber
        print 'Now searching for ' + name

        print 'Searching classname: ' + coursename
        time.sleep(1)
        br.find_element_by_xpath("//*[@id='subj_id']/option[@value='%s']" %coursename).click()

        print 'Submitting'
        time.sleep(1)
        br.find_element_by_xpath("//*[@id='courseBtnDiv']/input[2]").click()

        print 'Searching course number: ' + coursesection
        for i in range(2, len(br.find_elements_by_xpath("//tr"))):		# iterate through rows tr[i]
            if br.find_element_by_xpath("//tr["+str(i)+"]/td[2]").text == coursesection:  # td[2] refers to course number
                print 'Viewing sections'
                time.sleep(1)
                br.find_element_by_xpath("//tr["+str(i)+"]//input[30]").click() # input[30] refers to button
                break

        # td[2] = CRN, td[5] = section number, td[13] = remainder
        print 'Searching section number: ' + coursenumber
        for j in range(3, len(br.find_elements_by_xpath("//tr"))-3, 1):		# iterate through rows tr[j], starts at 3 and inc by 2
            if br.find_element_by_xpath("//tr["+str(j)+"]/td[5]").text == coursenumber:	# if row j matches with section number at td[5]
                if int(br.find_element_by_xpath("//tr["+str(j)+"]/td[13]").text) > 0:   # check if row j has spots > 0 located at td[13]
                    spots = br.find_element_by_xpath("//tr["+str(j)+"]/td[13]").text
                    crn = br.find_element_by_xpath("//tr["+str(j)+"]/td[2]").text   # get CRN at td[2]
                    print 'Sending email'
                    send_msg(email_user, email_pass, 'Class found for ' + name, 'Spot(s) left: ' + spots + '\nCRN: ' + crn)
                    removelist.append(name)
                    br.back()
                    br.back()
                    br.back()
                    signup(crn)
                    time.sleep(1)
                    break
                else:
                    print 'No spots available for section: ' + coursenumber + '. Searching for next class.\n'
                    br.back()
                    br.back()
                    br.back()
                    time.sleep(1)
                    break

# auto signup!
def signup(crn):
    br.back()
    br.find_element_by_xpath("//*[@id='customBulletedList']/li[2]/a").click()
    br.switch_to.default_content()
    br.switch_to.frame(1)
    br.find_element_by_xpath("/html/body/div[3]/form/input").click()
    br.find_element_by_id('crn_id1').send_keys(crn)
    br.find_element_by_id('crn_id1').send_keys(Keys.RETURN)
    # brings us back to My Record page
    br.back()
    br.back()
    br.back()
    print 'Navigating to "Search Class Schedule"\n'
    br.find_element_by_xpath("//li[1]/*[contains(text(), 'Search Class Schedule')]").click()

# LOOPER
while True:
    check(classname)
    remove(removelist, classname)
    removelist=[]                   # reset remove list
    print '\n***RESTARTING***\n\n'
    time.sleep(5)
