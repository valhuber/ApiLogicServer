## Problem Statement

Optimistic locking is a valuable feature for interactive systems, to **avoid update overwrites** and **maximize concurrency**, **without requiring special database columns**.

&nbsp;

### Constraints

Most systems operate under the following constraints:

1. **Maximize concurrency** by be eliminating long-duration locks
   * Rows cannot be locked (pessimistically) on read, _in case_ they are updated
2. **No special columns**, such as  `VersionNumber`
   * Database design is often constrained by other applications, or by internal standards
3. **Minimize network traffic** and keep client coding simple
   * E.g., unwieldy to send all "old" values back  

&nbsp;

### Avoid Update Overwrites

Within these constraints, the key objective is avoid overwriting updates.  Consider the following scenario:

| Time | User | Action |
|:----- |:-------|:----|
| T0 | U1 | Reads Row.Column with value V1  |
| T1 | U2 | Reads same row |
| T2 | U1 | Updates row with value V2 |
| T3 | U2 | Updates row with value V3 - V2 value overwritten, U1 not happy |

The objective, then, is to ***avoid overwriting U1's update***.

&nbsp;

### Optimistic Locking

A widely accepted solution is **optimistic locking:** 

1. On reads, no database locks are acquired
2. On update, ensure the row has not changed since the user read it

&nbsp;

## Approach: virtual `CheckSum` to detect changes

Before summarizing the approach, we note some key elements provided by architectural components.

&nbsp;

### Background: Key Architectural Elements

&nbsp;

#### 1. SAFRS `@jsonapi_attr`

SAFRS API provides adding derived virtual (non-stored) attributes: [`@jsonapi_attr`](https://github.com/thomaxxl/safrs/blob/master/examples/demo_pythonanywhere_com.py)
   * This enables the server to compute unstored values, here, `S_CheckSum`
   * SAFRS supports sending such values on client `patch` operations, so it is visible in logic

&nbsp;

#### 2. SQLAlchemy `loaded_as_persistent`

SQLAlchemy provides the `loaded_as_persistent` [event](https://docs.sqlalchemy.org/en/20/orm/events.html#sqlalchemy.orm.SessionEvents.loaded_as_persistent), enabling us to compute the `CheckSum`, store it in the row, so we can later check it on update.

&nbsp;

#### 3. The rules engine supports generic `before_logic`

This enables us to check the row compare `CheckSum` values before updates; see [`logic/declare_logic](https://github.com/ApiLogicServer/demo/blob/main/logic/declare_logic.py).  Note such logic has access to the about-to-be-updated row, and the old-row.

&nbsp;

### Creation options

You can configure optimistic locking when you create projects, with the following 2 CLI arguments:

1. `--opt_locking_attr` - this is the name of the attribute that contains the CheckSum.  It defaults to `S_CheckSum`

2. `--opt_locking` - select one of the following (default is *optional*):

| Option | Included on `Get` | Checked on `Patch` |
|:----- |:-------|:----|
| **ignored** | Never | Never |
| **optional** | Always | Yes - but no error if omitted |
| **required** | Always | Yes - error if omitted |

&nbsp;

### Configuration options

You can override the created `opt_locking` on server startup:

* by updating the Config file, and
* by using the `OPT_LOCKING` Env variable.

The options are the same as shown in the table above.

Note the env variables can be set on your IDE Run Configurations.

&nbsp;

### Processing Overview

The approach is summarized in the table below.  See the the code in [`api/system/opt_locking/opt_locking.py`](https://github.com/ApiLogicServer/demo/blob/main/api/system/opt_locking/opt_locking.py) for details.

&nbsp;

| Phase | Responsibility | Action | Notes |
|:-----|:-------|:-------|:----|
| Design Time | **System** | Declare <`opt_locking_attr`> as a `@jsonapi_attr` | Project creation (CLI) builds `models.py` with @json_attr |
| Runtime - Read | **System** | Compute Checksum | `opt_locking#loaded_as` (setup from from api_logic_server_run.py) |
| Runtime - Call Patch | **User** App Code,<br>Admin App | Return as-read-Checksum | See examples below |
| Runtime - Process Patch | **System** | Compare CheckSums: as-read vs. current | `opt_locking#opt_locking_patch`, via `logic/declare_logic.py`: generic before event |

&nbsp;

----
&nbsp;

## Exploring Optimistic Locking

You can explore this using the sample database with the the Admin App, or with the cURL commands below.

Use the `No Security` run config.

&nbsp;

### Category `Patch` - Missing S_Checksum passes

This should bypass optlock check and report "can't be x"

```
curl -X 'PATCH' \
  'http://localhost:5656/api/Category/1/' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": {
    "attributes": {
      "Description": "x"
    },
    "type": "Category",
    "id": "1"
  }
}'
```

&nbsp;

### Category `Patch` - Invalid S_Checksum raises exception

This should fail "Sorry, row altered by another user..."

```
curl -X 'PATCH' \
  'http://localhost:5656/api/Category/1/' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": {
    "attributes": {
      "Description": "x",
      "S_CheckSum": "Invalid S_Checksum raises exception"
    },
    "type": "Category",
    "id": "1"
  }
}'
```

&nbsp;

### Category 9 `Patch` valid S_CheckSum passes

This should bypass optlock check and report "can't be x"

```
curl -X 'PATCH' \
  'http://localhost:5656/api/Category/9/' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": {
    "attributes": {
      "Description": "x",
      "S_CheckSum": "83926768455664603"
    },
    "type": "Category",
    "id": "9"
  }
}'
```
&nbsp;


### Order 10643 Set Shipped (from null)

This case tests different attribute ordering (per alias attribute), resulting in different checksums.

Be sure to replace the db.sqlite after the test, since this changes it.

```
curl -X 'PATCH' \
  'http://localhost:5656/api/Order/10643/' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/json' \
  -d '{
  "data": {
    "attributes": {
        "RequiredDate": "2013-10-13",
        "Id": 10643
    },
    "type": "Order",
    "id": 10643
  }
}'
```

```
curl -X 'GET' \
  'http://localhost:5656/api/Order/10643/?include=parent%2COrderDetailList%2CCustomer%2CLocation%2CEmployee%2COrderList&fields%5BOrder%5D=ShipZip%2CId%2CCustomerId%2CEmployeeId%2COrderDate%2CRequiredDate%2CShippedDate%2CShipVia%2CFreight%2CShipName%2CShipAddress%2CShipCity%2CShipRegion%2CShipCountry%2CAmountTotal%2CCountry%2CCity%2CReady%2COrderDetailCount%2CCloneFromOrder%2C_check_sum_%2CCheckSum' \
  -H 'accept: application/vnd.api+json' \
  -H 'Content-Type: application/vnd.api+json'
```