# coding: utf-8
from sqlalchemy import Boolean, Column, DECIMAL, Date, Float, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


########################################################################################################################
# Classes describing database for SqlAlchemy ORM.
########################################################################################################################

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 
Base = declarative_base()
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *
########################################################################################################################



class Category(Base):
    __tablename__ = 'CategoryTableNameTest'
    _s_collection_name = 'Category'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    CategoryName = Column('CategoryName_ColumnName', String(8000))  # logical name
    Description = Column(String(8000))
    Client_id = Column(Integer)


class Customer(Base):
    __tablename__ = 'Customer'
    _s_collection_name = 'Customer'
    __bind_key__ = 'None'

    Id = Column(String(8000), primary_key=True)
    CompanyName = Column(String(8000))
    ContactName = Column(String(8000))
    ContactTitle = Column(String(8000))
    Address = Column(String(8000))
    City = Column(String(8000))
    Region = Column(String(8000))
    PostalCode = Column(String(8000))
    Country = Column(String(8000))
    Phone = Column(String(8000))
    Fax = Column(String(8000))
    Balance = Column(DECIMAL)
    CreditLimit = Column(DECIMAL)
    OrderCount = Column(Integer, server_default=text("0"))
    UnpaidOrderCount = Column(Integer, server_default=text("0"))
    Client_id = Column(Integer)
    allow_client_generated_ids = True

    OrderList = relationship('Order', cascade_backrefs=False, backref='Customer')


class CustomerDemographic(Base):
    __tablename__ = 'CustomerDemographic'
    _s_collection_name = 'CustomerDemographic'
    __bind_key__ = 'None'

    Id = Column(String(8000), primary_key=True)
    CustomerDesc = Column(String(8000))
    allow_client_generated_ids = True


class Department(Base):
    __tablename__ = 'Department'
    _s_collection_name = 'Department'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    DepartmentId = Column(ForeignKey('Department.Id'))
    DepartmentName = Column(String(100))

    # see backref on parent: Department = relationship('Department', remote_side=[Id], cascade_backrefs=False, backref='DepartmentList')

    Department = relationship('Department', remote_side=[Id], cascade_backrefs=False, backref='DepartmentList')  # special handling for self-relationships
    EmployeeList = relationship('Employee', primaryjoin='Employee.OnLoanDepartmentId == Department.Id', cascade_backrefs=False, backref='Department')
    EmployeeList1 = relationship('Employee', primaryjoin='Employee.WorksForDepartmentId == Department.Id', cascade_backrefs=False, backref='Department1')


class Location(Base):
    __tablename__ = 'Location'
    _s_collection_name = 'Location'
    __bind_key__ = 'None'

    country = Column(String(50), primary_key=True)
    city = Column(String(50), primary_key=True)
    notes = Column(String(256))
    allow_client_generated_ids = True

    OrderList = relationship('Order', cascade_backrefs=False, backref='Location')


class Product(Base):
    __tablename__ = 'Product'
    _s_collection_name = 'Product'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    ProductName = Column(String(8000))
    SupplierId = Column(Integer, nullable=False)
    CategoryId = Column(Integer, nullable=False)
    QuantityPerUnit = Column(String(8000))
    UnitPrice = Column(DECIMAL, nullable=False)
    UnitsInStock = Column(Integer, nullable=False)
    UnitsOnOrder = Column(Integer, nullable=False)
    ReorderLevel = Column(Integer, nullable=False)
    Discontinued = Column(Integer, nullable=False)
    UnitsShipped = Column(Integer)

    OrderDetailList = relationship('OrderDetail', cascade_backrefs=False, backref='Product')


class Region(Base):
    __tablename__ = 'Region'
    _s_collection_name = 'Region'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    RegionDescription = Column(String(8000))


class SampleDBVersion(Base):
    __tablename__ = 'SampleDBVersion'
    _s_collection_name = 'SampleDBVersion'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    Notes = Column(String(800))


class Shipper(Base):
    __tablename__ = 'Shipper'
    _s_collection_name = 'Shipper'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    CompanyName = Column(String(8000))
    Phone = Column(String(8000))


class Supplier(Base):
    __tablename__ = 'Supplier'
    _s_collection_name = 'Supplier'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    CompanyName = Column(String(8000))
    ContactName = Column(String(8000))
    ContactTitle = Column(String(8000))
    Address = Column(String(8000))
    City = Column(String(8000))
    Region = Column(String(8000))
    ShipZip = Column('ShipPostalCode', String(8000))  # manual fix - alias
    Country = Column(String(8000))
    Phone = Column(String(8000))
    Fax = Column(String(8000))
    HomePage = Column(String(8000))


class Territory(Base):
    __tablename__ = 'Territory'
    _s_collection_name = 'Territory'
    __bind_key__ = 'None'

    Id = Column(String(8000), primary_key=True)
    TerritoryDescription = Column(String(8000))
    RegionId = Column(Integer, nullable=False)
    allow_client_generated_ids = True

    EmployeeTerritoryList = relationship('EmployeeTerritory', cascade_backrefs=False, backref='Territory')


