create table DataTypes
(
	[Key] nvarchar(10) not null
		constraint DataTypes_pk
			primary key nonclustered,
	char_type char(10),
	varchar_type varchar(10)
)
go

create table Employees
(
	Id int identity
		primary key,
	Name nvarchar(50),
	Location nvarchar(50)
)
go


CREATE FUNCTION udfEmployeeInLocation (
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
      Location LIKE @location
go


CREATE FUNCTION udfEmployeeInLocationWithName (
    @location nvarchar(50),
    @Name nvarchar(50)
)
RETURNS TABLE
AS
RETURN
    SELECT
      Id, Name, Location
    FROM
      Employees
    WHERE
      Location LIKE @location and Name like @Name
go


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