#### Web Pro main page features

Feature: A visitor should be able to browses webpro
    As a visitor
    i want to browses webpro
    so that i can register or login

    Scenario: A visitor browses to webpro
    Given I am a visitor to webpro
    When I browse to webpro
    Then I shall see a link to register
    And I shall also see a link to login