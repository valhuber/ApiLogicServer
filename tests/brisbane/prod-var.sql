SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
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
) ON [TMVXTEMP]
GO
