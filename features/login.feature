#### #22: A global user verifies email during registration process
##### User Login
Feature: A registered user should be able to login to webpro

  Scenario: Logging in to webpro

    Given I am a regsterd user
    When I log in to webpro
    Then I see the link to logout
    And I logout