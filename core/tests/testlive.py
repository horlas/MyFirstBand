from selenium.webdriver.chrome.webdriver import WebDriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait
import time

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['user-data.json']

    TIMEOUT = 2

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

    def webdriver_wait(self):

        return WebDriverWait(self.selenium, self.TIMEOUT).until(
            lambda driver: driver.find_element_by_tag_name('body')
        )

    def test_signin(self):
        # we are on the index page , user is not registered
        self.selenium.get(self.live_server_url)
        time.sleep(2)

        # user wants to sign-in
        self.selenium.find_element_by_xpath('//a[@href="/authentication/signup/"]').click()

        # webDriver wait
        self.webdriver_wait()

        # he accesses to the signin form
        username_input = self.selenium.find_element_by_id("id_email")
        username_input.send_keys('michel@gmail.com')
        time.sleep(2)
        password_input = self.selenium.find_element_by_id("id_password1")
        password_input.send_keys('aqwz7418')
        time.sleep(2)
        password_input = self.selenium.find_element_by_id("id_password2")
        password_input.send_keys('aqwz7418')
        time.sleep(2)
        # he posts the signin form
        self.selenium.find_element_by_id("sign_up_button").click()
        # he is connected
        self.webdriver_wait()
        time.sleep(3)

    def test_login_logout(self):

        # self.selenium.get('%s%s' % (self.live_server_url, '/authentication/accounts/login/'))
        # we are on the index page , user is not connected
        self.selenium.get(self.live_server_url)
        time.sleep(2)

        # user wants to connect
        self.selenium.find_element_by_xpath('//a[@href="/authentication/accounts/login/"]').click()

        # webDriver wait
        self.webdriver_wait()

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
        self.webdriver_wait()
        time.sleep(3)

        # he wants to logout
        self.selenium.find_element_by_xpath('//a[@href="/authentication/accounts/logout/"]').click()
        self.webdriver_wait()

        # he is disconnected so we have the login icon
        self.selenium.find_element_by_xpath('//a[@href="/authentication/accounts/login/"]')

        # get the Live server url
        end_url = "{}/core/".format(self.live_server_url)
        self.assertEqual(self.selenium.current_url, end_url)