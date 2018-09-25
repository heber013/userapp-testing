from behave import step


@step(u'I enter the following user info')
def enter_user_info(context):
    """
    Enter the user information in the web page
    :return The corresponding page object instance stored in context
    variable: current_page
    """
    for row in context.table:
        context.current_page.enter_username(row['username'])
        context.current_page.enter_email(row['email'])
        context.current_page.enter_birthday(row['birthdate'])
        context.current_page.enter_address(row['address'])
    return context.current_page


@step(u'I confirm the operation of adding the new user')
def confirm_adding_user(context):
    return context.current_page.press_add_user_btn()


@step(u'The following user is on the list')
def check_users(context):
    for row in context.table:
        assert context.current_page.is_user_in_list(row), \
            'User not found in the list:%s' % row


@step(u'The following user is NOT in the list')
def check_users(context):
    for row in context.table:
        assert not context.current_page.is_user_in_list(row), \
            'User found in the list when it should not: %s' % row


@step(u'I see an error in "{field_name}" field')
def confirm_adding_user(context, field_name):
    assert context.current_page.is_field_error_present(field_name), \
        'Error not found for field: %s' % field_name
