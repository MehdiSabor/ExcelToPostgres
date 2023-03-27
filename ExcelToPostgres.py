import pandas as pd
import psycopg2

# Read data from excel file
df = pd.read_excel('data.xlsx')

# Connect to postgres database
conn = psycopg2.connect(
    host="localhost",
    database="database",
    user="postgres",
    password="password"
)

# Create a cursor object to execute SQL commands
cur = conn.cursor()

# Clear the data in the releve table
cur.execute("DELETE FROM Name")
print("Deleted all Names")
conn.commit()

# Loop through the rows in the excel data and insert them into the postgres table
for index, row in df.iterrows():
    try:
        cur.execute("INSERT INTO Name (name, lastname) VALUES (%s, %s)",
                    (row['FNAME'], row['LNAME']))
    except psycopg2.IntegrityError:
        print("Name already exists, skipping...")
        cur.execute("ROLLBACK")
        continue
    print("Inserting row:", row)
# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()