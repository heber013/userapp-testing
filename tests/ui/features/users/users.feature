Feature: Verify users page

  @WebUiTest
  Scenario: Verify I can add a new user in the web app ui
    Given I open the app in a browser
    When I enter the following user info:
      | username | email              | birthdate  | address    |
      | usertest | usertest@gmail.net | 04-20-1988 | street 123 |
    And I confirm the operation of adding the new user
    Then The following user is on the list:
      | username | email              | birthdate  | address    |
      | usertest | usertest@gmail.net | 1988-04-20 | street 123 |

  @WebUiTest
  Scenario: Verify I can add a new user with special characters in the username
    Given I open the app in a browser
    When I enter the following user info:
      | username    | email                | birthdate  | address      |
      | usertest$%& | usertest@hotmail.net | 04-20-1917 | mystraat 123 |
    And I confirm the operation of adding the new user
    Then The following user is on the list:
      | username    | email                | birthdate  | address      |
      | usertest$%& | usertest@hotmail.net | 1917-04-20 | mystraat 123 |

  @WebUiTest
  Scenario: Verify that username is mandatory when adding a new user
    Given I open the app in a browser
    When I enter the following user info:
      | username | email               | birthdate  | address    |
      |          | usertest2@gmail.net | 04-20-1978 | straat 001 |
    And I confirm the operation of adding the new user
    And I see an error in "username" field
    Then The following user is NOT in the list:
      | username | email               | birthdate  | address    |
      |          | usertest2@gmail.net | 04-20-1978 | straat 001 |

  @WebUiTest
  Scenario: Verify that email is mandatory when adding a new user
    Given I open the app in a browser
    When I enter the following user info:
      | username    | email | birthdate  | address    |
      | testinguser |       | 01-29-1987 | straat 001 |
    And I confirm the operation of adding the new user
    And I see an error in "emailaddress" field
    Then The following user is NOT in the list:
      | username    | email | birthdate  | address    |
      | testinguser |       | 01-29-1987 | straat 001 |

  @WebUiTest
  Scenario: Verify that birthdate is mandatory when adding a new user
    Given I open the app in a browser
    When I enter the following user info:
      | username | email           | birthdate | address     |
      | myuser   | myuser@test.net |           | straat 4875 |
    And I confirm the operation of adding the new user
    And I see an error in "birthdate" field
    Then The following user is NOT in the list:
      | username | email           | birthdate | address     |
      | myuser   | myuser@test.net |           | straat 4875 |

  @WebUiTest
  Scenario: Verify that address is mandatory when adding a new user
    Given I open the app in a browser
    When I enter the following user info:
      | username | email           | birthdate  | address |
      | myuser   | myuser@test.net | 01-29-1987 |         |
    And I confirm the operation of adding the new user
    And I see an error in "address" field
    Then The following user is NOT in the list:
      | username | email           | birthdate  | address |
      | myuser   | myuser@test.net | 01-29-1987 |         |

  @WebUiTest
  Scenario: Verify that it is not possible add an user with an invalid email address
    Given I open the app in a browser
    When I enter the following user info:
      | username | email              | birthdate  | address    |
      | myuser   | myuserinvalidemail | 04-20-2005 | straat 555 |
    And I confirm the operation of adding the new user
    And I see an error in "emailaddress" field
    Then The following user is NOT in the list:
      | username | email              | birthdate  | address    |
      | myuser   | myuserinvalidemail | 04-20-2005 | straat 555 |

  @WebUiTest
  Scenario: Verify that it is not possible add an user with a birthdate later than today
    Given I open the app in a browser
    When I enter the following user info:
      | username | email               | birthdate  | address    |
      | theuser  | theuser@hotmail.com | 04-20-9000 | straat 555 |
    And I confirm the operation of adding the new user
    And I see an error in "birthdate" field
    Then The following user is NOT in the list:
      | username | email               | birthdate  | address    |
      | theuser  | theuser@hotmail.com | 04-20-9000 | straat 555 |