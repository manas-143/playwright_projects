Feature: Google map feature
  Scenario Outline: Search for top 20 places
    Given User is on the google map website
    When User search for "<places>"
    And add top "<num>" places with its information
    Then User makes a csv file to save the information
    Examples:
      |   places      | num   |
      | Restaurants   |  5    |
      | Hotels        |  10   |
      | temples       |  15   |
