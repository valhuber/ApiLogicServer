Ports and Hosts
    Verified you can run SAFRS and Basic Web App concurrently
    Recent changes enabled pythonanywhere (PA), which works per wiki
    But, on local machine, none/any port has issues:
        swagger is still port 5000
        swagger-Execute locally fails to connect to server... needs to be 5000
        curl
            curl -X GET "http://localhost:8080/Order/?include=Customer%2CEmployee%2COrderDetailList&fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CRequiredDate%2CShippedDate%2CShipVia%2CFreight%2CShipName%2CShipAddress%2CShipCity%2CShipRegion%2CShipPostalCode%2CShipCountry%2CAmountTotal&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CRequiredDate%2CShippedDate%2CShipVia%2CFreight%2CShipName%2CShipAddress%2CShipCity%2CShipRegion%2CShipPostalCode%2CShipCountry%2CAmountTotal%2Cid" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/vnd.api+json"

