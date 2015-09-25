##### Logging in to web-pro
Feature: As registered user
  I should be able to login to web-pro

  Scenario: Logging in to web-pro

    Given I am a registered user
    When I visit the login page
    Then I shall login
    Then I see the link to logout
    And I should be able logout
    And I shall see a link to login
