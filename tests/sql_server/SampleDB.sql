CREATE DATABASE [SampleDB]
go

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


CREATE FUNCTION [dbo].[fn_Get_COD111]
(
@Key nvarchar(2)
)
RETURNS TABLE
AS
RETURN
(
select *
from DataTypes
where "Key"=(case when @Key='' then "Key" else @Key end)
)

CREATE FUNCTION [dbo].[fn_Data_u_CDM_BusinessProcess_yyyy] ()
returns Table
as
return
(
select char_type as 'Document'
from fn_Get_COD111('r1')
)

