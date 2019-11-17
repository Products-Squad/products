Feature: The product service back-end
    As a Product Store Owner
    I need a RESTful catalog service
    So that I can keep track of all my products

Background:
    Given the following products
        |             name              | stock | price |                      description                        | category |
        |    Wagyu Tenderloin Steak     |	 11  | 20.56 |	   The most decadent, succulent cut of beef, ever.     |   Food   | 
	    |      Y type Headphones        |   10  | 30.99 |       The best over-ear headphones for audiophiles      |Electronics|

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Product RESTful Service" in the title
    And I should not see "404 Not Found"

Scenario: Create a Product
    When I visit the "Home Page"
    And I set the "Name" to "Shampos"
    And I set the "Stock" to "48"
    And I set the "Price" to "12.34"
    And I set the "Description" to "Shampoo is a hair care product, typically in the form of a viscous liquid, that is used for cleaning hair"
    And I set the "Category" to "Health Care"
    And I press the "Create" button
    Then I should see the message "Success"
    When I copy the "Id" field
    And I press the "Clear" button
    Then the "Id" field should be empty
    And the "Name" field should be empty
    And the "Stock" field should be empty
    And the "Price" field should be empty
    And the "Description" field should be empty
    And the "Category" field should be empty
    When I paste the "Id" field
    And I press the "Retrieve" button
    Then I should see "Shampos" in the "Name" field
    And I should see "48" in the "Stock" field
    And I should see "12.34" in the "Price" field
    And I should see "Shampoo is a hair care product, typically in the form of a viscous liquid, that is used for cleaning hair" in the "Description" field
    And I should see "Health Care" in the "Category" field
    
Scenario: List all products
    When I visit the "Home Page"
    And I press the "Search" button
    Then I should see "Wagyu Tenderloin Steak" in the results
    And I should see "Y type Headphones" in the results
    
Scenario: List by Category
    When I visit the "Home Page"
    And I set the "Category" to "Food"
    And I press the "Search" button
    Then I should see "Wagyu Tenderloin Steak" in the results
    And I should not see "Y type Headphones" in the results

 Scenario: List by Name
    When I visit the "Home Page"
    And I set the "Name" to "Wagyu Tenderloin Steak"
    And I press the "Search" button
    Then I should see "Wagyu Tenderloin Steak" in the results
    And I should not see "Y type Headphones" in the results   

Scenario: Retrieve a Product
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "Wagyu Tenderloin Steak" in the "Name" field
    And I should see "11" in the "Stock" field
    And I should see "20.56" in the "Price" field
    And I should see "The most decadent, succulent cut of beef, ever." in the "Description" field
    And I should see "Food" in the "Category" field
    
Scenario: Update a Product
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Retrieve" button 
    Then I should see "Wagyu Tenderloin Steak" in the "Name" field
    When I change "Name" to "Wagyu Tenderloin Beef"
    And I press the "Update" button
    Then I should see the message "Success"
    When I set the "Id" to "1"
    And I press the "Retrieve" button
    Then I should see "Wagyu Tenderloin Beef" in the "Name" field
    When I press the "Clear" button 
    And I press the "Search" button
    Then I should see "Wagyu Tenderloin Beef" in the results
    And I should not see "Wagyu Tenderloin Steak" in the results

Scenario: Delete a Product
    When I visit the "Home Page"
    And I set the "Id" to "1"
    And I press the "Delete" button 
    Then I should see the message "Product has been Deleted!"
    When I press the "Clear" button
    And I set the "Id" to "1"
    And I press the "Search" button
    Then I should not see "Wagyu Tenderloin Steak" in the results

Scenario: Buy a Product
    When I visit the "Home Page"
    And I set the "Id" to "2"
    And I press the "Retrieve" button
    Then I should see "10" in the "Stock" field
    When I press the "Buy" button
    Then I should see the message "Success"
    When I press the "Clear" button
    And I set the "Id" to "2"
    And I press the "Retrieve" button
    Then I should see "9" in the "Stock" field

