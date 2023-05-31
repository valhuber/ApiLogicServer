Feature: Optimistic Locking

   Scenario: Get Category
      Given Category: 1
      When Get Cat1
      Then Expected Cat1 Checksum

   Scenario: Valid Checksum
      Given Category: 1
      When Patch Valid Checksum
      Then Valid Checksum, Invalid Description

   Scenario: Missing Checksum
      Given Category: 1
      When Patch Missing Checksum
      Then Valid Checksum, Invalid Description

   Scenario: Invalid Checksum
      Given Category: 1
      When Patch Invalid Checksum
      Then Invalid Checksum    