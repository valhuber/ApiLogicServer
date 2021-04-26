Ports and Hosts
===============
    Verified you can run SAFRS and Basic Web App concurrently
    Recent changes enabled pythonanywhere (PA), which works per wiki
    But, on local machine, none/any port has issues:
        swagger is still port 5000
        swagger-Execute locally fails to connect to server... needs to be 5000
        curl
            curl -X GET "http://localhost:8080/Order/?include=Customer%2CEmployee%2COrderDetailList&fields%5BOrder%5D=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CRequiredDate%2CShippedDate%2CShipVia%2CFreight%2CShipName%2CShipAddress%2CShipCity%2CShipRegion%2CShipPostalCode%2CShipCountry%2CAmountTotal&page%5Boffset%5D=0&page%5Blimit%5D=10&sort=Id%2CCustomerId%2CEmployeeId%2COrderDate%2CRequiredDate%2CShippedDate%2CShipVia%2CFreight%2CShipName%2CShipAddress%2CShipCity%2CShipRegion%2CShipPostalCode%2CShipCountry%2CAmountTotal%2Cid" -H  "accept: application/vnd.api+json" -H  "Content-Type: application/vnd.api+json"



TVF
===

Use SampleDB;

Alter FUNCTION udfEmployeeInLocation (
    @location nvarchar(50)
)
RETURNS TABLE
AS
RETURN
    SELECT
      Id, Name, Location
    FROM
      Employees
    WHERE
      Location LIKE @location;


SELECT * FROM udfEmployeeInLocation('Sweden');

this gives the cols:
SELECT TABLE_CATALOG AS [Database], TABLE_SCHEMA AS [Schema], TABLE_NAME AS [Function],
       COLUMN_NAME AS [Column], DATA_TYPE AS [Data Type], CHARACTER_MAXIMUM_LENGTH AS [Char Max Length]
FROM INFORMATION_SCHEMA.ROUTINE_COLUMNS
WHERE TABLE_NAME IN (SELECT ROUTINE_NAME FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_TYPE = 'FUNCTION' AND DATA_TYPE = 'TABLE') ORDER BY TABLE_NAME, COLUMN_NAME;

to get the args - https://www.mssqltips.com/sqlservertip/1669/generate-a-parameter-list-for-all-sql-server-stored-procedures-and-functions/
SELECT
   SCHEMA_NAME(SCHEMA_ID) AS [Schema]
  ,SO.name AS [ObjectName]
  ,SO.Type_Desc AS [ObjectType (UDF/SP)]
  ,P.parameter_id AS [ParameterID]
  ,P.name AS [ParameterName]
  ,TYPE_NAME(P.user_type_id) AS [ParameterDataType]
  ,P.max_length AS [ParameterMaxBytes]
  ,P.is_output AS [IsOutPutParameter]
FROM sys.objects AS SO
INNER JOIN sys.parameters AS P ON SO.OBJECT_ID = P.OBJECT_ID
ORDER BY [Schema], SO.name, P.parameter_id


SQLAlchemy 1.4.11
=================
Have LogicBank branch that works with it, as does ApiLogicServer.
But SAFRS.JABase fails, as does Flask AppBuilder.