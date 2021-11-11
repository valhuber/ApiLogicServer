# coding: utf-8
from sqlalchemy import Boolean, Column, DECIMAL, DateTime, Float, ForeignKey, ForeignKeyConstraint, Integer, LargeBinary, String, Table, Text, UniqueConstraint, text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.ext.declarative import declarative_base


########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
from safrs import SAFRSBase

import safrs
db = safrs.DB

# manually altered.  NB: no import database... at end

Base = db.Model
metadata = Base.metadata

NullType = db.String  # datatype fixup
TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.mysql import *

########################################################################################################################

## used to test --use_model (TBD)

class Category(SAFRSBase, Base):
    __tablename__ = 'Category'

    Id = Column(Integer, primary_key=True)
    CategoryName = Column(String(8000))
    Description = Column(String(8000))


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

    Department = relationship('Department', remote_side=[Id], cascade_backrefs=True, backref='DepartmentList')


class Location(SAFRSBase, Base):
    __tablename__ = 'Location'

    country = Column(String(50), primary_key=True, nullable=False)
    city = Column(String(50), primary_key=True, nullable=False)
    notes = Column(String(256))
    allow_client_generated_ids = True

class Product(SAFRSBase, Base):
    __tablename__ = 'Product'

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


t_ProductDetails_V = Table(
    'ProductDetails_V', metadata,
    Column('Id', Integer),
    Column('ProductName', String(8000)),
    Column('SupplierId', Integer),
    Column('CategoryId', Integer),
    Column('QuantityPerUnit', String(8000)),
    Column('UnitPrice', DECIMAL),
    Column('UnitsInStock', Integer),
    Column('UnitsOnOrder', Integer),
    Column('ReorderLevel', Integer),
    Column('Discontinued', Integer),
    Column('UnitsShipped', Integer),
    Column('CategoryName', String(8000)),
    Column('CategoryDescription', String(8000)),
    Column('SupplierName', String(8000)),
    Column('SupplierRegion', String(8000))
)


class Region(SAFRSBase, Base):
    __tablename__ = 'Region'

    Id = Column(Integer, primary_key=True)
    RegionDescription = Column(String(8000))


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

class AbPermission(SAFRSBase, Base):
    __tablename__ = 'ab_permission'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)


class AbRegisterUser(SAFRSBase, Base):
    __tablename__ = 'ab_register_user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256))
    email = Column(String(64), nullable=False)
    registration_date = Column(DateTime)
    registration_hash = Column(String(256))


class AbRole(SAFRSBase, Base):
    __tablename__ = 'ab_role'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, unique=True)


class AbUser(SAFRSBase, Base):
    __tablename__ = 'ab_user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(64), nullable=False)
    last_name = Column(String(64), nullable=False)
    username = Column(String(64), nullable=False, unique=True)
    password = Column(String(256))
    active = Column(Boolean)
    email = Column(String(64), nullable=False, unique=True)
    last_login = Column(DateTime)
    login_count = Column(Integer)
    fail_login_count = Column(Integer)
    created_on = Column(DateTime)
    changed_on = Column(DateTime)
    created_by_fk = Column(ForeignKey('ab_user.id'))
    changed_by_fk = Column(ForeignKey('ab_user.id'))

    parent = relationship('AbUser', remote_side=[id], primaryjoin='AbUser.changed_by_fk == AbUser.id', cascade_backrefs=True, backref='AbUserList')
    parent1 = relationship('AbUser', remote_side=[id], primaryjoin='AbUser.created_by_fk == AbUser.id', cascade_backrefs=True, backref='AbUserList_parent1')


class AbViewMenu(SAFRSBase, Base):
    __tablename__ = 'ab_view_menu'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False, unique=True)


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
    IsCommissioned = Column(Integer)
    Salary = Column(DECIMAL)
    WorksForDepartmentId = Column(ForeignKey('Department.Id'))
    OnLoanDepartmentId = Column(ForeignKey('Department.Id'))

    Department = relationship('Department', primaryjoin='Employee.OnLoanDepartmentId == Department.Id', cascade_backrefs=True, backref='EmployeeList')
    Department1 = relationship('Department', primaryjoin='Employee.WorksForDepartmentId == Department.Id', cascade_backrefs=True, backref='EmployeeList_Department1')


