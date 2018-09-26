from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage

_username = (By.ID, 'username')
_emailaddress = (By.ID, 'emailaddress')
_birthday = (By.ID, 'birthdate')
_address = (By.ID, 'address')
_add_user_btn = (By.ID, 'adduserbtn')
_users_table = (By.ID, 'userlist')


class UsersPage(BasePage):

    def enter_username(self, username):
        self.find_element(_username).send_keys(username)
        return self

    def enter_email(self, email):
        self.find_element(_emailaddress).send_keys(email)
        return self

    def enter_birthday(self, birthday):
        _birthday_field = self.find_element(_birthday)
        _birthday_field.send_keys(birthday)
        if not _birthday_field.get_attribute('value'):
            actions = ActionChains(self.driver)
            actions.move_to_element(_birthday_field)
            actions.click(on_element=_birthday_field)
            actions.send_keys(birthday)
            actions.perform()
        return self

    def enter_address(self, address):
        self.find_element(_address).send_keys(address)
        return self

    def press_add_user_btn(self):
        self.find_element(_add_user_btn).click()
        return self

    def get_users(self):
        users_table = self.find_element(_users_table)
        users = []
        header = []
        for i, row in enumerate(users_table.find_elements(*(By.TAG_NAME, 'tr'))):
            user = {}
            if i == 0:
                header = [cell.text.lower() for cell in row.find_elements(*(By.TAG_NAME, 'td'))]
                continue
            for j, cell in enumerate(row.find_elements(*(By.TAG_NAME, 'td'))):
                user[header[j]] = cell.text
            users.append(user)
        return users

    def is_user_in_list(self, user_to_check):
        current_users = self.get_users()
        for user in current_users:
            if (user_to_check['username'] == user['username']) and (
                    user_to_check['email'] == user['email']) and (
                    user_to_check['birthdate'] == user['birthdate']) and (
                    user_to_check['address'] == user['address']):
                return True
        return False

    def is_field_error_present(self, field_name):
        return self.find_element((By.ID, field_name)).get_attribute('validationMessage')
