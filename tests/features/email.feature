### #22: A global user verifies email during registration process
### User Registration

Feature: A global user verifies email during registration process
    As a global user
    i want to verify my email address during the registration process
    so that i can become a U-Reporter

### @tag ="UserRegistration"

  Scenario: Wrong email format
    Given I am a new user  with a wrong email format
    When I browse to u-report
    And I enter a wrong format for an email address
    And I click submit
    Then I should see a message "that does not seem to be a valid email address."

  Scenario: Registration a new User
    Given I am a new user with a correct email format
    When I browse to u-report
    And I fill in my email address
    And I click submit
    Then I shall see "my email" and a notification "Thanks! Just to confirm that you are actually you".

  Scenario:Wrong verification code
    Given I am a new user who has submitted their email address
    When I browse to u-report
    And I misspell the verification code
    And I click submit
    Then Then I should see a message "I'm sorry, that's an invalid code."

  Scenario: Double Registration for a User
    Given I am already registered
    When I browse to u-report
    And I fill in my email address
    And I click submit
    Then I shall see a notification "Email already registered".