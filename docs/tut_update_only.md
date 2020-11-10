---
id: tut_update_only
title: Processing - Update only
sidebar_label: Processing - Update only
---



### create table in delta

```sql
create table default.tgt_update_only (id int, c1 string, c2 string)
```

### insert data into table

```yaml
version: 1
job:
  type: processing
source:
  endpoint: hive
  incremental: false
  properties:
    sql: |-
      select 1 id, 'a' c1, 'b' c2 union all
      select 2 id, 'a' c1, 'b' c2 union all
      select 3 id, 'a' c1, 'b' c2 union all
      select 4 id, 'a' c1, 'b' c2 
target:
  primary_key_columns:
    - id
  operation: merge
  soft_delete: false
  properties:
    template: default
    table: tgt_update_only
  endpoint: hive
```

### perform update only with merged column

```yaml
version: 1
job:
  type: processing
source:
  endpoint: hive
  incremental: false
  properties:
    sql: |-
      select 1 id, 'a' c1, 'b' c2 union all
      select 2 id, 'a233' c1, 'b23' c2 union all
      select 3 id, 'a' c1, 'b' c2 union all
      select 5 id, 'a' c1, 'b' c2 union all
      select 4 id, 'a233' c1, 'b23' c2 
target:
  primary_key_columns:
    - id
  operation: update_only
  soft_delete: false
  properties:
    template: default
    table: tgt_update_only
  endpoint: hive
  merge_columns:
    - c1
```

### perform update only without merged column

```yaml
version: 1
job:
  type: processing
source:
  endpoint: hive
  incremental: false
  properties:
    sql: |-
      select 1 id, 'a' c1, 'b' c2 union all
      select 2 id, 'a233' c1, 'b23' c2 union all
      select 3 id, 'a' c1, 'b' c2 union all
      select 5 id, 'a' c1, 'b' c2 union all
      select 4 id, 'a233' c1, 'b23' c2 
target:
  primary_key_columns:
    - id
  operation: update_only
  soft_delete: false
  properties:
    template: default
    table: tgt_update_only
  endpoint: hive
```