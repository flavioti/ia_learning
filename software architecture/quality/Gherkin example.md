```Gherkin
Feature: Applying discount coupons at checkout
  As an online shopper
  I want to apply a discount code to my shopping cart
  So that I can pay a reduced price for my order

  Scenario Outline: Applying promo codes during checkout
    Given the user has items in their cart totaling $<CartTotal>
    When the user enters the promo code "<PromoCode>"
    And applies the coupon
    Then the final total should be $<FinalTotal>
    And a notification message "<Message>" should be displayed

    Examples:

      | CartTotal | PromoCode | FinalTotal | Message                     |
      | 100.00    | SAVE20    | 80.00      | Coupon applied successfully |
      | 50.00     | SAVE20    | 50.00      | Minimum spend not met       |
      | 75.00     | INVALID   | 75.00      | Invalid promo code          |

```