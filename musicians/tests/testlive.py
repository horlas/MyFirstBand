# from selenium.webdriver.chrome.webdriver import WebDriver
# from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from selenium.webdriver.support.wait import WebDriverWait
# import time
#
# class MySeleniumTests(StaticLiveServerTestCase):
#
#     fixtures = ['profil-data.json', 'user-data.json']
#     TIMEOUT = 2
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.selenium = WebDriver()
#         cls.selenium.maximize_window()
#         cls.selenium.implicitly_wait(10)
#     @classmethod
#     def tearDownClass(cls):
#         cls.selenium.quit()
#         super().tearDownClass()
#
#     def webdriver_wait(self):
#
#         return WebDriverWait(self.selenium, self.TIMEOUT).until(
#             lambda driver: driver.find_element_by_tag_name('body')
#         )
#
#     def test_update_profile(self):
