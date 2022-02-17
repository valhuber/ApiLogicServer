# coding: utf-8
from sqlalchemy.dialects.mysql import *
from sqlalchemy import Boolean, CHAR, Column, Computed, DECIMAL, Date, DateTime, Index, Integer, NCHAR, Numeric, String, Table, Unicode, text
from sqlalchemy.ext.declarative import declarative_base


########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
from safrs import SAFRSBase

import safrs

Base = declarative_base()
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

# from sqlalchemy.dialects.mysql import *
########################################################################################################################



t_AirtableBase = Table(
    'AirtableBase', metadata,
    Column('AirtableBaseID', Integer, nullable=False, server_default=text("0")),
    Column('AirtableBase', String(50, 'Latin1_General_BIN')),
    Column('BuySheetURL', String(100, 'Latin1_General_BIN')),
    Column('M3ListsURL', String(100, 'Latin1_General_BIN'))
)


t_AirtableBase2 = Table(
    'AirtableBase2', metadata,
    Column('AirtableID', Integer, nullable=False),
    Column('AirtableBase', String(50, 'Latin1_General_BIN')),
    Column('BuySheetURL', String(100, 'Latin1_General_BIN')),
    Column('M3ListsURL', String(100, 'Latin1_General_BIN'))
)


t_Brand_Supplement_Data = Table(
    'Brand_Supplement_Data', metadata,
    Column('M3 Brand Code', String(50, 'Latin1_General_BIN')),
    Column('Brand Type', String(50, 'Latin1_General_BIN')),
    Column('Margin', String(50, 'Latin1_General_BIN')),
    Column('Cost', String(50, 'Latin1_General_BIN'))
)


t_Calendar = Table(
    'Calendar', metadata,
    Column('CalendarDate', DateTime, nullable=False)
)


t_Cost120days = Table(
    'Cost120days', metadata,
    Column('startdate', DateTime),
    Column('Warehouse', String(10, 'Latin1_General_BIN')),
    Column('ITEM', String(20, 'Latin1_General_BIN')),
    Column('COST120', DECIMAL(18, 2))
)


class Date(SAFRSBase, Base):
    __tablename__ = 'Dates'

    dt = Column(Date, primary_key=True)
    d = Column(Integer, Computed('(datepart(day,[dt]))', persisted=False))
    y = Column(Integer, Computed('(datepart(year,[dt]))', persisted=False))
    q = Column(Integer, Computed('(datepart(quarter,[dt]))', persisted=False))
    m = Column(Integer, Computed('(datepart(month,[dt]))', persisted=False))
    fm = Column(DateTime, Computed('(dateadd(month,datediff(month,(0),[dt]),(0)))', persisted=False))
    w = Column(Integer, Computed('(datepart(week,[dt]))', persisted=False))
    wd = Column(Integer, Computed('(datepart(weekday,[dt]))', persisted=False))
    mn = Column(Unicode(30), Computed('(datename(month,[dt]))', persisted=False))
    s101 = Column(String(10, 'Latin1_General_BIN'), Computed('(CONVERT([char](10),[dt],(101)))', persisted=False))
    s103 = Column(String(10, 'Latin1_General_BIN'), Computed('(CONVERT([char](10),[dt],(103)))', persisted=False))
    s112 = Column(String(8, 'Latin1_General_BIN'), Computed('(CONVERT([char](8),[dt],(112)))', persisted=False), index=True)
    s112 = Column(String(8, 'Latin1_General_BIN'), index=True) # , Computed('(CONVERT([char](8),[dt],(112)))', persisted=False))
    allow_client_generated_ids = True


class EXTAPPSUPPLIERBRANDDISCOUNT(SAFRSBase, Base):
    __tablename__ = 'EXTAPP_SUPPLIER_BRAND_DISCOUNTS'
    __table_args__ = (
        Index('IX_EXTAPP_SUPPLIER_BRAND_DISCOUNTS', 'SUNO', 'ITCL', unique=True),
    )

    SupplierBrandDiscountID = Column(Integer, primary_key=True, server_default=text("0"))
    SUNO = Column(NCHAR(10), nullable=False)
    ITCL = Column(NCHAR(10), nullable=False)
    DISCOUNT = Column(DECIMAL(10, 2), nullable=False)
    Deleted = Column(Boolean, nullable=False, server_default=text("((0))"))
    CreatedTime = Column(NCHAR(15))
    USID = Column(NCHAR(10))
    ModifiedTime = Column(NCHAR(15))
    ModifiedUSID = Column(NCHAR(10))


t_EXTAPP_USERPREFIX = Table(
    'EXTAPP_USERPREFIX', metadata,
    Column('USID', Unicode(10), nullable=False),
    Column('PREFIX', String(5, 'Latin1_General_BIN'), nullable=False)
)


t_Minimum_Stock_Levels = Table(
    'Minimum_Stock_Levels', metadata,
    Column('Item SKU', String(50, 'Latin1_General_BIN')),
    Column('100', String(50, 'Latin1_General_BIN')),
    Column('200', String(50, 'Latin1_General_BIN')),
    Column('210', String(50, 'Latin1_General_BIN')),
    Column('300', String(50, 'Latin1_General_BIN')),
    Column('303', String(50, 'Latin1_General_BIN')),
    Column('310', String(50, 'Latin1_General_BIN')),
    Column('400', String(50, 'Latin1_General_BIN')),
    Column('410', String(50, 'Latin1_General_BIN')),
    Column('411', String(50, 'Latin1_General_BIN')),
    Column('600', String(50, 'Latin1_General_BIN'))
)


