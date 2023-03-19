create table main.CategoryTableNameTest
(
    Id           INTEGER
        primary key,
    CategoryName VARCHAR(8000),
    Description  VARCHAR(8000),
    Client_id    INTEGER
);

create table main.Customer
(
    Id               VARCHAR(8000)
        primary key,
    CompanyName      VARCHAR(8000),
    ContactName      VARCHAR(8000),
    ContactTitle     VARCHAR(8000),
    Address          VARCHAR(8000),
    City             VARCHAR(8000),
    Region           VARCHAR(8000),
    PostalCode       VARCHAR(8000),
    Country          VARCHAR(8000),
    Phone            VARCHAR(8000),
    Fax              VARCHAR(8000),
    Balance          Decimal,
    CreditLimit      Decimal,
    OrderCount       INT default 0,
    UnpaidOrderCount INT default 0,
    Client_id        INTEGER
);

create table main.CustomerDemographic
(
    Id           VARCHAR(8000)
        primary key,
    CustomerDesc VARCHAR(8000)
);

create table main.Department
(
    Id             INTEGER
        constraint Department_pk
            primary key autoincrement,
    DepartmentId   INTEGER
        constraint HeadDepartment
            references main.Department
            on update cascade on delete cascade,
    DepartmentName varchar(100)
);

create table main.Location
(
    country varchar(50),
    city    varchar(50),
    notes   varchar(256),
    constraint City_pk
        primary key (country, city)
);

create table main.Product
(
    Id              INTEGER
        primary key,
    ProductName     VARCHAR(8000),
    SupplierId      INTEGER not null,
    CategoryId      INTEGER not null,
    QuantityPerUnit VARCHAR(8000),
    UnitPrice       DECIMAL not null,
    UnitsInStock    INTEGER not null,
    UnitsOnOrder    INTEGER not null,
    ReorderLevel    INTEGER not null,
    Discontinued    INTEGER not null,
    UnitsShipped    INTEGER
);

create table main.Region
(
    Id                INTEGER
        primary key,
    RegionDescription VARCHAR(8000)
);

create table main.SampleDBVersion
(
    Id    INTEGER
        constraint SampleDBVersion_pk
            primary key autoincrement,
    Notes varchar(800)
);

create table main.Shipper
(
    Id          INTEGER
        primary key,
    CompanyName VARCHAR(8000),
    Phone       VARCHAR(8000)
);

create table main.Supplier
(
    Id           INTEGER
        primary key,
    CompanyName  VARCHAR(8000),
    ContactName  VARCHAR(8000),
    ContactTitle VARCHAR(8000),
    Address      VARCHAR(8000),
    City         VARCHAR(8000),
    Region       VARCHAR(8000),
    PostalCode   VARCHAR(8000),
    Country      VARCHAR(8000),
    Phone        VARCHAR(8000),
    Fax          VARCHAR(8000),
    HomePage     VARCHAR(8000)
);

create table main.Territory
(
    Id                   VARCHAR(8000)
        primary key,
    TerritoryDescription VARCHAR(8000),
    RegionId             INTEGER not null
);

create table main."Union"
(
    Id   INTEGER
        constraint Union_pk
            primary key autoincrement,
    Name varchar(80)
);

create table main.Employee
(
    Id                   INTEGER
        primary key,
    LastName             VARCHAR(8000),
    FirstName            VARCHAR(8000),
    Title                VARCHAR(8000),
    TitleOfCourtesy      VARCHAR(8000),
    BirthDate            VARCHAR(8000),
    HireDate             VARCHAR(8000),
    Address              VARCHAR(8000),
    City                 VARCHAR(8000),
    Region               VARCHAR(8000),
    PostalCode           VARCHAR(8000),
    Country              VARCHAR(8000),
    HomePhone            VARCHAR(8000),
    Extension            VARCHAR(8000),
    Notes                VARCHAR(8000),
    ReportsTo            INTEGER,
    PhotoPath            VARCHAR(8000),
    EmployeeType         varchar(16) default Salaried,
    Salary               Decimal,
    WorksForDepartmentId INTEGER
        references main.Department
            on update cascade on delete set null,
    OnLoanDepartmentId   INTEGER
        references main.Department
            on update cascade on delete set null,
    UnionId              INTEGER
        constraint Employee_Union_Id_fk
            references main."Union",
    Dues                 Decimal
);

create index main.Employee_ReportsTo_index
    on main.Employee (ReportsTo);

create table main.EmployeeAudit
(
    Id         INTEGER
        constraint Employee_Audit_pk
            primary key autoincrement,
    Title      varchar,
    Salary     Decimal,
    LastName   Varchar,
    FirstName  varchar,
    EmployeeId INTEGER
        constraint EmployeeAudit_Employee_Id_fk
            references main.Employee,
    CreatedOn  TEXT
);

create table main.EmployeeTerritory
(
    Id          VARCHAR(8000)
        primary key,
    EmployeeId  INTEGER not null
        references main.Employee,
    TerritoryId VARCHAR(8000)
        references main.Territory
);

create table main."Order"
(
    Id               INTEGER
        primary key autoincrement,
    CustomerId       VARCHAR(8000) not null
        references main.Customer,
    EmployeeId       INTEGER       not null
        references main.Employee,
    OrderDate        VARCHAR(8000),
    RequiredDate     date,
    ShippedDate      VARCHAR(8000),
    ShipVia          INTEGER,
    Freight          DECIMAL default 0,
    ShipName         VARCHAR(8000),
    ShipAddress      VARCHAR(8000),
    ShipCity         VARCHAR(8000),
    ShipRegion       VARCHAR(8000),
    ShipPostalCode   VARCHAR(8000),
    ShipCountry      VARCHAR(8000),
    AmountTotal      Decimal(10, 2),
    Country          varchar(50),
    City             varchar(50),
    Ready            BOOLEAN default TRUE,
    OrderDetailCount INTEGER default 0,
    CloneFromOrder   INTEGER
        constraint Order_Order_Id_fk
            references main."Order",
    foreign key (Country, City) references main.Location
        on update cascade on delete set null
);

create index main.Order_CustomerId_index
    on main."Order" (CustomerId);

create index main.Order_EmployeeId_index
    on main."Order" (EmployeeId);

create table main.OrderDetail
(
    Id          INTEGER
        primary key autoincrement,
    OrderId     INTEGER           not null
        references main."Order"
            on delete cascade,
    ProductId   INTEGER           not null
        references main.Product,
    UnitPrice   DECIMAL,
    Quantity    INTEGER default 1 not null,
    Discount    DOUBLE  default 0,
    Amount      Decimal,
    ShippedDate VARCHAR(8000)
);

create index main.OrderDetail_OrderId_index
    on main.OrderDetail (OrderId);

create index main.OrderDetail_ProductId_index
    on main.OrderDetail (ProductId);

create table main.sqlite_master
(
    type     TEXT,
    name     TEXT,
    tbl_name TEXT,
    rootpage INT,
    sql      TEXT
);

create table main.sqlite_sequence
(
    name,
    seq
);

