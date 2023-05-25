## Problem Statement

Optimistic locking is a valuable feature for interactive systems with typical constraints:

1. Rows cannot be locked (pessimistically) on read, _in case_ they are updated
   * This would drastically decrease performance by making users wait on locks, so undesirable
2. Database design cannot tolerate new `VersionNumber` columns
3. Minimize network traffic and keep client coding simple
   * E.g., unwieldy to send all "old" values back  

Consider the scenario:

| Time | User | Action |
|:----- |:-------|:----|
| T0 | U1 | Reads Row.Column with value V1  |
| T1 | U2 | Reads same row |
| T2 | U1 | Updates row with value V2 |
| T3 | U2 | Updates row with value V3 - V2 value overwritten, U1 not happy |

A widely accepted solution is **optimistic locking:** 

> No read locks; on update, ensure the row has not changed since the user read it

&nbsp;

## Approach: `CheckSum` to detect changes

Before summarizing the approach, we note some key elements provided by architectural components.

&nbsp;

### Key Architectural Elements

&nbsp;

#### 1. SAFRS `@jsonapi_attr`

SAFRS API provides add derived attribute: [`@jsonapi_attr`](https://github.com/thomaxxl/safrs/blob/master/examples/demo_pythonanywhere_com.py)
   * This enables the server to compute unstored values, here, `CheckSum`
   * SAFRS supports client `patch` operations

&nbsp;

#### 2. SQLAlchemy `loaded_as_persistent`

SQLAlchemy provides the `loaded_as_persistent` [event](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.loaded_as_persistent), enabling us to compute the `CheckSum`, store it in the row, so can later check it on update.

&nbsp;

#### 3. The rules engine supports generic `before_logic`

This enables us to check the row compare `CheckSum` values; see [`declare_logic](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/project_prototype/logic/declare_logic.py).

&nbsp;

### Approach

The approach is summarized in the table below.  See the the code in [`api/system/opt_locking/opt_locking.py`](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/project_prototype/api/system/opt_locking/opt_locking.py) for details.

&nbsp;

| Phase | Responsibility | Action | Notes |
|:-----|:-------|:-------|:----|
| Design Time | API Logic Server CLI | Declare Checksum | models.py - json_attr |
| Runtime - Read | System | Compute Checksum | opt_locking#loaded_as (from api_logic_server_run.py) |
| Runtime - Call Patch | Custom App Code<br>Admin App | Return as-read-Checksum | See examples below |
| Runtime - Process Patch | System | Compare CheckSums: as-read vs. current | opt_locking#opt_locking_patch, via logic: generic before event |

&nbsp;

### Status: working, but...

TODO failing, since **patch retrieves the row**, which sets (bad) CheckSum (reflects upd, eg, setShipped).

We expected to overwrite it with client as-read, but that's missing in behave tests

Also show on Admin App updates....

How does get event know it's patch (don't set cs) vs get (set cs)

&nbsp;

## Samples

You can explore this using the sample database with the cURL commands below.

&nbsp;

&nbsp;

### `Get`

Observe that `CheckSum` is returned:

```
curl -X 'GET' \
  'http://localhost:5656/api/Employee/5/?include=EmployeeAuditList%2CEmployeeTerritoryList%2COrderList%2CManager%2CDepartment%2CDepartment1%2CUnion%2CManages&fields%5BEmployee%5D=Id%2CLastName%2CFirstName%2CTitle%2CTitleOfCourtesy%2CBirthDate%2CHireDate%2CAddress%2CCity%2CRegion%2CPostalCode%2CCountry%2CHomePhone%2CExtension%2CNotes%2CReportsTo%2CPhotoPath%2CEmployeeType%2CSalary%2CWorksForDepartmentId%2COnLoanDepartmentId%2CUnionId%2CDues%2C_check_sum_%2CCheckSum%2C__proper_salary__%2CProperSalary' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/vnd.api+json'
```

&nbsp;

### `Patch`

**Important:** Admin App is not sending unchanged attributes; we must convince it to send the CheckSum.

To simulate the client:
1. Use cURL (note: this should fail with constraint violation):

```curl
curl -X 'PATCH' \
  'http://localhost:5656/api/Employee/5/' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {
        "attributes": {
            "Salary": 97000,
            "CheckSum": 6785985870086950264,
            "Proper_Salary": 50000,
            "Id": 5},
        "type": "Employee",
        "id": 5
    }
}'
```
&nbsp;

## Problem Statement

Optimistic locking is a valuable feature for interactive systems with typical constraints:

1. Rows cannot be locked (pessimistically) on read, _in case_ they are updated
   * This would drastically decrease performance by making users wait on locks, so undesirable
2. Database design cannot tolerate new `VersionNumber` columns
3. Minimize network traffic and keep client coding simple
   * E.g., unwieldy to send all "old" values back  

Consider the scenario:

| Time | User | Action |
|:----- |:-------|:----|
| T0 | U1 | Reads Row.Column with value V1  |
| T1 | U2 | Reads same row |
| T2 | U1 | Updates row with value V2 |
| T3 | U2 | Updates row with value V3 - V2 value overwritten, U1 not happy |

A widely accepted solution is **optimistic locking:** 

> No read locks; on update, ensure the row has not changed since the user read it

&nbsp;

## Approach: `CheckSum` to detect changes

Before summarizing the approach, we note some key elements provided by architectural components.

&nbsp;

### Key Architectural Elements

&nbsp;

#### 1. SAFRS `@jsonapi_attr`

SAFRS API provides add derived attribute: [`@jsonapi_attr`](https://github.com/thomaxxl/safrs/blob/master/examples/demo_pythonanywhere_com.py)
   * This enables the server to compute unstored values, here, `CheckSum`
   * SAFRS supports client `patch` operations

&nbsp;

#### 2. SQLAlchemy `loaded_as_persistent`

SQLAlchemy provides the `loaded_as_persistent` [event](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.loaded_as_persistent), enabling us to compute the `CheckSum`, store it in the row, so can later check it on update.

&nbsp;

#### 3. The rules engine supports generic `before_logic`

This enables us to check the row compare `CheckSum` values; see [`declare_logic](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/project_prototype/logic/declare_logic.py).

