from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait
import time
import os

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

    # def test_signin(self):
    #     # we are on the index page , user is not registered
    #     print('We test the sign in form')
    #
    #     self.selenium.get(self.live_server_url)
    #     time.sleep(2)
    #
    #     # user wants to sign-in
    #     self.selenium.find_element_by_xpath('//a[@href="/authentication/signup/"]').click()
    #
    #     # webDriver wait
    #     self.webdriver_wait()
    #
    #     # he accesses to the signin form
    #     username_input = self.selenium.find_element_by_id("id_email")
    #     username_input.send_keys('michel@gmail.com')
    #     time.sleep(2)
    #     password_input = self.selenium.find_element_by_id("id_password1")
    #     password_input.send_keys('aqwz7418')
    #     time.sleep(2)
    #     password_input = self.selenium.find_element_by_id("id_password2")
    #     password_input.send_keys('aqwz7418')
    #     time.sleep(2)
    #     # he posts the signin form
    #     self.selenium.find_element_by_id("sign_up_button").click()
    #     # he is connected so we have the logout icon
    #     self.webdriver_wait()
    #     time.sleep(3)
    #     self.selenium.find_element_by_xpath('//a[@href="/authentication/accounts/logout/"]')
    #
    #     # get the Live server url
    #     end_url = "{}/core/".format(self.live_server_url)
    #     self.assertEqual(self.selenium.current_url, end_url)

    def test_login_logout(self):

        path = os.getcwd()
        print(path)

        print('We test the login form')

        # self.selenium.get('%s%s' % (self.live_server_url, '/authentication/accounts/login/'))
        # we are on the index page , user is not connected
        self.selenium.get(self.live_server_url)
        time.sleep(2)

        # user wants to connect
        self.selenium.find_element_by_id('login').click()

        # webDriver wait
        self.webdriver_wait()

        # he accesses to the login form
        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys('tata@gmail.com')
        time.sleep(2)
        password_input = self.selenium.find_element_by_id("id_password")
        password_input.send_keys('aqwz7418')
        time.sleep(2)
        # he posts the login form
        self.selenium.find_element_by_xpath('//button["#login_button"]').click()

        # he is connected
        print('He is connected')
        self.webdriver_wait()
        time.sleep(3)

        # he wants to update his profil
        print('he updates his profil')
        # print(self.request.user.id)
        self.selenium.find_element_by_id('edit-compte').click()
        self.webdriver_wait()
        time.sleep(2)
        self.selenium.find_element_by_id('trigger_avatar').click()
        self.webdriver_wait()


        print('He upload his avatar')
        time.sleep(4)
        avatar_input = self.selenium.find_element_by_id("id_avatar")
        avatar_input.send_keys(os.getcwd() + '/musicians/tests/test_img/test.png')
        time.sleep(2)
        self.selenium.find_element_by_id('submit_avatar').click()
        self.webdriver_wait()
        # time.sleep(4)

        print('He uploads his datas')
        self.selenium.find_element_by_id('trigger_profil').click()
        self.webdriver_wait()
        username_input = self.selenium.find_element_by_id("id_username")
        username_input.send_keys('Super Tatie')
        time.sleep(2)
        bio_input = self.selenium.find_element_by_id("id_bio")
        bio_input.send_keys("J'aime la musique et m'amuser!")
        time.sleep(2)
        by_input = self.selenium.find_element_by_id("id_birth_year")
        by_input.send_keys(1948)
        time.sleep(2)

        # self.selenium.find_element_by_class_name('dropdown-content select-dropdown').click()

        self.selenium.find_element_by_xpath("//input[@class='select-dropdown dropdown-trigger']").click()

        self.webdriver_wait()

        time.sleep(2)
        self.selenium.find_element_by_xpath("//li/span[contains(text(), 'Femme')]").click()

        self.webdriver_wait()
        time.sleep(2)
        self.selenium.find_element_by_id('submit_profile').click()
        self.webdriver_wait()
        # time.sleep(2)

        print('He moves ')
        self.selenium.find_element_by_id('trigger-local').click()
        self.webdriver_wait()
        code = self.selenium.find_element_by_id("id_code")
        code.send_keys(34)
        time.sleep(2)
        self.selenium.find_element_by_id('send').click()
        self.webdriver_wait()
        time.sleep(3)
        alert = self.selenium.find_element_by_id("bad_cp")
        time.sleep(3)
        if alert.is_displayed():
            print('alert found')
            time.sleep(3)
            self.selenium.find_element_by_xpath("//a[@class='modal-close waves-effect waves-green btn-flat']").click()
        time.sleep(2)
        code.clear()
        code.send_keys(31170)
        time.sleep(2)
        self.selenium.find_element_by_id('send').click()
        self.webdriver_wait()
        time.sleep(2)
        self.selenium.find_element_by_id('submit_local').click()
        self.webdriver_wait()
        time.sleep(2)

        print('His new home is updated ')

        # print('The user add an instrument ')
        # self.selenium.find_element_by_id('trigger-instru').click()
        # self.webdriver_wait()
        # self.selenium.find_element_by_id('add').click()
        # self.webdriver_wait()
        # dropdowns = self.selenium.find_elements_by_xpath("//input[@class='select-dropdown dropdown-trigger'][0]")
        # print(dropdowns[0])
        # dropdowns.click()
        #
        # for input in dropdowns:
        #     print(input)
        #
        # # By.xpath("(//span[@class='title'])[0]"));
        # # self.selenium.find_element_by_xpath("//input[@data-target='select-options-ca4e91b3-2dce-58dd-472c-fdec5d160b7b']").click()
        # self.webdriver_wait()
        # time.sleep(2)
        # self.selenium.find_element_by_xpath("//li/span[contains(text(), 'Bassiste')]").click()
        # self.webdriver_wait()
        # time.sleep(2)


        # Todo : test intru form add plus delete
        # Todo : check username in index page when the user is connected








        # he wants to logout

        # self.selenium.find_element_by_xpath('//a[@href="/authentication/accounts/logout/"]').click()
        # self.webdriver_wait()
        #
        # # he is disconnected so we have the login icon
        # self.selenium.find_element_by_xpath('//a[@href="/authentication/accounts/login/"]')
        #
        # # get the Live server url
        # end_url = "{}/core/".format(self.live_server_url)
        # self.assertEqual(self.selenium.current_url, end_url)
        # print('he is disconnected')