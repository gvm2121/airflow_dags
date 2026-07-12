from dags.fecha import dia
import pandas as pd
from psycopg2 import sql
from decimal import Decimal

pd.set_option('display.float_format', '{:.6f}'.format) # 5 decimales
df = pd.read_excel("rentabilidades.xlsx",
                   sheet_name="Rentabilidades Listado Completo",
                   skiprows=6,
                   header=1,
                   index_col=0,
                   names = [
    "id",
    "administradora",
    "run",
    "fondo",
    "serie",
    "categoria_cmf",
    "categoria_afm",
    "valor_cuota_peso_chileno",
    "valor_cuota_moneda_original",
    "apv",
    "diaria_nominal_pct",
    "dias7_nominal_pct",
    "dias7_real_pct",
    "dias30_nominal_pct",
    "dias30_real_pct",
    "meses3_nominal_pct",
    "meses3_real_pct",
    "meses12_nominal_pct",
    "meses12_real_pct",
    "ytd_nominal_pct",
    "ytd_real_pct",
    "moneda_original",
]
                  )
df.dropna(how='all',inplace=True)
df.reset_index(drop=True,inplace=True)

df["scrapping_timestamp"] = f"{dia} 00:00:00"     # TIMESTAMP
df["scrapping_date"]      = dia       # DATE

#df["scrapping_timestamp"] = datetime.now() - timedelta(days=1)     # TIMESTAMP
#df["scrapping_date"]      = date.today() - timedelta(days=1) 

# 2) Conexión a PostgreSQL  (método habitual: usa variables de entorno)
conn = psycopg2.connect(
    host="localhost",
    dbname="aaff",
    user="aaff_db_scrapper",
    password="1234",
    port=5432
)
conn.autocommit = False           # transacción explícita
cur = conn.cursor()

# 3) Preparar la INSERT dinámica (evita escribir 20+ columnas a mano)
cols = df.columns.tolist()        # en el mismo orden que el DataFrame
placeholders = [f"%({c})s" for c in cols]

insert_stmt = sql.SQL("""
    INSERT INTO rent_raw ({fields})
    VALUES ({values})
""").format(
    fields = sql.SQL(',').join(map(sql.Identifier, cols)),
    values = sql.SQL(',').join(sql.Placeholder(c) for c in cols)
)

try:
    # iterar por filas convirtiendo floats a Decimal (mantiene NUMERIC(18,6))
    for record in df.to_dict(orient="records"):
        for k, v in record.items():
            if isinstance(v, float):
                record[k] = Decimal(str(v))    # precisión exacta
            if pd.isna(v):                     # NaN -> NULL
                record[k] = None
        cur.execute(insert_stmt, record)

    conn.commit()
    print(f"{cur.rowcount} filas insertadas correctamente")

except Exception as e:
    conn.rollback()
    raise e

finally:
    cur.close()
    conn.close()