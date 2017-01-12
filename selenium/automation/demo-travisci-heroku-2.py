#!/usr/bin/env python2.7

#--------------------------------------------------------------------
# 
# Title: demo-travisci-heroku-2.py
#
#--------------------------------------------------------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from datetime import datetime, timedelta
from optparse import OptionParser
import time, unittest, os, json

from autotools import demo_api as api
from autotools import HTMLTestRunner

with open("data/login.json") as data_file:
    server = json.load(data_file)

with open("data/input.json") as data_file:
    data = json.load(data_file)

testname = "TravisciHerokuWebAutomation-Demo2"
chromedriver = "../chromedriver"
current_date = datetime.now()

profile = None
# option in command line
parser = OptionParser()
parser.add_option("-d", "--driver", action="store", dest="drivername")
parser.add_option("-u", "--url", action="store", dest="urlname")
(options, args) = parser.parse_args()
# parsing the URL option
if options.urlname:
    urladdress = options.urlname

    # if another URL used, then set the Firefox preference
    profile = webdriver.FirefoxProfile()
    profile.set_preference("xpinstall.signatures.required", False)
else: urladdress = server["domain"]

# parsing the web browser testing option and checking system os
if options.drivername == "chrome": WebDriver = webdriver.Chrome(chromedriver)
else: WebDriver = webdriver.Firefox(firefox_profile=profile)
#else: WebDriver = webdriver.Firefox()

class TravisciHerokuWebAutomation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        global WebDriver
        cls.driver = WebDriver

    def setUp(self):
        print "setUp"

    def test_001_get_domain(self):
        try:
            self.driver.get(urladdress)
            self.driver.maximize_window()
            time.sleep(3)
        except Exception as e:
            print e
            raise Exception("Cannot open URL: ", e)

    def tearDown(self):
        print "tearDown"

    @classmethod
    def tearDownClass(cls):
        print "test done"
        cls.driver.close()
        cls.driver.quit()


if __name__ == '__main__':
    # output to a file
    if not os.path.exists('reports'): os.mkdir('reports')
    suite = unittest.TestLoader().loadTestsFromTestCase(TravisciHerokuWebAutomation)

    test_report = 'reports/' + testname + '.html'
    fp = file(test_report, 'wb')
    runner = HTMLTestRunner.HTMLTestRunner(
                stream=fp,
                title=testname,
                description='This demonstrates the report output by HTMLTestRunner.'
                )

    # run the test
    runner.run(suite)

    # output result on console for debugging
    #unittest.TextTestRunner(verbosity=2).run(suite)
    
    # close output file
    fp.close()


