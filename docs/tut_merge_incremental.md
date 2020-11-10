---
id: tut_merge_incremental
title: Processing - Merge Incremental Option
sidebar_label: Processing - Merge Incremental Option
---



### create table in delta

```sql
create table default.tgt_merge_not_incremental (id int, c1 string, c2 string, w_current_record_flag string)
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
  additional_columns:
    - name: w_current_record_flag
      framework_column: w_current_record_flag
target:
  primary_key_columns:
    - id
  operation: merge
  soft_delete: false
  properties:
    template: default
    table: tgt_merge_not_incremental
    history_columns:
      - c1
      - c2
  endpoint: hive

```

### perform merge without incremental

```yaml
version: 1
job:
  type: processing
source:
  endpoint: hive
  incremental: false
  properties:
    sql: |-

      select 2 id, 'a1' c1, 'b' c2 union all
      select 3 id, 'a' c1, 'b' c2 union all
      select 5 id, 'a' c1, 'b' c2 union all
      select 4 id, 'a1' c1, 'b' c2 
  additional_columns:
    - name: w_current_record_flag
      framework_column: w_current_record_flag
target:
  primary_key_columns:
    - id
  operation: merge
  soft_delete: false
  properties:
    template: default
    table: tgt_merge_not_incremental
    history_columns:
      - c1
      - c2
  endpoint: hive

```

### perform merge with incremental

```yaml
version: 1
job:
  type: processing
source:
  endpoint: hive
  incremental: true
  properties:
    sql: |-

      select 6 id, 'a12' c1, 'b' c2 union all
      select 3 id, 'a' c1, 'b' c2 union all
      select 5 id, 'a' c1, 'b' c2 union all
      select 4 id, 'a1' c1, 'b' c2 
  additional_columns:
    - name: w_current_record_flag
      framework_column: w_current_record_flag
target:
  primary_key_columns:
    - id
  operation: merge
  soft_delete: false
  properties:
    template: default
    table: tgt_merge_not_incremental
    history_columns:
      - c1
      - c2
  endpoint: hive

```