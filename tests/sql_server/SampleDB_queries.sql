# test:
SELECT * FROM udfEmployeeInLocation('Sweden');

SELECT * FROM udfEmployeeInLocationWithName('Sweden', 'John');


CREATE FUNCTION [dbo].[FN_APPLY_FEE_LIST]
(
@EC_RSP_NO varchar(20)
)
RETURNS varchar(1000)
AS
BEGIN

DECLARE @strFeeName NVARCHAR(100)
DECLARE @strRetValue NVARCHAR(500)

SET @strRetValue = ''

........
RETURN ISNULL(@strRetValue ,'')
END


SELECT SCHEMA_NAME(SCHEMA_ID) AS [Schema],SO.name AS [ObjectName],SO.Type_Desc AS [ObjectType (UDF/SP)],P.parameter_id AS [ParameterID],P.name AS [ParameterName],TYPE_NAME(P.user_type_id) AS [ParameterDataType],P.max_length AS [ParameterMaxBytes],P.is_output AS [IsOutPutParameter]
FROM sys.objects AS SO INNER JOIN sys.parameters AS P ON SO.OBJECT_ID = P.OBJECT_ID
ORDER BY [Schema], SO.name, P.parameter_id

SELECT SO.name AS [ObjectName],SO.Type_Desc AS [ObjectType (UDF/SP)]
FROM sys.objects AS SO
ORDER BY SO.name

SELECT SO.name AS [ObjectName],SO.Type_Desc AS [ObjectType (UDF/SP)]
FROM sys.objects AS SO
WHERE SO.Type_Desc = 'SQL_INLINE_TABLE_VALUED_FUNCTION'
ORDER BY SO.name

SELECT SCHEMA_NAME(SCHEMA_ID) AS [Schema],SO.name AS [ObjectName],SO.Type_Desc AS [ObjectType (UDF/SP)],P.parameter_id AS [ParameterID],P.name AS [ParameterName],TYPE_NAME(P.user_type_id) AS [ParameterDataType],P.max_length AS [ParameterMaxBytes],P.is_output AS [IsOutPutParameter]
FROM sys.objects AS SO LEFT OUTER JOIN sys.parameters AS P ON SO.OBJECT_ID = P.OBJECT_ID
WHERE SO.Type_Desc = 'SQL_INLINE_TABLE_VALUED_FUNCTION'
ORDER BY [Schema], SO.name, P.parameter_id