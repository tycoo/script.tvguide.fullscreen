import sqlite3

tables = ["programs"]

f = open('dump.sql','wb')

connection = sqlite3.connect('source.db')

f.write('BEGIN TRANSACTION;\n')

cu = connection.cursor()
q = """
    SELECT "name", "type", "sql"
    FROM "sqlite_master"
        WHERE "sql" NOT NULL AND
        "type" == 'table'
        ORDER BY "name"
    """
schema_res = cu.execute(q)
for table_name, type, sql in schema_res.fetchall():
    if table_name in tables:
        sql = sql.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
        f.write(sql+';\n')
        table_name_ident = table_name.replace('"', '""')
        f.write('DELETE FROM %s;\n' % table_name_ident)        
        res = cu.execute('PRAGMA table_info("{0}")'.format(table_name_ident))
        column_names = [str(table_info[1]) for table_info in res.fetchall()]
        q = """SELECT 'INSERT OR REPLACE INTO "{0}" VALUES({1})' FROM "{0}";""".format(
            table_name_ident,
            ",".join("""'||quote("{0}")||'""".format(col.replace('"', '""')) for col in column_names))
        query_res = cu.execute(q)
        for row in query_res:
            f.write("%s;\n" % row[0].encode("utf8"))

f.write('COMMIT;\n')