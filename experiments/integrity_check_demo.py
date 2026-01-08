import glob
import os

from embeddings.embedding_store import EmbeddingStore
from embeddings.integrity import EmbeddingIntegrityRegistry
from embeddings.audit import AuditLogger


# -----------------------------
# Vocabulary (MUST match base)
# -----------------------------
vocab = {
    "python": 0,
    "java": 1,
    "ai": 2,
    "language": 3,
    "snake": 4,
    "model": 5,
    "code": 6
}

BASE_PATH = "embeddings/base_embeddings.safetensors"


# -----------------------------
# Load BASE embeddings (trusted)
# -----------------------------
if not os.path.exists(BASE_PATH):
    raise FileNotFoundError(
        "❌ Base embeddings not found. Integrity verification impossible."
    )

base_store = EmbeddingStore.load(BASE_PATH)

registry = EmbeddingIntegrityRegistry()
registry.register(base_store.embedding.weight)

print("✅ Trusted embedding hashes registered")


# -----------------------------
# Auto-detect latest tampered embeddings
# -----------------------------
tampered_files = glob.glob("embeddings/tampered_embeddings_*.safetensors")

if not tampered_files:
    raise FileNotFoundError(
        "❌ No tampered embedding files found to verify."
    )

latest_tampered = max(tampered_files, key=os.path.getctime)

print(f"ℹ️ Using tampered file: {latest_tampered}")

tampered_store = EmbeddingStore.load(latest_tampered)


# -----------------------------
# Verify integrity
# -----------------------------
results = registry.verify(tampered_store.embedding.weight)

print("\n🔍 Integrity Check Results:")

tampering_detected = False
tampered_tokens = []

for token, token_id in vocab.items():
    intact = results[token_id]
    status = "✅ INTACT" if intact else "❌ TAMPERED"
    print(f"{token:10s} → {status}")

    if not intact:
        tampering_detected = True
        tampered_tokens.append(token)


# -----------------------------
# Fail-fast enforcement + audit
# -----------------------------
if tampering_detected:
    logger = AuditLogger()
    logger.log_integrity_violation(
        tampered_tokens=results,
        vocab=vocab,
        embedding_file=latest_tampered
    )

    raise RuntimeError(
        f"\n🚨 EMBEDDING INTEGRITY VIOLATION DETECTED\n"
        f"Tampered tokens: {tampered_tokens}\n"
        f"Aborting model usage."
    )

else:
    print("\n✅ Embeddings verified successfully. Safe to proceed.")
