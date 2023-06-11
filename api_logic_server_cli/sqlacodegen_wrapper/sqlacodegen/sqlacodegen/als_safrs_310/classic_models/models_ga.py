# coding: utf-8
from sqlalchemy import Column, DECIMAL, Date, ForeignKey, Integer, SmallInteger, String, Text
from sqlalchemy.sql.sqltypes import NullType
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# mypy: ignore-errors

from safrs import SAFRSBase
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *
########################################################################################################################



class Office(SAFRSBase, Base):
    __tablename__ = 'offices'
    _s_collection_name = 'Office'  # type: ignore
    __bind_key__ = 'None'

    officeCode = Column(String(10), primary_key=True)
    city = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50))
    state = Column(String(50))
    country = Column(String(50), nullable=False)
    postalCode = Column(String(15), nullable=False)
    territory = Column(String(10), nullable=False)
    allow_client_generated_ids = True

    EmployeeList = relationship('Employee', cascade_backrefs=True, backref='office')


class Productline(SAFRSBase, Base):
    __tablename__ = 'productlines'
    _s_collection_name = 'Productline'  # type: ignore
    __bind_key__ = 'None'

    productLine = Column(String(50), primary_key=True)
    textDescription = Column(String(4000))
    htmlDescription = Column(Text)
    image = Column(NullType)
    allow_client_generated_ids = True

    ProductList = relationship('Product', cascade_backrefs=True, backref='productline')


class Employee(SAFRSBase, Base):
    __tablename__ = 'employees'
    _s_collection_name = 'Employee'  # type: ignore
    __bind_key__ = 'None'

    employeeNumber = Column(Integer, primary_key=True)
    lastName = Column(String(50), nullable=False)
    firstName = Column(String(50), nullable=False)
    extension = Column(String(10), nullable=False)
    email = Column(String(100), nullable=False)
    officeCode = Column(ForeignKey('offices.officeCode'), nullable=False, index=True)
    reportsTo = Column(ForeignKey('employees.employeeNumber'), index=True)
    jobTitle = Column(String(50), nullable=False)

    # see backref on parent: office = relationship('Office', cascade_backrefs=True, backref='EmployeeList')
    # see backref on parent: parent = relationship('Employee', remote_side=[employeeNumber], cascade_backrefs=True, backref='EmployeeList')

    parent = relationship('Employee', remote_side=[employeeNumber], cascade_backrefs=True, backref='EmployeeList')  # special handling for self-relationships
    CustomerList = relationship('Customer', cascade_backrefs=True, backref='employee')


class Product(SAFRSBase, Base):
    __tablename__ = 'products'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    productCode = Column(String(15), primary_key=True)
    productName = Column(String(70), nullable=False)
    productLine = Column(ForeignKey('productlines.productLine'), nullable=False, index=True)
    productScale = Column(String(10), nullable=False)
    productVendor = Column(String(50), nullable=False)
    productDescription = Column(Text, nullable=False)
    quantityInStock = Column(SmallInteger, nullable=False)
    buyPrice = Column(DECIMAL(10, 2), nullable=False)
    MSRP = Column(DECIMAL(10, 2), nullable=False)
    allow_client_generated_ids = True

    # see backref on parent: productline = relationship('Productline', cascade_backrefs=True, backref='ProductList')

    OrderdetailList = relationship('Orderdetail', cascade_backrefs=True, backref='product')


class Customer(SAFRSBase, Base):
    __tablename__ = 'customers'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    customerNumber = Column(Integer, primary_key=True)
    customerName = Column(String(50), nullable=False)
    contactLastName = Column(String(50), nullable=False)
    contactFirstName = Column(String(50), nullable=False)
    phone = Column(String(50), nullable=False)
    addressLine1 = Column(String(50), nullable=False)
    addressLine2 = Column(String(50))
    city = Column(String(50), nullable=False)
    state = Column(String(50))
    postalCode = Column(String(15))
    country = Column(String(50), nullable=False)
    salesRepEmployeeNumber = Column(ForeignKey('employees.employeeNumber'), index=True)
    creditLimit = Column(DECIMAL(10, 2))

    # see backref on parent: employee = relationship('Employee', cascade_backrefs=True, backref='CustomerList')

    OrderList = relationship('Order', cascade_backrefs=True, backref='customer')
    PaymentList = relationship('Payment', cascade_backrefs=True, backref='customer')


class Order(SAFRSBase, Base):
    __tablename__ = 'orders'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    orderNumber = Column(Integer, primary_key=True)
    orderDate = Column(Date, nullable=False)
    requiredDate = Column(Date, nullable=False)
    shippedDate = Column(Date)
    status = Column(String(15), nullable=False)
    comments = Column(Text)
    customerNumber = Column(ForeignKey('customers.customerNumber'), nullable=False, index=True)

    # see backref on parent: customer = relationship('Customer', cascade_backrefs=True, backref='OrderList')

    OrderdetailList = relationship('Orderdetail', cascade_backrefs=True, backref='order')


class Payment(SAFRSBase, Base):
    __tablename__ = 'payments'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    customerNumber = Column(ForeignKey('customers.customerNumber'), primary_key=True, nullable=False)
    checkNumber = Column(String(50), primary_key=True, nullable=False)
    paymentDate = Column(Date, nullable=False)
    amount = Column(DECIMAL(10, 2), nullable=False)
    allow_client_generated_ids = True

    # see backref on parent: customer = relationship('Customer', cascade_backrefs=True, backref='PaymentList')


class Orderdetail(SAFRSBase, Base):
    __tablename__ = 'orderdetails'
    _s_collection_name = 'Orderdetail'  # type: ignore
    __bind_key__ = 'None'

    orderNumber = Column(ForeignKey('orders.orderNumber'), primary_key=True, nullable=False)
    productCode = Column(ForeignKey('products.productCode'), primary_key=True, nullable=False, index=True)
    quantityOrdered = Column(Integer, nullable=False)
    priceEach = Column(DECIMAL(10, 2), nullable=False)
    orderLineNumber = Column(SmallInteger, nullable=False)
    allow_client_generated_ids = True

    # see backref on parent: order = relationship('Order', cascade_backrefs=True, backref='OrderdetailList')
    # see backref on parent: product = relationship('Product', cascade_backrefs=True, backref='OrderdetailList')
