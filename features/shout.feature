#####  Send unsolicited massages
Feature: A registered user should be able to send  unsolicited massages to web-pro

  Scenario: Sending unsolicited massages to web-pro

    Given I am a logged into wep-pro
    When I visit the shout page
    Then I shall be able to send a message
