#! /bin/bash

touch archive.db
cat schema.sql | sqlite3 archive.db