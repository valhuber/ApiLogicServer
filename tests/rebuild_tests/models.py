# coding: utf-8
from sqlalchemy import Boolean, Column, DECIMAL, Date, Float, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, String, Table, Text, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
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

from sqlalchemy.dialects.mysql import *
########################################################################################################################



class Category(SAFRSBase, Base):
    __tablename__ = 'Category'

    Id = Column(Integer, primary_key=True)
    CategoryName = Column(String(8000))
    Description = Column(String(8000))
    NewAttribute = Column(String(8000))

    ProductList = relationship('Product', cascade_backrefs=True, backref='Category')


class CategoryNew(SAFRSBase, Base):
    __tablename__ = 'CategoryNew'

    Id = Column(Integer, primary_key=True)
    Name = Column(String(8000))
    Description = Column(String(8000))
    # NewCol = Column(String(8000))


class Customer(SAFRSBase, Base):
    __tablename__ = 'Customer'

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
    allow_client_generated_ids = True

    OrderList = relationship('Order', cascade_backrefs=True, backref='Customer')


class CustomerDemographic(SAFRSBase, Base):
    __tablename__ = 'CustomerDemographic'

    Id = Column(String(8000), primary_key=True)
    CustomerDesc = Column(String(8000))
    allow_client_generated_ids = True


class Department(SAFRSBase, Base):
    __tablename__ = 'Department'

    Id = Column(Integer, primary_key=True)
    DepartmentId = Column(ForeignKey('Department.Id'))
    DepartmentName = Column(String(100))

    # see backref on parent: Department = relationship('Department', remote_side=[Id], cascade_backrefs=True, backref='DepartmentList')

    Department = relationship('Department', remote_side=[Id], cascade_backrefs=True, backref='DepartmentList')  # special handling for self-relationships
    EmployeeList = relationship('Employee', primaryjoin='Employee.OnLoanDepartmentId == Department.Id', cascade_backrefs=True, backref='Department')
    EmployeeList1 = relationship('Employee', primaryjoin='Employee.WorksForDepartmentId == Department.Id', cascade_backrefs=True, backref='Department1')


class Location(SAFRSBase, Base):
    __tablename__ = 'Location'

    country = Column(String(50), primary_key=True)
    city = Column(String(50), primary_key=True)
    notes = Column(String(256))
    allow_client_generated_ids = True

    OrderList = relationship('Order', cascade_backrefs=True, backref='Location')


class Product(SAFRSBase, Base):
    __tablename__ = 'Product'

    Id = Column(Integer, primary_key=True)
    ProductName = Column(String(8000))
    SupplierId = Column(Integer, nullable=False)
    CategoryId = Column(ForeignKey('Category.Id'))
    QuantityPerUnit = Column(String(8000))
    UnitPrice = Column(DECIMAL, nullable=False)
    UnitsInStock = Column(Integer, nullable=False)
    UnitsOnOrder = Column(Integer, nullable=False)
    ReorderLevel = Column(Integer, nullable=False)
    Discontinued = Column(Integer, nullable=False)
    UnitsShipped = Column(Integer)

    OrderDetailList = relationship('OrderDetail', cascade_backrefs=True, backref='Product')


class Region(SAFRSBase, Base):
    __tablename__ = 'Region'

    Id = Column(Integer, primary_key=True)
    RegionDescription = Column(String(8000))


class SampleDBVersion(SAFRSBase, Base):
    __tablename__ = 'SampleDBVersion'

    Id = Column(Integer, primary_key=True)
    Notes = Column(String(800))


class Shipper(SAFRSBase, Base):
    __tablename__ = 'Shipper'

    Id = Column(Integer, primary_key=True)
    CompanyName = Column(String(8000))
    Phone = Column(String(8000))


class Supplier(SAFRSBase, Base):
    __tablename__ = 'Supplier'

    Id = Column(Integer, primary_key=True)
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
    HomePage = Column(String(8000))


class Territory(SAFRSBase, Base):
    __tablename__ = 'Territory'

    Id = Column(String(8000), primary_key=True)
    TerritoryDescription = Column(String(8000))
    RegionId = Column(Integer, nullable=False)
    allow_client_generated_ids = True

    EmployeeTerritoryList = relationship('EmployeeTerritory', cascade_backrefs=True, backref='Territory')


class Union(SAFRSBase, Base):
    __tablename__ = 'Union'

    Id = Column(Integer, primary_key=True)
    Name = Column(String(80))

    EmployeeList = relationship('Employee', cascade_backrefs=True, backref='Union')


t_sqlite_sequence = Table(
    'sqlite_sequence', metadata,
    Column('name', NullType),
    Column('seq', NullType)
)


