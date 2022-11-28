import sqlite3 

database = 'IPL.sqlite'

conn = sqlite3.connect(database)
cur = conn.cursor()

cur.execute('SELECT * FROM "table"')
raw_data = cur.fetchall()

new_data = []
for data in raw_data :
    new_set = []
    venue = data[2]
    venue = str(str(venue).split(',')[-1]).strip()
    for i in data :
        if i != data[2] :
            new_set.append(i)
        else :
            new_set.append(venue)
    new_data.append(new_set)

print(raw_data[0])
print(new_data[0])

for i in new_data :
    date = i[0]
    match = i[1]
    venue = i[2]
    winner = i[3]

    cur.execute(f'UPDATE "table" SET "venue" = "{venue}" WHERE "date" = "{date}" AND "match" = "{match}" ')
conn.commit()
cur.close()