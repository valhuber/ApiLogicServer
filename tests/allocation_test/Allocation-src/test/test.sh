#!/bin/bash

curl -X POST "http://localhost:5656/api/Payment/" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/json" -d "{  \"data\": {    \"attributes\": {      \"Amount\": 100,      \"CustomerId\": \"ALFKI\"    },    \"type\": \"Payment\"  }}" > results.txt

if grep -q '"AmountUnAllocated": 0.0' results.txt
    then
        echo "pass -- AmountUnAllocated:0.0"
    else
        if grep -q '"AmountUnAllocated":0.0' results.txt
            then
                echo "pass -- AmountUnAllocated:0.0"
            else
                echo "fail -"
        fi
fi