Feature: Place Order

  Scenario: Good Order Custom Service
     Given Customer Account: ALFKI
      When Good Order Placed
      Then Logic adjusts Balance (demo: chain up)
      Then Logic adjusts Products Reordered
      Then Logic sends email to salesrep
      Then Logic adjusts aggregates down on delete order


  Scenario: Bad Order Custom Service
     Given Customer Account: ALFKI
      When Order Placed with excessive quantity
      Then Rejected per Check Credit


  Scenario: Alter Item Qty to exceed credit
     Given Customer Account: ALFKI
      When Order Detail Quantity altered very high
      Then Rejected per Check Credit


  Scenario: Alter Required Date - adjust logic pruned
     Given Customer Account: ALFKI
      When Order RequiredDate altered (2013-10-13)
      Then Balance not adjusted


  Scenario: Set Shipped - adjust logic reuse
     Given Customer Account: ALFKI
      When Order ShippedDate altered (2013-10-13)
      Then Balance reduced 1086


  Scenario: Reset Shipped - adjust logic reuse
     Given Shipped Order
      When Order ShippedDate set to None
      Then Logic adjusts Balance by -1086


  Scenario: Clone Existing Order
     Given Shipped Order
      When Cloning Existing Order
      Then Logic Copies ClonedFrom OrderDetails