t_PRGP = Table(
    'PRGP', metadata,
    Column('MMITNO', Integer),
    Column('MMPRGP', String(255, 'Latin1_General_BIN'))
)


t_PRGP2 = Table(
    'PRGP2', metadata,
    Column('MMITNO', String(255, 'Latin1_General_BIN')),
    Column('MMPRGP', String(255, 'Latin1_General_BIN'))
)


t_PRGP3 = Table(
    'PRGP3', metadata,
    Column('MMTPLI', Integer),
    Column('HMSTYN', String(255, 'Latin1_General_BIN'))
)


t_PRGP4 = Table(
    'PRGP4', metadata,
    Column('PRTPLI', Integer),
    Column('PRSTYN', String(255, 'Latin1_General_BIN'))
)


t_PRGP5 = Table(
    'PRGP5', metadata,
    Column('MMITNO', String(255, 'Latin1_General_BIN')),
    Column('MMCFI1', String(255, 'Latin1_General_BIN'))
)


t_Perth_Last_7_Days_Sales_Y2 = Table(
    'Perth_Last_7_Days_Sales_Y2', metadata,
    Column('Store ID', String(50, 'Latin1_General_BIN')),
    Column('Store', String(50, 'Latin1_General_BIN')),
    Column('M3 item code', String(50, 'Latin1_General_BIN')),
    Column('Qty', String(50, 'Latin1_General_BIN'))
)


class SOH(SAFRSBase, Base):
    __tablename__ = 'SOH'

    SOHDate = Column(DateTime, primary_key=True, nullable=False)
    Brand = Column(String(20, 'Latin1_General_BIN'))
    Gender = Column(String(15, 'Latin1_General_BIN'))
    ItemType = Column(String(250, 'Latin1_General_BIN'))
    Warehouse = Column(String(6, 'Latin1_General_BIN'), primary_key=True, nullable=False)
    Item = Column(String(20, 'Latin1_General_BIN'), primary_key=True, nullable=False)
    RunningQty = Column(DECIMAL(10, 2))
    Seqno = Column(Integer)
    allow_client_generated_ids = True

'''
t_Storessales20190416_20190423(2) = Table(
    'Storessales20190416-20190423(2)', metadata,
    Column('GL_ARTICLE', String(55, 'Latin1_General_BIN')),
    Column('Store ID', String(55, 'Latin1_General_BIN')),
    Column('GA_CHARLIBRE2', String(55, 'Latin1_General_BIN')),
    Column('M3 item code', String(55, 'Latin1_General_BIN')),
    Column('Qty', Integer)
)


class Date(SAFRSBase, Base):
    __tablename__ = '_Dates'

    d = Column(Date, primary_key=True)
    allow_client_generated_ids = True


t_product-variant-soh-20190423 = Table(
    'product-variant-soh-20190423', metadata,
    Column('id', String(55, 'Latin1_General_BIN')),
    Column('product_id', String(55, 'Latin1_General_BIN')),
    Column('qty_brisbane', Integer),
    Column('qty_chadstone', Integer),
    Column('qty_melbourne', Integer),
    Column('qty_parramatta', Integer),
    Column('qty_perth', Integer),
    Column('qty_southport', Integer),
    Column('qty_sydney', Integer),
    Column('qty_goldcoast', Integer),
    Column('qty_warehouse', Integer)
)


t_productvariantsoh-20190423 = Table(
    'productvariantsoh-20190423', metadata,
    Column('id', String(55, 'Latin1_General_BIN')),
    Column('product_id', String(55, 'Latin1_General_BIN')),
    Column('qty_brisbane', Integer),
    Column('qty_chadstone', Integer),
    Column('qty_melbourne', Integer),
    Column('qty_parramatta', Integer),
    Column('qty_perth', Integer),
    Column('qty_southport', Integer),
    Column('qty_sydney', Integer),
    Column('qty_goldcoast', Integer),
    Column('qty_warehouse', Integer)
)
'''

class RelatedCustomerOrder(SAFRSBase, Base):
    __tablename__ = 'related_customer_orders'

    customer_order_no = Column(Unicode(70))
    related_customer_order_no = Column(Unicode(70))
    related_key = Column(Unicode(70))
    ID = Column(Integer, primary_key=True, server_default=text("0"))


class RelatedCustomerOrdersKey(SAFRSBase, Base):
    __tablename__ = 'related_customer_orders_keys'

    ID = Column(Integer, primary_key=True, server_default=text("0"))
    customer_order_no = Column(Unicode(70))
    related_key = Column(Unicode(70))


t_y2_orderdates_salesperson = Table(
    'y2_orderdates_salesperson', metadata,
    Column('y2_order_number_m3_format', Unicode(70)),
    Column('y2_order_date', Date),
    Column('y2_sales_person', Unicode(211)),
    Column('y2_r02_identifier', Unicode(21)),
    Column('y2_revenue_inclu_gst', Numeric(19, 6))
)


# from database import customize_models