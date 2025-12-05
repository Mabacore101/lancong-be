from sentence_transformers import SentenceTransformer
from neo4j import GraphDatabase

# === Load Model ===
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# === Koneksi Neo4j ===
uri = "neo4j://localhost:7687"
user = "neo4j"
password = "Allan123410"

driver = GraphDatabase.driver(uri, auth=(user, password))

# === Ambil seluruh Place dari Neo4j ===
def get_all_places(tx):
    result = tx.run("""
        MATCH (p:Place)
        RETURN p.id AS id, p.name AS name
    """)
    return result.data()

# === Insert embedding kembali ke Neo4j ===
def save_embedding(tx, id_value, embedding):
    tx.run("""
        MATCH (p:Place {id: $id})
        SET p.embedding = $embedding
    """, id=id_value, embedding=embedding)

# === Pipeline: Ambil > Buat Embedding > Simpan ===
with driver.session() as session:

    # gunakan execute_read di Neo4j Driver 5+
    places = session.execute_read(get_all_places)

    print(f"Jumlah data ditemukan: {len(places)}")

    for place in places:
        text = place["name"]
        emb = model.encode(text).tolist()

        # gunakan execute_write di driver baru
        session.execute_write(save_embedding, place["id"], emb)

        print(f"✓ Embedding dibuat untuk Place {place['id']}")

driver.close()
print("Selesai membuat embedding!")