class AbPermissionView(SAFRSBase, Base):
    __tablename__ = 'ab_permission_view'
    __table_args__ = (
        UniqueConstraint('permission_id', 'view_menu_id'),
    )

    id = Column(Integer, primary_key=True)
    permission_id = Column(ForeignKey('ab_permission.id'))
    view_menu_id = Column(ForeignKey('ab_view_menu.id'))

    permission = relationship('AbPermission', cascade_backrefs=True, backref='AbPermissionViewList')
    view_menu = relationship('AbViewMenu', cascade_backrefs=True, backref='AbPermissionViewList')


class AbUserRole(SAFRSBase, Base):
    __tablename__ = 'ab_user_role'
    __table_args__ = (
        UniqueConstraint('user_id', 'role_id'),
    )

    id = Column(Integer, primary_key=True)
    user_id = Column(ForeignKey('ab_user.id'))
    role_id = Column(ForeignKey('ab_role.id'))

    role = relationship('AbRole', cascade_backrefs=True, backref='AbUserRoleList')
    user = relationship('AbUser', cascade_backrefs=True, backref='AbUserRoleList')


class EmployeeAudit(SAFRSBase, Base):
    __tablename__ = 'EmployeeAudit'

    Id = Column(Integer, primary_key=True)
    Title = Column(String)
    Salary = Column(DECIMAL)
    LastName = Column(String)
    FirstName = Column(String)
    EmployeeId = Column(ForeignKey('Employee.Id'))
    CreatedOn = Column(Text)

    Employee = relationship('Employee', cascade_backrefs=True, backref='EmployeeAuditList')


class EmployeeTerritory(SAFRSBase, Base):
    __tablename__ = 'EmployeeTerritory'

    Id = Column(String(8000), primary_key=True)
    EmployeeId = Column(ForeignKey('Employee.Id'), nullable=False)
    TerritoryId = Column(ForeignKey('Territory.Id'))
    allow_client_generated_ids = True
    Employee = relationship('Employee', cascade_backrefs=True, backref='EmployeeTerritoryList')
    Territory = relationship('Territory', cascade_backrefs=True, backref='EmployeeTerritoryList')


class Order(SAFRSBase, Base):
    __tablename__ = 'Order'
    __table_args__ = (
        ForeignKeyConstraint(['Country', 'City'], ['Location.country', 'Location.city']),
    )

    Id = Column(Integer, primary_key=True)
    CustomerId = Column(ForeignKey('Customer.Id'), index=True)
    EmployeeId = Column(ForeignKey('Employee.Id'), nullable=False, index=True)
    OrderDate = Column(String(8000))
    RequiredDate = Column(String(8000))
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

    Location = relationship('Location', cascade_backrefs=True, backref='OrderList')
    Customer = relationship('Customer', cascade_backrefs=True, backref='OrderList')
    Employee = relationship('Employee', cascade_backrefs=True, backref='OrderList')


class AbPermissionViewRole(SAFRSBase, Base):
    __tablename__ = 'ab_permission_view_role'
    __table_args__ = (
        UniqueConstraint('permission_view_id', 'role_id'),
    )

    id = Column(Integer, primary_key=True)
    permission_view_id = Column(ForeignKey('ab_permission_view.id'))
    role_id = Column(ForeignKey('ab_role.id'))

    permission_view = relationship('AbPermissionView', cascade_backrefs=True, backref='AbPermissionViewRoleList')
    role = relationship('AbRole', cascade_backrefs=True, backref='AbPermissionViewRoleList')


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

    Order = relationship('Order', cascade_backrefs=True, backref='OrderDetailList')
    Product = relationship('Product', cascade_backrefs=True, backref='OrderDetailList')

