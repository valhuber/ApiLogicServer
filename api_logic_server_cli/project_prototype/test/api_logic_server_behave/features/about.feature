# Create 1 or more .feature files here, and corresponding /steps/<feature>.py files
# Run Launch Configuration:
#   - Behave Run - runs your test suite
#   - Behave Logic Report - produces wiki for Behave Run, including Logic

Feature: About Sample

  Scenario: Transaction Processing
     Given Sample Database
      When Transactions are submitted
      Then Enforce business policies with Logic (rules + code)

