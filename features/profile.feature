#### deactivate my wep-pro account

Feature: As a registered user
    i want to deactivate my account
    so that i can no longer be a u-reporter

    Scenario: Deactivate account

      Given I am a registered user
      When I login to u-report
      And I go to the profile page
      And I deactivate my account
      Then I shall not be able to login