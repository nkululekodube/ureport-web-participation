### #22: A global user verifies email during registration process

Feature: User Registration
    As a global user
    i want to verify my email address during the registration process
    so that i can become a U-Reporter

### @tag ="UserRegistration"

    Scenario: Registration a new User
        Given I am a new user
        When I browse to u-report website
        And I fill in critical registration details
        And I click submit critical registration details
        Then I shall be a registered u-reporter.