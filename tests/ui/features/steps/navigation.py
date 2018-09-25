import os

from behave import step

from page_objects.users_page import UsersPage


@step(u'I open the app in a browser')
def open_app(context):
    """
    Open users app in a web browser
    :return The corresponding page object instance stored in context
    variable: current_page
    """
    context.browser.get(os.environ.get('WEB_ADDRESS'))
    context.current_page = UsersPage(context.browser)
    return context.current_page


@step(u'I am on "{page}" Page')
def check_page(context, page):
    """
    Check if the given page is the one that is open in the browser
    :param page: the page to check. Can be the page title or the url.
    """
    assert page in context.browser.title or page in context.browser.current_url, \
        'Pages do not match. Actual: %s. Expected: %s' % (
            context.browser.title, page)
