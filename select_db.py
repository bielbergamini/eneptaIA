import json
import mysql.connector
from dotenv import load_dotenv
import os
from collections import defaultdict

load_dotenv()

# Conexão com MySQL no Docker
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password= os.getenv("SENHA"),
    database= os.getenv("DATABASE"),
    port=3306
)
cursor = conn.cursor(dictionary=True)

dataset = []

# =========================
# 1) Motores -> Produtos
# =========================
cursor.execute("""
    SELECT m.modelo AS motor, p.name AS produto
    FROM ironsearch_product_motor pm
    JOIN ironsearch_motormodel m ON pm.motormodel_id = m.id
    JOIN ironsearch_product p ON pm.product_id = p.id
""")

motores = defaultdict(list)
for row in cursor.fetchall():
    motores[row["motor"]].append(row["produto"])

for motor, produtos in motores.items():
    output = f"Produtos compatíveis com o motor '{motor}' incluem: " + ", ".join(f"'{p}'" for p in produtos)
    dataset.append({
        "input": f"Encontre produtos para o motor '{motor}'.",
        "output": output
    })

# =========================
# 2) Produtos -> Carrocerias
# =========================
cursor.execute("""
    SELECT p.name AS produto, c.modelo AS carroceria
    FROM ironsearch_product_carroceria pc
    JOIN ironsearch_product p ON pc.product_id = p.id
    JOIN ironsearch_carroceriamodel c ON pc.carroceriamodel_id = c.id
""")

produtos_carroceria = defaultdict(list)
for row in cursor.fetchall():
    produtos_carroceria[row["produto"]].append(row["carroceria"])

for produto, carrocerias in produtos_carroceria.items():
    output = f"As carrocerias disponíveis para o produto '{produto}' incluem: " + ", ".join(f"'{c}'" for c in carrocerias)
    dataset.append({
        "input": f"Quais carrocerias estão disponíveis para o produto '{produto}'?",
        "output": output
    })

# =========================
# 3) Produtos -> Chassis
# =========================
cursor.execute("""
    SELECT p.name AS produto, ch.modelo AS chassi
    FROM ironsearch_product_chassi pc
    JOIN ironsearch_product p ON pc.product_id = p.id
    JOIN ironsearch_chassimodel ch ON pc.chassimodel_id = ch.id
""")

produtos_chassi = defaultdict(list)
for row in cursor.fetchall():
    produtos_chassi[row["produto"]].append(row["chassi"])

for produto, chassis in produtos_chassi.items():
    output = f"Os chassis compatíveis com o produto '{produto}' incluem: " + ", ".join(f"'{c}'" for c in chassis)
    dataset.append({
        "input": f"Quais chassis são compatíveis com o produto '{produto}'?",
        "output": output
    })

# =========================
# 4) Produtos -> Equivalentes
# =========================
cursor.execute("""
    SELECT p1.name AS produto, p2.name AS equivalente
    FROM ironsearch_product_equivalent_products ep
    JOIN ironsearch_product p1 ON ep.from_product_id = p1.id
    JOIN ironsearch_product p2 ON ep.to_product_id = p2.id
""")

produtos_equivalentes = defaultdict(list)
for row in cursor.fetchall():
    produtos_equivalentes[row["produto"]].append(row["equivalente"])

for produto, equivalentes in produtos_equivalentes.items():
    output = f"Os produtos equivalentes a '{produto}' incluem: " + ", ".join(f"'{e}'" for e in equivalentes)
    dataset.append({
        "input": f"Quais são os produtos equivalentes a '{produto}'?",
        "output": output
    })

# =========================
# Salvar dataset
# =========================
with open("dataset_real.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print(f"Dataset real gerado com {len(dataset)} exemplos em dataset.json")