&nbsp;

### Approach

The approach is summarized in the table below.  See the the code in [`api/system/opt_locking/opt_locking.py`](https://github.com/valhuber/ApiLogicServer/blob/main/api_logic_server_cli/project_prototype/api/system/opt_locking/opt_locking.py) for details.

&nbsp;

| Phase | Responsibility | Action | Notes |
|:-----|:-------|:-------|:----|
| Design Time | API Logic Server CLI | Declare Checksum | models.py - json_attr |
| Runtime - Read | System | Compute Checksum | opt_locking#loaded_as (from api_logic_server_run.py) |
| Runtime - Call Patch | Custom App Code<br>Admin App | Return as-read-Checksum | See examples below |
| Runtime - Process Patch | System | Compare CheckSums: as-read vs. current | opt_locking#opt_locking_patch, via logic: generic before event |

&nbsp;

## Samples

You can explore this using the sample database with the cURL commands below.

&nbsp;

&nbsp;

### `Get`

Observe that `CheckSum` is returned:

```
curl -X 'GET' \
  'http://localhost:5656/api/Employee/5/?include=EmployeeAuditList%2CEmployeeTerritoryList%2COrderList%2CManager%2CDepartment%2CDepartment1%2CUnion%2CManages&fields%5BEmployee%5D=Id%2CLastName%2CFirstName%2CTitle%2CTitleOfCourtesy%2CBirthDate%2CHireDate%2CAddress%2CCity%2CRegion%2CPostalCode%2CCountry%2CHomePhone%2CExtension%2CNotes%2CReportsTo%2CPhotoPath%2CEmployeeType%2CSalary%2CWorksForDepartmentId%2COnLoanDepartmentId%2CUnionId%2CDues%2C_check_sum_%2CCheckSum%2C__proper_salary__%2CProperSalary' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/vnd.api+json'
```

&nbsp;

### `Patch`

**Important:** Admin App is not sending unchanged attributes; we must convince it to send the CheckSum.

To simulate the client:
1. Use cURL (note: this should fail with constraint violation):

```curl
curl -X 'PATCH' \
  'http://localhost:5656/api/Employee/5/' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {
        "attributes": {
            "Salary": 97000,
            "CheckSum": 6785985870086950264,
            "Proper_Salary": 50000,
            "Id": 5},
        "type": "Employee",
        "id": 5
    }
}'
```
&nbsp;

### `Patch` no CheckSum

**Important:** Admin App is not sending unchanged attributes; we must convince it to send the CheckSum.

To simulate the client:
1. Use cURL (note: this should fail with constraint violation):

```curl
curl -X 'PATCH' \
  'http://localhost:5656/api/Employee/5/' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -d '{
    "data": {
        "attributes": {
            "Salary": 97000,
            "Proper_Salary": 50000,
            "Id": 5},
        "type": "Employee",
        "id": 5
    }
}'
```
&nbsp;

