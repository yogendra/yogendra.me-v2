---
title: "YugabyteDB ♥️ Vault: Fun Times"
date: 2024-05-23T00:28:38+08:00
draft: false
---

I have been working with [YugabyteDB](https://yugabyte.com) for a while now. I am always experimenting with YugabyteDB + (something). Today, its [Vault](https://www.vaultproject.io/).

<!-- more -->

I have also worked on Vault for a bit and did a a [lightening talk](https://github.com/yogendra/vault-transform-demo) earlier this year. That talks was primarily around the data masking. But today, I was exploring the database secret engine.

For the uninitiated, Vault provides you with ability to dynamically generate database credentials for your application. It does this by leveraging the simple RBAC SQLs provided by the database engine. It supports variety of databases including [Postgres](https://developer.hashicorp.com/vault/docs/secrets/databases/postgresql), and YugabyteDB by compatibility.

## What triggered this post?

One of the things that I encountered working with Vault was failing to cleanup the old credentials due to timeouts. On looking into vault code, I saw that the automatically generated queries tries to find all the privileges on user through introspection. One of these queries can be really slow if you have large number of database users created.

```sql
SELECT DISTINCT table_schema FROM information_schema.role_column_grants WHERE grantee='....';"
```

Lets look at the query plan ([visualize](https://www.pgexplain.dev/plan/aa278626-2d23-4993-a065-40c8237bfebe)):

```sql
yugabyte=# EXPLAIN ANALYZE SELECT DISTINCT table_schema FROM information_schema.role_column_grants WHERE grantee='v-token-approle--Bp1TDJdp645o0K8gHmqp-1716386830';
                                                                                                            QUERY PLAN

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Unique  (cost=1025.94..1027.20 rows=251 width=32) (actual time=10538.331..10538.331 rows=0 loops=1)
   ->  Sort  (cost=1025.94..1026.57 rows=251 width=32) (actual time=10538.329..10538.329 rows=0 loops=1)
         Sort Key: ((nc.nspname)::information_schema.sql_identifier)
         Sort Method: quicksort  Memory: 25kB
         ->  Nested Loop  (cost=944.18..1015.94 rows=251 width=32) (actual time=10538.307..10538.307 rows=0 loops=1)
               Join Filter: ((pg_has_role(u_grantor.oid, 'USAGE'::text) OR pg_has_role(pg_authid.oid, 'USAGE'::text) OR (pg_authid.rolname = 'PUBLIC'::name)) AND ((has
hed SubPlan 1) OR (hashed SubPlan 2)))
               ->  Nested Loop  (cost=724.18..763.38 rows=120 width=136) (actual time=761.744..7273.274 rows=9780 loops=1)
                     ->  Nested Loop  (cost=724.18..744.98 rows=120 width=72) (actual time=761.405..4018.709 rows=9780 loops=1)
                           ->  HashAggregate  (cost=724.18..725.38 rows=120 width=177) (actual time=761.064..766.771 rows=9780 loops=1)
                                 Group Key: pr_c.grantor, pr_c.grantee, a.attname, pr_c.relname, pr_c.relnamespace, pr_c.prtype, pr_c.grantable, pr_c.relowner
                                 ->  Append  (cost=16.50..721.78 rows=120 width=177) (actual time=25.204..755.990 rows=9780 loops=1)
                                       ->  Hash Join  (cost=16.50..635.50 rows=100 width=177) (actual time=25.202..28.599 rows=9774 loops=1)
                                             Hash Cond: (pr_c.oid = a.attrelid)
                                             ->  Subquery Scan on pr_c  (cost=0.00..615.00 rows=200 width=117) (actual time=7.796..9.656 rows=1086 loops=1)
                                                   Filter: (pr_c.prtype = ANY ('{INSERT,SELECT,UPDATE,REFERENCES}'::text[]))
                                                   Rows Removed by Filter: 678
                                                   ->  Result  (cost=0.00..465.00 rows=10000 width=117) (actual time=7.791..9.245 rows=1764 loops=1)
                                                         ->  ProjectSet  (cost=0.00..165.00 rows=10000 width=108) (actual time=7.784..8.774 rows=1764 loops=1)
                                                               ->  Seq Scan on pg_class  (cost=0.00..105.00 rows=1000 width=108) (actual time=7.755..8.038 rows=212 loops=1)
                                                                     Filter: (relkind = ANY ('{r,v,f,p}'::"char"[]))
                                                                     Rows Removed by Filter: 135
                                             ->  Hash  (cost=15.25..15.25 rows=100 width=68) (actual time=17.359..17.359 rows=2137 loops=1)
                                                   Buckets: 4096 (originally 1024)  Batches: 1 (originally 1)  Memory Usage: 241kB
                                                   ->  Index Scan using pg_attribute_relid_attnum_index on pg_attribute a  (cost=0.00..15.25 rows=100 width=68) (actual time=9.298..16.561 rows=2137 loops=1)
                                                         Index Cond: (attnum > 0)
                                                         Remote Filter: (NOT attisdropped)
                                       ->  Nested Loop  (cost=0.00..84.48 rows=20 width=177) (actual time=245.590..725.759 rows=6 loops=1)
                                             ->  Subquery Scan on pr_a  (cost=0.00..79.08 rows=20 width=109) (actual time=245.222..723.723 rows=6 loops=1)
                                                   Filter: (pr_a.prtype = ANY ('{INSERT,SELECT,UPDATE,REFERENCES}'::text[]))
                                                   ->  Result  (cost=0.00..64.08 rows=1000 width=109) (actual time=245.220..723.717 rows=6 loops=1)
                                                         ->  ProjectSet  (cost=0.00..34.08 rows=1000 width=100) (actual time=245.216..723.710 rows=6 loops=1)
                                                               ->  Nested Loop  (cost=0.00..28.08 rows=100 width=104) (actual time=7.824..720.093 rows=2137 loops=1)
                                                                     ->  Index Scan using pg_attribute_relid_attnum_index on pg_attribute a_1  (cost=0.00..15.25 rows=1 00 width=100) (actual time=7.012..8.463 rows=2137 loops=1)
                                                                           Index Cond: (attnum > 0)
                                                                           Remote Filter: (NOT attisdropped)
                                                                     ->  Index Scan using pg_class_oid_index on pg_class cc  (cost=0.00..0.15 rows=1 width=8) (actual time=0.327..0.327 rows=1 loops=2137)
                                                                           Index Cond: (oid = a_1.attrelid)
                                             ->  Index Scan using pg_class_oid_index on pg_class c  (cost=0.00..0.32 rows=1 width=76) (actual time=0.334..0.334 rows=1 loops=6)
                                                   Index Cond: (oid = pr_a.attrelid)
                                                   Filter: (relkind = ANY ('{r,v,f,p}'::"char"[]))
                           ->  Index Scan using pg_namespace_oid_index on pg_namespace nc  (cost=0.00..0.14 rows=1 width=68) (actual time=0.327..0.327 rows=1 loops=9780)
                                 Index Cond: (oid = pr_c.relnamespace)
                     ->  Index Scan using pg_authid_oid_index on pg_authid u_grantor  (cost=0.00..0.14 rows=1 width=68) (actual time=0.327..0.327 rows=1 loops=9780)
                           Index Cond: (oid = pr_c.grantor)
               ->  Append  (cost=0.00..0.20 rows=2 width=68) (actual time=0.333..0.333 rows=0 loops=9780)
                     ->  Index Scan using pg_authid_oid_index on pg_authid  (cost=0.00..0.16 rows=1 width=68) (actual time=0.327..0.327 rows=0 loops=9780)
                           Index Cond: (oid = pr_c.grantee)
                           Filter: (((rolname)::information_schema.sql_identifier)::text = 'v-token-approle--Bp1TDJdp645o0K8gHmqp-1716386830'::text)
                           Rows Removed by Filter: 1
                     ->  Subquery Scan on "*SELECT* 2"  (cost=0.01..0.03 rows=1 width=68) (actual time=0.000..0.000 rows=0 loops=9780)
                           Filter: (pr_c.grantee = "*SELECT* 2".oid)
                           ->  Result  (cost=0.01..0.01 rows=1 width=68) (actual time=0.000..0.000 rows=0 loops=9780)
                                 One-Time Filter: ((('PUBLIC'::character varying)::information_schema.sql_identifier)::text = 'v-token-approle--Bp1TDJdp645o0K8gHmqp-1716386830'::text)
               SubPlan 1
                 ->  Seq Scan on pg_authid a_2  (cost=0.00..107.50 rows=1000 width=32) (never executed)
                       Filter: pg_has_role(oid, 'USAGE'::text)
               SubPlan 2
                 ->  Seq Scan on pg_authid a_3  (cost=0.00..107.50 rows=1000 width=32) (never executed)
                       Filter: pg_has_role(oid, 'USAGE'::text)
 Planning Time: 3.016 ms
 Execution Time: 10538.738 ms
 Peak Memory Usage: 5583 kB
 ```

We can change this to use cost based optimizer. Lets look at that query plan ([visualize](https://www.pgexplain.dev/plan/f50c98a6-3cac-42d1-942d-1f2e0eb9911d))

```sql
yugabyte=# set yb_enable_base_scans_cost_model=on;
yugabyte=# EXPLAIN ANALYZE SELECT DISTINCT table_schema FROM information_schema.role_column_grants WHERE grantee='v-token-approle--Bp1TDJdp645o0K8gHmqp-1716386830';
                                                                                                                   QUERY PLAN

------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
 Unique  (cost=5322.60..5324.90 rows=461 width=32) (actual time=423.430..423.430 rows=0 loops=1)
   ->  Sort  (cost=5322.60..5323.75 rows=461 width=32) (actual time=423.429..423.429 rows=0 loops=1)
         Sort Key: ((nc.nspname)::information_schema.sql_identifier)
         Sort Method: quicksort  Memory: 25kB
         ->  Hash Join  (cost=4195.81..5302.20 rows=461 width=32) (actual time=423.423..423.423 rows=0 loops=1)
               Hash Cond: (x.grantor = u_grantor.oid)
               Join Filter: ((pg_has_role(u_grantor.oid, 'USAGE'::text) OR pg_has_role(pg_authid.oid, 'USAGE'::text) OR (pg_authid.rolname = 'PUBLIC'::name)) AND ((hashed SubPlan 1) OR (hashed SubPlan 2)))
               ->  Nested Loop  (cost=2586.82..3680.29 rows=1101 width=136) (actual time=422.699..422.699 rows=0 loops=1)
                     Join Filter: (x.grantee = pg_authid.oid)
                     Rows Removed by Join Filter: 9780
                     ->  Merge Join  (cost=2582.12..3124.06 rows=220 width=72) (actual time=418.664..420.096 rows=9780 loops=1)
                           Merge Cond: (nc.oid = x.relnamespace)
                           ->  Index Scan using pg_namespace_oid_index on pg_namespace nc  (cost=4.71..540.86 rows=1000 width=68) (actual time=0.634..0.637 rows=4 loops=1)
                           ->  Sort  (cost=2577.41..2577.96 rows=220 width=12) (actual time=418.025..418.340 rows=9780 loops=1)
                                 Sort Key: x.relnamespace
                                 Sort Method: quicksort  Memory: 843kB
                                 ->  Subquery Scan on x  (cost=2564.45..2568.85 rows=220 width=12) (actual time=414.694..416.964 rows=9780 loops=1)
                                       ->  HashAggregate  (cost=2564.45..2566.65 rows=220 width=177) (actual time=414.694..416.041 rows=9780 loops=1)
                                             Group Key: pr_c.grantor, pr_c.grantee, a.attname, pr_c.relname, pr_c.relnamespace, pr_c.prtype, pr_c.grantable, pr_c.relowner
                                             ->  Append  (cost=9.41..2560.05 rows=220 width=177) (actual time=2.695..410.859 rows=9780 loops=1)
                                                   ->  Nested Loop  (cost=9.41..666.35 rows=20 width=177) (actual time=2.694..401.406 rows=9774 loops=1)
                                                         ->  Subquery Scan on pr_c  (cost=4.71..548.44 rows=4 width=117) (actual time=1.960..4.298 rows=1086 loops=1)
                                                               Filter: (pr_c.prtype = ANY ('{INSERT,SELECT,UPDATE,REFERENCES}'::text[]))
                                                               Rows Removed by Filter: 678
                                                               ->  Result  (cost=4.71..545.44 rows=200 width=117) (actual time=1.959..3.808 rows=1764 loops=1)
                                                                     ->  ProjectSet  (cost=4.71..539.44 rows=200 width=108) (actual time=1.956..3.291 rows=1764 loops=1)
                                                                           ->  Seq Scan on pg_class  (cost=4.71..538.24 rows=20 width=108) (actual time=1.947..2.198 ro ws=212 loops=1)
                                                                                 Filter: (relkind = ANY ('{r,v,f,p}'::"char"[]))
                                                                                 Rows Removed by Filter: 135
                                                         ->  Index Scan using pg_attribute_relid_attnum_index on pg_attribute a  (cost=4.71..29.47 rows=1 width=68) (actual time=0.353..0.356 rows=9 loops=1086)
                                                               Index Cond: ((attrelid = pr_c.oid) AND (attnum > 0))
                                                               Remote Filter: (NOT attisdropped)
                                                   ->  Hash Join  (cost=1087.67..1890.40 rows=200 width=177) (actual time=6.023..8.451 rows=6 loops=1)
                                                         Hash Cond: (pr_a.attrelid = c.oid)
                                                         ->  Subquery Scan on pr_a  (cost=549.49..1350.59 rows=200 width=109) (actual time=4.802..7.230 rows=6 loops=1)
                                                               Filter: (pr_a.prtype = ANY ('{INSERT,SELECT,UPDATE,REFERENCES}'::text[]))
                                                               ->  Result  (cost=549.49..1200.59 rows=10000 width=109) (actual time=4.801..7.228 rows=6 loops=1)
                                                                     ->  ProjectSet  (cost=549.49..900.59 rows=10000 width=100) (actual time=4.800..7.225 rows=6 loops=1)
                                                                           ->  Hash Join  (cost=549.49..840.59 rows=1000 width=104) (actual time=4.255..6.523 rows=2137 loops=1)
                                                                                 Hash Cond: (a_1.attrelid = cc.oid)
                                                                                 ->  Index Scan using pg_attribute_relid_attnum_index on pg_attribute a_1  (cost=4.71..287.62 rows=1000 width=100) (actual time=3.184..5.148 rows=2137 loops=1)
                                                                                       Index Cond: (attnum > 0)
                                                                                       Remote Filter: (NOT attisdropped)
                                                                                 ->  Hash  (cost=532.28..532.28 rows=1000 width=8) (actual time=1.060..1.060 rows=347 loops=1)
                                                                                       Buckets: 1024  Batches: 1  Memory Usage: 22kB
                                                                                       ->  Seq Scan on pg_class cc  (cost=4.71..532.28 rows=1000 width=8) (actual time=0.951..1.022 rows=347 loops=1)
                                                         ->  Hash  (cost=537.93..537.93 rows=20 width=76) (actual time=1.206..1.206 rows=212 loops=1)
                                                               Buckets: 1024  Batches: 1  Memory Usage: 31kB
                                                               ->  Seq Scan on pg_class c  (cost=4.71..537.93 rows=20 width=76) (actual time=1.085..1.177 rows=212 loops=1)
                                                                     Filter: (relkind = ANY ('{r,v,f,p}'::"char"[]))
                                                                     Rows Removed by Filter: 135
                     ->  Materialize  (cost=4.71..536.44 rows=6 width=68) (actual time=0.000..0.000 rows=1 loops=9780)
                           ->  Append  (cost=4.71..536.41 rows=6 width=68) (actual time=0.391..0.392 rows=1 loops=1)
                                 ->  Seq Scan on pg_authid  (cost=4.71..536.36 rows=5 width=68) (actual time=0.390..0.390 rows=1 loops=1)
                                       Filter: (((rolname)::information_schema.sql_identifier)::text = 'v-token-approle--Bp1TDJdp645o0K8gHmqp-1716386830'::text)
                                       Rows Removed by Filter: 15
                                 ->  Result  (cost=0.01..0.01 rows=1 width=68) (actual time=0.001..0.001 rows=0 loops=1)
                                       One-Time Filter: ((('PUBLIC'::character varying)::information_schema.sql_identifier)::text = 'v-token-approle--Bp1TDJdp645o0K8gHmqp-1716386830'::text)
               ->  Hash  (cost=528.86..528.86 rows=1000 width=68) (actual time=0.718..0.718 rows=16 loops=1)
                     Buckets: 1024  Batches: 1  Memory Usage: 10kB
                     ->  Seq Scan on pg_authid u_grantor  (cost=4.71..528.86 rows=1000 width=68) (actual time=0.693..0.699 rows=16 loops=1)
               SubPlan 1
                 ->  Seq Scan on pg_authid a_2  (cost=4.71..532.98 rows=333 width=32) (never executed)
                       Filter: pg_has_role(oid, 'USAGE'::text)
               SubPlan 2
                 ->  Seq Scan on pg_authid a_3  (cost=4.71..532.98 rows=333 width=32) (never executed)
                       Filter: pg_has_role(oid, 'USAGE'::text)
 Planning Time: 44.508 ms
 Execution Time: 423.630 ms
 Peak Memory Usage: 7852 kB
(70 rows)
```

This is a huge improvement. We went from 10s+ to 400ms. Since this query is deep insides vault code, we can't change the query. But we can solve it. We have 2 options

1. Quick way to solve this is to just alter the vault db user (`vault_admin`) and set this flag

    ```sql
    alter role vault_admin set yb_enable_base_scans_cost_model=on;
    ```

2. Use custom revoke statement. This way you avoid the code path running this query, entirely. See the example of this in the instructions below

If you want to try this yourself, please follow the rest of the blog to understand how to setup and YugabyteDB and Vault to work together.

## Running YugabyteDB and Vault Together

> NOTE: There is a [YugabyteDB plugin for Vault](https://docs.yugabyte.com/preview/integrations/hashicorp-vault/), but its in dev preview at the moment, so lets just stick with PG Plugin

Lets jump into demo mode straight. I will be using a docker based setup. If you want to follow along and go through the whole process, just pull this docker compose file and launch it.

> ```bash
> wget https://gist.githubusercontent.com/yogendra/cc10b0f3b3918f3490b7fd672dc57c36/raw/docker-compose.yaml
> docker compose up -d
> docker compose exec shell bash -l
> ```

## Setup

Lets first check versions and connectivity. Starting with yugabytedb.

```bash
ysqlsh -c 'select version();'
```

Expected Output

```sql
                                                                                                                          version

-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
PostgreSQL 11.2-YB-2.20.3.1-b0 on aarch64-unknown-linux-gnu, compiled by clang version 16.0.6 (/opt/yb-build/llvm/yb-llvm-v16.0.6-yb-3-1695119965-1e6329f4-cent
os7-aarch64-build/src/llvm-project/clang 1e6329f40e5c531c09ade7015278078682293ebd), 64-bit
(1 row)
```

This looks good. Now we will check vault

```bash
vault status
```

Expected output:

```log
Key             Value
---             -----
Seal Type       shamir
Initialized     true
Sealed          false
Total Shares    1
Threshold       1
Version         1.16.2
Build Date      2024-04-22T16:25:54Z
Storage Type    inmem
Cluster Name    vault-cluster-e8cd73ab
Cluster ID      068df8dd-a466-307f-e559-517129785fc3
HA Enabled      false
```

Next, we create a database role for vault to connect. This user/role should have permission to create application roles.

```bash
ysqlsh -c "CREATE ROLE vault_admin WITH ENCRYPTED PASSWORD  'P@ssw0rd' LOGIN NOSUPERUSER CREATEROLE;"
```

- Vault database user (`vault_admin`) is given only `CREATEROLE` permission
- This prevents any accidental misconfiguration on vault side from altering any data per say

Expected output:

```sql
CREATE ROLE
```

Noe, we need to create a database role for our application. Roles created by vault will "inherit" the permissions from this role

```bash
ysqlsh -c "
CREATE ROLE "approle" WITH NOLOGIN; \
GRANT USAGE ON SCHEMA public to GROUP "approle"; \
GRANT ALL ON ALL TABLES IN SCHEMA public to GROUP "approle" ; \
GRANT ALL ON ALL SEQUENCES IN SCHEMA public to  GROUP "approle" ; \
"
```

- `CREATE ROLE` statement creates a role
  - `NOLOGIN` will ensure that this role is not used for any login
- `GRANT` statements grants (one or more) privileges on a set of objects
  - Just enough permissions that should be needed for a application to work
  - Grant privilege as a group, so individual users created by vault, will become member of this and inherits the permissions.
  - `USAGE` permission for schema is needed for an application user to be abel to access tables and sequences under
    the schema.

Expected output:

```sql
GRANT
```

Lets check the new role in database

```bash
ysqlsh -c '\du'
```

This is a shorthand command for a very long query. It shows the defines users and roles.

Expected output:

```sql
                                    List of roles
  Role name   |                         Attributes                         | Member of
--------------+------------------------------------------------------------+-----------
approle      | Cannot login                                               | {}
postgres     | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
vault_admin  | Create role                                                | {}
yb_db_admin  | No inheritance, Cannot login                               | {}
yb_extension | Cannot login                                               | {}
yb_fdw       | Cannot login                                               | {}
yugabyte     | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
```

As you can see `approle` is defined here and it cannot login


Now, on this vault setup. First we enable database secrets engine

```bash
vault secrets enable database
```

Expected output:

```sql
Success! Enabled the database secrets engine at: database/
```

New, create a vault database secrets connection

```bash
vault write database/config/yugabytedb \
  name="yugabyte" \
  plugin_name=postgresql-database-plugin \
  allowed_roles='approle' \
  verify_connection="true" \
  username="vault_admin" \
  password="P@ssw0rd" \
  root_rotation_statements="ALTER ROLE {{username}} WITH ENCRYPTED PASSWORD '{{password}}';" \
  password_authentication="scram-sha-256" \
  connection_url="postgres://{{username}}:{{password}}@$PGHOST:5433/$PGDATABASE"
```

- `plugin_name` is set to postgresql-database-plugin, based on documentation
- `allowed_roles` it can be a list of roles. We just need one.
- `username` and `password` were created above
- `root_rotation_statement` is for making the vault change its own password. I think this is a good practice. We will rotate the this password immediately, below.
- `password_authentication` is set to `scram-sha-256` based on [Postgres' authentication methods](https://www.postgresql.org/docs/current/auth-password.html).
- `connection_url` is templated to use `username` and `password`. `$YB_HOST` will be substituted to a proper host name by the shell. You can replace this with any other hostname where yugabytedb is running.

Expected output:

```bash
Success! Data written to: database/config/yugabytedb
```

After creating the connect, first thing we need to do is to secure the database password of the admin user. So we rotate root credentials

```bash
vault write -force database/rotate-root/yugabytedb
```

Expected output:

```bash
Success! Data written to: database/rotate-root/yugabytedb
```

Now the password for vault_admin is also rotated. Lets check if we can login with the original password (Hint: we can't)

```bash
PGPASSWORD=P@ssw0rd ysqlsh -U vault_admin -c 'select 1 as works;'
```

Expected output:

```bash
ysqlsh: FATAL:  password authentication failed for user "vault_admin"
```

Great! Now even I don't know whats the password to impersonate vault. Next, we create a dynamic db credentials generation config for `yugabytedb` to use the automatic statement generation capability

```bash
  vault write database/roles/approle \
    db_name=yugabytedb \
    creation_statements="CREATE ROLE \"{{name}}\" WITH ENCRYPTED PASSWORD '{{password}}' VALID UNTIL '{{expiration}}' LOGIN IN ROLE \"approle\";" \
    revocation_statements="DROP ROLE \"{{name}}\";" \
    rollback_statements="DROP ROLE \"{{name}}\";" \
    renew_statements="ALTER ROLE \"{{name}}\" WITH VALID UNTIL '{{expiration}}';" \
    default_ttl="1h" \
    max_ttl="24h"
```

- `creation_statements` is a minimal requirement. Others are optional. This statement is creating a user in database:
  - With dynamic username
  - With dynamic password
  - With expiration based policy (1hr in this case)
  - With membership of `approle` group
- `revocation_statement` and `rollback_statements` are simple `DROP ROLE` statements. Since we do not make any additional grants.
- `renew_statement` alters the role and extends the validity of the role

Expected output:

```bash
Success! Data written to: database/roles/approle
```

## Test

Vault is now ready to create dynamic credentials for out application. Lets create a create a credential with this config and check


```bash
CREDS="$(vault read database/creds/approle)"
echo "$CREDS"
```

- Storing this in a variable so that we can get lease_id, username, and password in following steps

Expected output:

```log
Key                Value
---                -----
lease_id           database/creds/approle/lkM5j7NPjIcnMIBI0sg1ZdQT
lease_duration     1h
lease_renewable    true
password           aVOzfQ3ICNl3-ztUA21y
username           v-token-approle-L65VQiweoYeDxqnMaBF5-1716390741
```

> **Important**: Record this as we will need lease_id, username and password for following setups

Also, check on database side what we see in the user list.

```bash
ysqlsh -c '\du'
```

Expected output:

```sql
                    Role name                    |                         Attributes                         | Member of
-------------------------------------------------+------------------------------------------------------------+-----------
 approle                                         | Cannot login                                               | {}
 postgres                                        | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 v-token-approle-L65VQiweoYeDxqnMaBF5-1716390741 | Password valid until 2024-05-22 16:12:26+00                | {approle}
 vault_admin                                     | Create role                                                | {}
 yb_db_admin                                     | No inheritance, Cannot login                               | {}
 yb_extension                                    | Cannot login                                               | {}
 yb_fdw                                          | Cannot login                                               | {}
 yugabyte                                        | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
```

- `v-token-approle-L65VQiweoYeDxqnMaBF5-1716390741` is a dynamically created user with 1 hour validity
- Its part of approle group

Let's use the credentials for this newly created user to connect to database and execute a query

```bash
PGPASSWORD=$(echo "$CREDS"| grep password | cut -c20-) PGUSER=$(echo "$CREDS"| grep username | cut -c20-) ysqlsh -c 'select count(customer_id) from customers;'
```

- Using `CREDS` variable to extract username and password for the connection
- Reading data table `customers`

Expected output:

```sql
 count
-------
    91
(1 row)
```

So, far all okay. Lets test a renewal operation to validate our renew query

```bash
vault lease renew $(echo "$CREDS"| grep lease_id| cut -c20-)
```

Expected output:

```log
Key                Value
---                -----
lease_id           database/creds/approle/lkM5j7NPjIcnMIBI0sg1ZdQT
lease_duration     1h
lease_renewable    true
```

On database, we should see updated validity time

```bash
ysqlsh -c '\du'
```

Expected output:

```sql
                                                      List of roles
                    Role name                    |                         Attributes                         | Member of
-------------------------------------------------+------------------------------------------------------------+-----------
 approle                                         | Cannot login                                               | {}
 postgres                                        | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 v-token-approle-L65VQiweoYeDxqnMaBF5-1716390741 | Password valid until 2024-05-22 16:20:58+00                | {approle}
 vault_admin                                     | Create role                                                | {}
 yb_db_admin                                     | No inheritance, Cannot login                               | {}
 yb_extension                                    | Cannot login                                               | {}
 yb_fdw                                          | Cannot login                                               | {}
 yugabyte                                        | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
```

As you can see, the expiry time has gone up from `16:12:26+00` to `16:20:58+00`. Next (and laster) operation is revoking /deleting dynamic user

```bash
vault lease revoke $(echo "$CREDS"| grep lease_id| cut -c20-)
```

Expected output

```bash
All revocation operations queued successfully!
```

Let's check lease information (Hint: there isn't any)

```bash
vault lease lookup $(echo "$CREDS"| grep lease_id| cut -c20-)
```

Expected output:

```bash
error looking up lease id database/creds/approle/lkM5j7NPjIcnMIBI0sg1ZdQT: Error making API request.

URL: PUT http://vault:8200/v1/sys/leases/lookup
Code: 400. Errors:

* invalid lease
```

And on the db side, `v-token-approle-L65VQiweoYeDxqnMaBF5-1716390741` should be gone.

```bash
ysqlsh -c '\du'
```

Expected output:

```sql
                                      List of roles
  Role name   |                         Attributes                         | Member of
--------------+------------------------------------------------------------+-----------
 approle      | Cannot login                                               | {}
 postgres     | Superuser, Create role, Create DB, Replication, Bypass RLS | {}
 vault_admin  | Create role                                                | {}
 yb_db_admin  | No inheritance, Cannot login                               | {}
 yb_extension | Cannot login                                               | {}
 yb_fdw       | Cannot login                                               | {}
 yugabyte     | Superuser, Create role, Create DB, Replication, Bypass RLS | {}

```

- Dynamically created role (` v-token-approle-L65VQiweoYeDxqnMaBF5-171639074`) is gone.

## Cleanup

To clean up this lab:

- Exit shell

  ```bash
  exit
  ```

- Delete containers

  ```bash
  docker compose down -v --remove-orphans
  ```

That's all. Feel free to reach out to me on the [community slack](https://yugabyte.com/slack)/[Twitter](https://twitter.com/yogendra) for more info or feedback. Ta

## References

- Postgres
  - [CREATE ROLE](https://www.postgresql.org/docs/current/sql-createrole.html)
  - [GRANT](https://www.postgresql.org/docs/9.1/sql-grant.html)
- Vault
  - [Database Secrets Engine](https://developer.hashicorp.com/vault/api-docs/secret/databases#database-secrets-engine-api)
  - [Database Secrets Engine / Postgres](https://developer.hashicorp.com/vault/api-docs/secret/databases/postgresql)
  - [Blog: PostgreSQL minimum permissions required to create the dynamic/static credentials.](https://support.hashicorp.com/hc/en-us/articles/26413108467731-Vault-Database-Secrets-Engine-PostgreSQL-minimum-permissions-required-to-create-the-dynamic-static-credentials)
- YugabyteD
  - [Hashicorp Vault](https://docs.yugabyte.com/preview/integrations/hashicorp-vault/)
