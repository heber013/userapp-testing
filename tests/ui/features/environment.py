import os
import requests

from selenium import webdriver


def before_all(context):
    browser = os.environ.get('BROWSER', 'chrome')
    grid_url = os.environ.get('GRID_URL')
    capabilities = getattr(webdriver.DesiredCapabilities, browser.upper())
    if grid_url:
        context.browser = webdriver.Remote(grid_url,
                                           desired_capabilities=capabilities)
    elif browser == 'firefox':
        context.browser = webdriver.Firefox(capabilities=capabilities)
    elif browser == 'chrome':
        context.browser = webdriver.Chrome(desired_capabilities=capabilities)
    requests.delete(os.environ.get('WEB_ADDRESS') + '/deleteall')


def after_all(context):
    context.browser.quit()
