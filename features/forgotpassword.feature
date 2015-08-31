#### #22: A global user verifies email during registration process
##### User Login
Feature: A registered user should be able to change my password

  Scenario: Resetting password for web-pro with a registered email

    Given I am a registered user
    When I visit the login page
    And I click Forgot-password link
    Then I see the page requesting me for an email address
    And I shall input my email address
    And I shall see a notification 'We have sent an email ...'


  Scenario: Resetting password for web-pro with non registered email

    Given I am a registered user
    When I visit the login page
    And I click Forgot-password link
    Then I see the page requesting me for an email address
    And I shall input a wrong email address
    And I shall see a notification 'There is no registered user ... '
