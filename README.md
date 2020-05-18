# generateQuery

It is to generate CREATE TABLE script with specified template.\
It can help to generate CREATE scripts for various database with a template.

# How to use?
## Without option
```
$ ./generateQuery.py
Enter input file name : [template file name]
Enter output file name : [output file name]
Enter the target database : [Database engine name(mysql/db2 ...)]
```
## With option
```
$ ./generateQuery.py [-i template file] [-o output file]
Enter the target database : [Database engine name(mysql/db2 ...)]
```

# Writing rules (Template file example)
```
CREATE TABLE $TABLE_NAME (
I column_name PRIMARY KEY,  -- I -> INTEGER / INT
T column_name,              -- T -> TEXT / VARCHAR
B column_name,              -- B -> BOOLEAN
BL column_name              -- BL -> BLOB
);
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
