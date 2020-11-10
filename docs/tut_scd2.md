---
id: tut_scd2
title: Processing - SCD2
sidebar_label: Processing - SCD2
---


## scd2 test

### create table in delta

```sql
use default;
create table tgt_scd2 (id int, c1 string, c2 string, eff_start_dt timestamp, eff_end_dt timestamp, curr_rec string, seq_key bigint);
--truncate table  tgt_scd2;
--insert into tgt_scd2 select  -1,null,null,current_timestamp, null,'Y',0;
 select * from   tgt_scd2
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
    - name: eff_start_dt
      framework_column: w_eff_start_date_ts
      framework_generated: true
    - name: eff_end_dt
      framework_column: w_eff_end_date_ts
      framework_generated: true
    - name: curr_rec
      framework_column: w_current_record_flag
      framework_generated: true
    - name: seq_key
      framework_column: w_sequence_key
      framework_generated: true
target:
  primary_key_columns:
    - id
  operation: effective_date_merge
  soft_delete: false
  properties:
    template: default
    table: tgt_scd2
    history_columns:
      - c1
      - c2
  endpoint: hive
```

### perform scd2

```
version: 1
job:
  type: processing
source:
  endpoint: hive
  incremental: false
  properties:
    sql: |-
      select 1 id, 'a' c1, 'b' c2 union all
      select 2 id, 'a1' c1, 'b' c2 union all
      select 3 id, 'a' c1, 'b' c2 union all
      select 4 id, 'a1' c1, 'b' c2 
  additional_columns:
    - name: eff_start_dt
      framework_column: w_eff_start_date_ts
      framework_generated: true
    - name: eff_end_dt
      framework_column: w_eff_end_date_ts
      framework_generated: true
    - name: curr_rec
      framework_column: w_current_record_flag
      framework_generated: true
    - name: seq_key
      framework_column: w_sequence_key
      framework_generated: true
target:
  primary_key_columns:
    - id
  operation: effective_date_merge
  soft_delete: false
  properties:
    template: default
    table: tgt_scd2
    history_columns:
      - c1
      - c2
  endpoint: hive
```