# generateQuery

It is to generate CREATE TABLE script with specified template.
It can help to generate CREATE scripts for various database with a template.

# Writing rules
```
CREATE TABLE $TABLE_NAME
I column_name PRIMARY KEY,  -- I -> INTEGER / INT
T column_name,              -- T -> TEXT / VARCHAR
B column_name,              -- B -> BOOLEAN
BL column_name              -- BL -> BLOB
```

# Supported DB and Types (It can be added)

- mysql
    - INT
    - VARCHAR(255)
    - BOOLEAN
    - BLOB
- db2
    - INTEGER
    - VARCHAR(255)
    - BOOLEAN
    - BLOB
