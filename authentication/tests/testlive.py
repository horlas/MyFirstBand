from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait
import time

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver()
        cls.selenium.maximize_window()
        cls.selenium.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login_logout(self):

        timeout = 2
        # self.selenium.get('%s%s' % (self.live_server_url, '/authentication/accounts/login/'))
        # we are on the index page , user is not connected
        self.selenium.get(self.live_server_url)
        time.sleep(2)
        # user wants to connect
        self.selenium.find_element_by_xpath('//a[@href="/authentication/accounts/login/"]').click()
        # webDriver wait
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body')
        )
        # he accesses to the login form
        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys('toto@gmail.com')
        time.sleep(2)
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys('aqwz7418')
        time.sleep(2)
        # he posts the login form
        self.selenium.find_element_by_xpath('//input[@value="login"]').click()

        # he is connected
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body')
        )
        time.sleep(3)

        # he wants to logout
        self.selenium.find_element_by_xpath('//a[@href="/authentication/accounts/logout/"]').click()
        WebDriverWait(self.selenium, timeout).until(
            lambda driver: driver.find_element_by_tag_name('body')
        )

        # he is disconnected so we have the login icon
        self.selenium.find_element_by_xpath('//a[@href="/authentication/accounts/login/"]')

        # get the Live server url
        end_url = "{}/core/".format(self.live_server_url)
        self.assertEqual(self.selenium.current_url, end_url)