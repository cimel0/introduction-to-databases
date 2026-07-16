# /// script
# requires-python = ">=3.10"
# dependencies = [
#  "psycopg[binary]"
# ]
# ///

import psycopg
import getpass

# Passwort sicher eingeben
password = getpass.getpass("Password: ")

# Verbindung zur Datenbank
con = psycopg.connect(
    host='dmi-dbis-introdb1.dmi.unibas.ch',
    port=5432,
    dbname='introdb',
    user='introdb107',
    password=password,
)

cur = con.cursor()
print("✓ Verbindung erfolgreich!\n")

# 1. WELCHE TABELLEN GIBT ES?
print("=" * 60)
print("SCHRITT 1: Alle Tabellen in der Datenbank")
print("=" * 60)

cur.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

tables = cur.fetchall()
print(f"Gefundene Tabellen ({len(tables)}):\n")
for table in tables:
    print(f"  - {table[0]}")

print("\n")

# 2. STRUKTUR JEDER TABELLE
print("=" * 60)
print("SCHRITT 2: Struktur jeder Tabelle")
print("=" * 60)

for table in tables:
    table_name = table[0]
    print(f"\nTabelle: {table_name}")
    print("-" * 60)
    
    # Spalten anzeigen
    cur.execute(f"""
        SELECT 
            column_name, 
            data_type, 
            character_maximum_length,
            is_nullable,
            column_default
        FROM information_schema.columns 
        WHERE table_name = '{table_name}'
        ORDER BY ordinal_position;
    """)
    
    columns = cur.fetchall()
    print(f"{'Spalte':<20} {'Typ':<20} {'NULL?':<10} {'Default':<20}")
    print("-" * 60)
    
    for col in columns:
        col_name = col[0]
        data_type = col[1]
        max_length = col[2]
        nullable = col[3]
        default = col[4] if col[4] else "-"
        
        # Datentyp formatieren
        if max_length:
            data_type = f"{data_type}({max_length})"
        
        print(f"{col_name:<20} {data_type:<20} {nullable:<10} {default:<20}")

print("\n")

# 3. PRIMARY KEYS
print("=" * 60)
print("SCHRITT 3: Primary Keys")
print("=" * 60)

for table in tables:
    table_name = table[0]
    
    cur.execute(f"""
        SELECT a.attname
        FROM pg_index i
        JOIN pg_attribute a ON a.attrelid = i.indrelid 
                            AND a.attnum = ANY(i.indkey)
        WHERE i.indrelid = '{table_name}'::regclass
        AND i.indisprimary;
    """)
    
    pk_columns = cur.fetchall()
    if pk_columns:
        pk_list = ", ".join([col[0] for col in pk_columns])
        print(f"  {table_name}: [{pk_list}]")

print("\n")

# 4. FOREIGN KEYS
print("=" * 60)
print("SCHRITT 4: Foreign Keys (Beziehungen)")
print("=" * 60)

cur.execute("""
    SELECT
        tc.table_name AS from_table,
        kcu.column_name AS from_column,
        ccu.table_name AS to_table,
        ccu.column_name AS to_column
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
        ON tc.constraint_name = kcu.constraint_name
        AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
        ON ccu.constraint_name = tc.constraint_name
        AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY'
    AND tc.table_schema = 'public'
    ORDER BY tc.table_name;
""")

foreign_keys = cur.fetchall()
print(f"Gefundene Foreign Keys ({len(foreign_keys)}):\n")

for fk in foreign_keys:
    from_table = fk[0]
    from_col = fk[1]
    to_table = fk[2]
    to_col = fk[3]
    print(f"  {from_table}.{from_col} → {to_table}.{to_col}")

print("\n")

# Verbindung schließen
cur.close()
con.close()
print("✓ Fertig!")