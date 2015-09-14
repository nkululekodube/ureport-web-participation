#### #22: A global user verifies email during registration process
##### User Login
Feature: A registered user should be able to change my password

  Scenario: Resetting password for web-pro with a matching passwords

    Given I am a registered user
    When I change visit reset password page
    And I submit my new password
    Then I see a notification of password changed
    And I shall login with the new password


  Scenario: Resetting password for web-pro with  passwords that do not match
    Given I am a registered user
    When I change visit reset password page
    And I submit my un matching passwords
    Then I see a notification of passwords do not match
    And I shall login with the old password
