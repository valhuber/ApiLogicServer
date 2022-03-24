Feature: Salary Change

  Scenario: Audit Salary Change
     Given Employee 5 (Buchanan) - Salary 95k
      When Patch Salary to 200k
      Then Salary_audit row created

  Scenario: Raise Must be Meaningful
     Given Employee 5 (Buchanan) - Salary 95k
      When Patch Salary to 96k
      Then Reject - Raise too small
