CREATE DATABASE [SampleDB]
go

use SampleDB
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


CREATE TABLE [dbo].[Dash-Table](
	[Id] [int] IDENTITY(1,1) NOT NULL
	    , [Name] [nvarchar](50) NULL
	    , [Location] [nvarchar](50) NULL
        , QtyAvailable smallint
        , UnitPrice money
        , InventoryValue AS QtyAvailable * UnitPrice) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Dash-Table] ADD PRIMARY KEY CLUSTERED
(
	[Id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO

create view "Dash-View" as select * from [dbo].[Dash-Table]

CREATE TABLE [dbo].[productvariantsoh-20190423](
	[id] [varchar](55) NULL,
	[product_id] [varchar](55) NULL,
	[qty_brisbane] [int] NULL,
	[qty_chadstone] [int] NULL,
	[qty_melbourne] [int] NULL,
	[qty_parramatta] [int] NULL,
	[qty_perth] [int] NULL,
	[qty_southport] [int] NULL,
	[qty_sydney] [int] NULL,
	[qty_goldcoast] [int] NULL,
	[qty_warehouse] [int] NULL
)
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Dates](
	[dt] [date] NOT NULL,
	[d]  AS (datepart(day,[dt])),
	[y]  AS (datepart(year,[dt])),
	[q]  AS (datepart(quarter,[dt])),
	[m]  AS (datepart(month,[dt])),
	[fm]  AS (dateadd(month,datediff(month,(0),[dt]),(0))),
	[w]  AS (datepart(week,[dt])),
	[wd]  AS (datepart(weekday,[dt])),
	[mn]  AS (datename(month,[dt])),
	[s101]  AS (CONVERT([char](10),[dt],(101))),
	[s103]  AS (CONVERT([char](10),[dt],(103))),
	[s112]  AS (CONVERT([char](8),[dt],(112))),
PRIMARY KEY CLUSTERED
(
	[dt] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
)
GO
SET ARITHABORT ON
SET CONCAT_NULL_YIELDS_NULL ON
SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
SET ANSI_PADDING ON
SET ANSI_WARNINGS ON
SET NUMERIC_ROUNDABORT OFF
GO
CREATE NONCLUSTERED INDEX [i1] ON [dbo].[Dates]
(
	[s112] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
CREATE NONCLUSTERED INDEX [s112_index] ON [dbo].[Dates]
(
	[s112] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, DROP_EXISTING = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, FILLFACTOR = 90)
GO


CREATE TABLE [dbo].[_Dates](
	[d] [date] NOT NULL,
PRIMARY KEY CLUSTERED
(
	[d] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON)
)
GO


SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Storessales20190416-20190423(2)](
	[GL_ARTICLE] [varchar](55) NULL,
	[Store ID] [varchar](55) NULL,
	[GA_CHARLIBRE2] [varchar](55) NULL,
	[M3 item code] [varchar](55) NULL,
	[Qty] [int] NULL
)
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

