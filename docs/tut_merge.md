---
id: tut_merge
title: Processing - merge
sidebar_label: Processing - merge
---



### create table in delta

```sql
create table default.tgt_merge (id int, c1 string, c2 string)
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
    table: tgt_merge
    pre_sql:
      - truncate table default.tgt_merge
  endpoint: hive
```

### perform merge with merged column

- only column c1 will be updated

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
  operation: merge
  soft_delete: false
  properties:
    template: default
    table: tgt_merge
  endpoint: hive
  merge_columns:
    - c1
```

### perform merge without merged column

- both column c1 and c2 will be updated

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
  operation: merge
  soft_delete: false
  properties:
    template: default
    table: tgt_merge
  endpoint: hive
```