class Union(Base):
    __tablename__ = 'Union'
    _s_collection_name = 'Union'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    Name = Column(String(80))

    EmployeeList = relationship('Employee', cascade_backrefs=False, backref='Union')


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Employee(Base):
    __tablename__ = 'Employee'
    _s_collection_name = 'Employee'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    LastName = Column(String(8000))
    FirstName = Column(String(8000))
    Title = Column(String(8000))
    TitleOfCourtesy = Column(String(8000))
    BirthDate = Column(String(8000))
    HireDate = Column(String(8000))
    Address = Column(String(8000))
    City = Column(String(8000))
    Region = Column(String(8000))
    PostalCode = Column(String(8000))
    Country = Column(String(8000))
    HomePhone = Column(String(8000))
    Extension = Column(String(8000))
    Notes = Column(String(8000))
    ReportsTo = Column(Integer, index=True)
    PhotoPath = Column(String(8000))
    EmployeeType = Column(String(16), server_default=text("Salaried"))
    Salary = Column(DECIMAL)
    WorksForDepartmentId = Column(ForeignKey('Department.Id'))
    OnLoanDepartmentId = Column(ForeignKey('Department.Id'))
    UnionId = Column(ForeignKey('Union.Id'))
    Dues = Column(DECIMAL)

    # see backref on parent: Department = relationship('Department', primaryjoin='Employee.OnLoanDepartmentId == Department.Id', cascade_backrefs=False, backref='EmployeeList')
    # see backref on parent: Union = relationship('Union', cascade_backrefs=False, backref='EmployeeList')
    # see backref on parent: Department1 = relationship('Department', primaryjoin='Employee.WorksForDepartmentId == Department.Id', cascade_backrefs=False, backref='EmployeeList_Department1')

    EmployeeAuditList = relationship('EmployeeAudit', cascade_backrefs=False, backref='Employee')
    EmployeeTerritoryList = relationship('EmployeeTerritory', cascade_backrefs=False, backref='Employee')
    OrderList = relationship('Order', cascade_backrefs=False, backref='Employee')


class EmployeeAudit(Base):
    __tablename__ = 'EmployeeAudit'
    _s_collection_name = 'EmployeeAudit'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    Title = Column(String)
    Salary = Column(DECIMAL)
    LastName = Column(String)
    FirstName = Column(String)
    EmployeeId = Column(ForeignKey('Employee.Id'))
    CreatedOn = Column(Text)

    # see backref on parent: Employee = relationship('Employee', cascade_backrefs=False, backref='EmployeeAuditList')


class EmployeeTerritory(Base):
    __tablename__ = 'EmployeeTerritory'
    _s_collection_name = 'EmployeeTerritory'
    __bind_key__ = 'None'

    Id = Column(String(8000), primary_key=True)
    EmployeeId = Column(ForeignKey('Employee.Id'), nullable=False)
    TerritoryId = Column(ForeignKey('Territory.Id'))
    allow_client_generated_ids = True

    # see backref on parent: Employee = relationship('Employee', cascade_backrefs=False, backref='EmployeeTerritoryList')
    # see backref on parent: Territory = relationship('Territory', cascade_backrefs=False, backref='EmployeeTerritoryList')


class Order(Base):
    __tablename__ = 'Order'
    _s_collection_name = 'Order'
    __bind_key__ = 'None'
    __table_args__ = (
        ForeignKeyConstraint(['Country', 'City'], ['Location.country', 'Location.city']),
    )

    Id = Column(Integer, primary_key=True)
    CustomerId = Column(ForeignKey('Customer.Id'), nullable=False, index=True)
    EmployeeId = Column(ForeignKey('Employee.Id'), nullable=False, index=True)
    OrderDate = Column(String(8000))
    RequiredDate = Column(Date)
    ShippedDate = Column(String(8000))
    ShipVia = Column(Integer)
    Freight = Column(DECIMAL, server_default=text("0"))
    ShipName = Column(String(8000))
    ShipAddress = Column(String(8000))
    ShipCity = Column(String(8000))
    ShipRegion = Column(String(8000))
    ShipZip = Column('ShipPostalCode', String(8000))  # manual fix - alias
    ShipCountry = Column(String(8000))
    AmountTotal = Column(DECIMAL(10, 2))
    Country = Column(String(50))
    City = Column(String(50))
    Ready = Column(Boolean, server_default=text("TRUE"))
    OrderDetailCount = Column(Integer, server_default=text("0"))
    CloneFromOrder = Column(ForeignKey('Order.Id'))

    # see backref on parent: parent = relationship('Order', remote_side=[Id], cascade_backrefs=False, backref='OrderList')
    # see backref on parent: Location = relationship('Location', cascade_backrefs=False, backref='OrderList')
    # see backref on parent: Customer = relationship('Customer', cascade_backrefs=False, backref='OrderList')
    # see backref on parent: Employee = relationship('Employee', cascade_backrefs=False, backref='OrderList')

    parent = relationship('Order', remote_side=[Id], cascade_backrefs=False, backref='OrderList')  # special handling for self-relationships
    OrderDetailList = relationship('OrderDetail', cascade='all, delete', cascade_backrefs=False, backref='Order')  # manual fix


class OrderDetail(Base):
    __tablename__ = 'OrderDetail'
    _s_collection_name = 'OrderDetail'
    __bind_key__ = 'None'

    Id = Column(Integer, primary_key=True)
    OrderId = Column(ForeignKey('Order.Id'), nullable=False, index=True)
    ProductId = Column(ForeignKey('Product.Id'), nullable=False, index=True)
    UnitPrice = Column(DECIMAL)
    Quantity = Column(Integer, server_default=text("1"), nullable=False)
    Discount = Column(Float, server_default=text("0"))
    Amount = Column(DECIMAL)
    ShippedDate = Column(String(8000))

    # see backref on parent: Order = relationship('Order', cascade_backrefs=False, backref='OrderDetailList')
    # see backref on parent: Product = relationship('Product', cascade_backrefs=False, backref='OrderDetailList')
