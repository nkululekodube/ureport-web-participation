##### Forgotten the password for web-pro
Feature: A registered user has forgotten the password

  Scenario: User has forgotten the password for web-pro but has a registered email
    Given I am a registered user
    When I visit the login page
    And I click Forgot-password link
    Then I see the page requesting me for an email address
    And I shall input my email address
    And I shall see a notification 'We have sent an email ...'

  Scenario: User has forgotten the password for web-pro but submits a non-registered email
    Given I am a registered user
    When I visit the login page
    And I click Forgot-password link
    Then I see the page requesting me for an email address
    And I shall input a wrong email address
    And I shall see a notification 'There is no registered user ... '

  Scenario: Resetting password for web-pro with a matching passwords
    Given I am a registered user
    When I visit the login page
    And I click Forgot-password link
    And I see the page requesting me for an email address
    And I shall input my email address
    And I go to reset password page
    Then I shall change my password
    And I shall login with the new password

  Scenario: Resetting password for web-pro with  passwords that do not match
    Given I am a registered user
    When I visit reset password page
    And I submit my un matching passwords
    Then I see a notification of passwords do not match
    And I shall login with the old password