class Employee(SAFRSBase, Base):
    __tablename__ = 'Employee'

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
    Photo = Column(LargeBinary)
    Notes = Column(String(8000))
    ReportsTo = Column(Integer, index=True)
    PhotoPath = Column(String(8000))
    EmployeeType = Column(String(16), server_default=text("Salaried"))
    Salary = Column(DECIMAL)
    WorksForDepartmentId = Column(ForeignKey('Department.Id'))
    OnLoanDepartmentId = Column(ForeignKey('Department.Id'))
    UnionId = Column(ForeignKey('Union.Id'))
    Dues = Column(DECIMAL)

    # see backref on parent: Department = relationship('Department', primaryjoin='Employee.OnLoanDepartmentId == Department.Id', cascade_backrefs=True, backref='EmployeeList')
    # see backref on parent: Union = relationship('Union', cascade_backrefs=True, backref='EmployeeList')
    # see backref on parent: Department1 = relationship('Department', primaryjoin='Employee.WorksForDepartmentId == Department.Id', cascade_backrefs=True, backref='EmployeeList_Department1')

    EmployeeAuditList = relationship('EmployeeAudit', cascade_backrefs=True, backref='Employee')
    EmployeeTerritoryList = relationship('EmployeeTerritory', cascade_backrefs=True, backref='Employee')
    OrderList = relationship('Order', cascade_backrefs=True, backref='Employee')


class EmployeeAudit(SAFRSBase, Base):
    __tablename__ = 'EmployeeAudit'

    Id = Column(Integer, primary_key=True)
    Title = Column(String)
    Salary = Column(DECIMAL)
    LastName = Column(String)
    FirstName = Column(String)
    EmployeeId = Column(ForeignKey('Employee.Id'))
    CreatedOn = Column(Text)

    # see backref on parent: Employee = relationship('Employee', cascade_backrefs=True, backref='EmployeeAuditList')


class EmployeeTerritory(SAFRSBase, Base):
    __tablename__ = 'EmployeeTerritory'

    Id = Column(String(8000), primary_key=True)
    EmployeeId = Column(ForeignKey('Employee.Id'), nullable=False)
    TerritoryId = Column(ForeignKey('Territory.Id'))
    allow_client_generated_ids = True

    # see backref on parent: Employee = relationship('Employee', cascade_backrefs=True, backref='EmployeeTerritoryList')
    # see backref on parent: Territory = relationship('Territory', cascade_backrefs=True, backref='EmployeeTerritoryList')


class Order(SAFRSBase, Base):
    __tablename__ = 'Order'
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
    Freight = Column(DECIMAL, nullable=False)
    ShipName = Column(String(8000))
    ShipAddress = Column(String(8000))
    ShipCity = Column(String(8000))
    ShipRegion = Column(String(8000))
    ShipPostalCode = Column(String(8000))
    ShipCountry = Column(String(8000))
    AmountTotal = Column(DECIMAL(10, 2))
    Country = Column(String(50))
    City = Column(String(50))
    Ready = Column(Boolean, server_default=text("TRUE"))
    OrderDetailCount = Column(Integer, server_default=text("0"))
    CloneFromOrder = Column(ForeignKey('Order.Id'))

    # see backref on parent: parent = relationship('Order', remote_side=[Id], cascade_backrefs=True, backref='OrderList')
    # see backref on parent: Location = relationship('Location', cascade_backrefs=True, backref='OrderList')
    # see backref on parent: Customer = relationship('Customer', cascade_backrefs=True, backref='OrderList')
    # see backref on parent: Employee = relationship('Employee', cascade_backrefs=True, backref='OrderList')

    parent = relationship('Order', remote_side=[Id], cascade_backrefs=True, backref='OrderList')  # special handling for self-relationships
    OrderDetailList = relationship('OrderDetail', cascade='all, delete', cascade_backrefs=True, backref='Order')  # manual fix


class OrderDetail(SAFRSBase, Base):
    __tablename__ = 'OrderDetail'

    Id = Column(Integer, primary_key=True)
    OrderId = Column(ForeignKey('Order.Id'), nullable=False, index=True)
    ProductId = Column(ForeignKey('Product.Id'), nullable=False, index=True)
    UnitPrice = Column(DECIMAL, nullable=False)
    Quantity = Column(Integer, nullable=False)
    Discount = Column(Float, nullable=False)
    Amount = Column(DECIMAL)
    ShippedDate = Column(String(8000))

    # see backref on parent: Order = relationship('Order', cascade_backrefs=True, backref='OrderDetailList')
    # see backref on parent: Product = relationship('Product', cascade_backrefs=True, backref='OrderDetailList')


from database import customize_models
