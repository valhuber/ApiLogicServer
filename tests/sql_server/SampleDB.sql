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

create table "Plus+Table"
(
	Id int identity
		primary key,
	Name nvarchar(50),
	Location nvarchar(50)
)
go

CREATE TABLE [dbo].[Plus+Table](
	[Id] [int] IDENTITY(1,1) NOT NULL
	    , [Name] [nvarchar](50) NULL
	    , [Location] [nvarchar](50) NULL
        , QtyAvailable smallint
        , UnitPrice money
        , InventoryValue AS QtyAvailable * UnitPrice) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Plus+Table] ADD PRIMARY KEY CLUSTERED
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO


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

