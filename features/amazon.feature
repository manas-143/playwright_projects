Feature: Amazon laptop purchase
  Scenario Outline: Search for laptops,add to cart and verify the total price
    Given User is on the amazon website
    When User search for "<laptops>"
    And User filter by ratings
    And add top "<num>" laptops to the cart
    Then the total amount in the cart should match the laptop prices
    Examples:
      |   laptops    | num |
      | HP LAPTOPS   |  4  |
      | dELL LAPTOPS |  3  |
      | ACER LAPTOPS |  5  |

