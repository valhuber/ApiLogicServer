#!/bin/bash

if [ $# -eq 0 ]
    then
        echo " "
        echo "\n Runs logic audit test - using shell scripts for testing"
        echo " "
        echo " IMPORTANT:"
        echo "   1. Server running on localhost:5656 "
        echo "   2. Run this from the test directory "
        echo " "
        echo "  sh server_test.sh [ go ]"
        echo " "
        exit 0
    fi

echo "\n Update employee"
curl -X PATCH "http://localhost:5656/api/Employee/1/" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/json" -d "{  \"data\": {    \"attributes\": {      \"Salary\": 200000    },    \"type\": \"Employee\",    \"id\": \"1\"  }}" > results-give-raise.txt
if grep -q '"Salary": 200000' results-give-raise.txt
    then
        echo "..pass update emp"
    else
        more results-give-raise.txt
        echo '..FAIL update emp - did not see "Salary": 200000'
        exit 1
fi

echo "\n Verify audited"
curl -X GET "http://localhost:5656/api/EmployeeAudit/?include=Employee&fields%5BEmployeeAudit%5D=Id%2CTitle%2CSalary%2CLastName%2CFirstName%2CEmployeeId%2CCreatedOn&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=Id%2CTitle%2CSalary%2CLastName%2CFirstName%2CEmployeeId%2CCreatedOn%2Cid" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/vnd.api+json" > results-verify-audit.txt
if grep -q '"Salary": 200000' results-verify-audit.txt
    then
        echo '..pass audited'
    else
        more results-verify-audit.txt
        echo '..FAIL audited - did not see "Salary": 200000'
        exit 1
fi
