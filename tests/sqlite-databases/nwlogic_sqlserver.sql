create table dbo.CategoryTableNameTest
(
    Id           INTEGER
        primary key,
    CategoryName VARCHAR(8000),
    Description  VARCHAR(8000),
    Client_id    INTEGER
);

create table dbo.Customer
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

create table dbo.CustomerDemographic
(
    Id           VARCHAR(8000)
        primary key,
    CustomerDesc VARCHAR(8000)
);

create table dbo.Department
(
    Id             INTEGER
        constraint Department_pk
            primary key identity,
    DepartmentId   INTEGER
        constraint HeadDepartment
            references dbo.Department
            /* on update cascade on delete cascade */ ,
    DepartmentName varchar(100)
);

create table dbo.Location
(
    country varchar(50),
    city    varchar(50),
    notes   varchar(256),
    constraint City_pk
        primary key (country, city)
);

create table dbo.Product
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

create table dbo.Region
(
    Id                INTEGER
        primary key,
    RegionDescription VARCHAR(8000)
);

create table dbo.SampleDBVersion
(
    Id    INTEGER
        constraint SampleDBVersion_pk
            primary key identity,
    Notes varchar(800)
);

create table dbo.Shipper
(
    Id          INTEGER
        primary key,
    CompanyName VARCHAR(8000),
    Phone       VARCHAR(8000)
);

create table dbo.Supplier
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

create table dbo.Territory
(
    Id                   VARCHAR(8000)
        primary key,
    TerritoryDescription VARCHAR(8000),
    RegionId             INTEGER not null
);

create table dbo."Union"
(
    Id   INTEGER
        constraint Union_pk
            primary key identity,
    Name varchar(80)
);

create table dbo.Employee
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
    EmployeeType         varchar(16),
    Salary               Decimal,
    WorksForDepartmentId INTEGER
        references dbo.Department
            on update cascade on delete set null,
    OnLoanDepartmentId   INTEGER
        references dbo.Department
            on update cascade on delete set null,
    UnionId              INTEGER
        constraint Employee_Union_Id_fk
            references dbo."Union",
    Dues                 Decimal
);

/*
create index dbo.Employee_ReportsTo_index
    on dbo.Employee (ReportsTo);
*/


create table dbo.EmployeeAudit
(
    Id         INTEGER
        constraint Employee_Audit_pk
            primary key identity,
    Title      varchar,
    Salary     Decimal,
    LastName   Varchar,
    FirstName  varchar,
    EmployeeId INTEGER
        constraint EmployeeAudit_Employee_Id_fk
            references dbo.Employee,
    CreatedOn varchar(max)
);

create table dbo.EmployeeTerritory
(
    Id          VARCHAR(8000)
        primary key,
    EmployeeId  INTEGER not null
        references dbo.Employee,
    TerritoryId VARCHAR(8000)
        references dbo.Territory
);

create table dbo."Order"
(
    Id               INTEGER
        primary key identity,
    CustomerId       VARCHAR(8000) not null
        references dbo.Customer,
    EmployeeId       INTEGER       not null
        references dbo.Employee,
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
    Ready            bit default 1,
    OrderDetailCount INTEGER default 0,
    CloneFromOrder   INTEGER
        constraint Order_Order_Id_fk
            references dbo."Order",
    foreign key (Country, City) references dbo.Location
        on update cascade on delete set null
);

/*
create index dbo.Order_CustomerId_index
    on dbo."Order" (CustomerId);

create index dbo.Order_EmployeeId_index
    on dbo."Order" (EmployeeId);
*/

create table dbo.OrderDetail
(
    Id          INTEGER
        primary key identity,
    OrderId     INTEGER           not null
        references dbo."Order"
            on delete cascade,
    ProductId   INTEGER           not null
        references dbo.Product,
    UnitPrice   DECIMAL,
    Quantity    INTEGER default 1 not null,
    Discount    DECIMAL  default 0,
    Amount      Decimal,
    ShippedDate VARCHAR(8000)
);

/*
create index dbo.OrderDetail_OrderId_index
    on dbo.OrderDetail (OrderId);

create index dbo.OrderDetail_ProductId_index
    on dbo.OrderDetail (ProductId);
*/

/*

808 - not working
select Customer.Id, `Order`.* from `Order` left outer join Customer where `Order`.CustomerId = Customer.Id;

22 orphan Orders for DUMO, OCEA, QUEE
select `Order`.Id, `Order`.CustomerId,
       (select count(*) from Customer where `Order`.CustomerId = Customer.Id) as rowcount
from `Order`
where rowcount = 0;

Customer: 91, 91
Order:  830, 830   select count(*) from nwlogic.dbo.[Order];
orderDetail:  2155, 2155
Product:  77, 77

backup to: /var/opt/mssql/data/nwlogic-202316-17-50-13.bak
BACKUP DATABASE [nwlogic] TO  DISK = N'/var/opt/mssql/data/nwlogic-2023316-17-50-13.bak' WITH NOFORMAT, NOINIT,  NAME = N'nwlogic-Full-2023-03-17T00:50:13', NOSKIP, REWIND, NOUNLOAD,  STATS = 10
docker cp b5d1aed6408e:/var/opt/mssql/data/nwlogic-2023316-17-50-13.bak ~/Desktop/nwlogic-bkp.bak 
docker cp sqlsvr-container:/var/opt/mssql/data/nwlogic-2023316-17-50-13.bak ~/Desktop/nwlogic-bkp.bak 
docker cp sqlsvr-container:/var/opt/mssql/data/nwlogic.bak ~/Desktop/nwlogic-bkp.bak 
*/




