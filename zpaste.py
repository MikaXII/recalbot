from selenium import webdriver
import time
import settings

class ZPaste:

    def __init__(self, dict):

        self._isPaste = False
        self._link = ""

        self.driver = webdriver.PhantomJS()
        self.driver.get(settings.ZBIN)
        for value in dict.itervalues():
            self.driver.find_element_by_id('content').send_keys(value)
        self.driver.find_element_by_id("submit_form").click()

        while self.driver.current_url.find('paste') == -1:
            # print "Processing...Please wait..."
            # print driver.current_url
            time.sleep(1)

        # print driver.current_url
        self._link = self.driver.current_url
        self.driver.quit()


    def _get_is_paste(self):
        return self._isPaste

    def _get_link(self):
        return self._link

    isPaste = property(_get_is_paste)
    link = property(_get_link)
