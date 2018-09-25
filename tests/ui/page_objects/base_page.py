# -*- coding: utf-8 -*-
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.wait import WebDriverWait


class BasePage:
    TITLE = u''

    def __init__(self, driver):
        self.driver = driver

    def find_element(self, locator, condition=ec.visibility_of_element_located, **kwargs):
        """
        Find a web element that matches the expected condition using explicit wait
        :param locator: the locator to look for the web element
        :param condition: the condition to look for the web element: visible, clickable, etc.
        :return: the web element that match the locator and condition
        :raise: timeout exception if element is not found in the given retries and time
        """
        wait = kwargs.get('wait', 2)
        retries = kwargs.get('retries', 5)
        wd_wait = WebDriverWait(self.driver, wait)
        acum = 0
        element = None
        while acum <= retries and not element:
            try:
                if wd_wait.until(condition(locator)):
                    element = self.driver.find_element(*locator)
                    acum += 1
            except TimeoutException:
                acum += 1
        return element

    def find_elements(self, locator, condition=ec.visibility_of_element_located, **kwargs):
        """
        Find a list web elements that match the expected condition using explicit wait
        :param locator: the locator to look for the web elements
        :param condition: the condition to look for the web elements: visible, clickable, etc.
        :return: a list of web elements that match the locator and condition
        :raise: timeout exception if no element is found in the given retries and time
        """
        wait = kwargs.get('wait', 2)
        retries = kwargs.get('retries', 5)
        wd_wait = WebDriverWait(self.driver, wait)
        acum = 0
        elements = []
        while acum <= retries and not elements:
            try:
                if wd_wait.until(condition(locator)):
                    elements = self.driver.find_elements(*locator)
                    acum += 1
            except TimeoutException:
                acum += 1
        return elements

    def get(self, url):
        """
        Navigate to the given url
        :param url: the url to navigate to
        """
        self.driver.get(url)
