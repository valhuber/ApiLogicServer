Feature: Application Integration

  Scenario: GET Customer
     Given Customer Account: VINET
      When GET Orders API
      Then VINET retrieved


  Scenario: GET Department
     Given Department 2
      When GET Department with SubDepartments API
      Then SubDepartments returned
