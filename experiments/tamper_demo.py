import torch
import time
from embeddings.embedding_store import EmbeddingStore


# -----------------------------
# Step 1: Vocabulary
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

TOKEN_TO_TAMPER = "python"
TAMPER_SCALE = 0.5


# -----------------------------
# Step 2: Load / Create base embeddings
# -----------------------------
import os

BASE_PATH = "embeddings/base_embeddings.safetensors"

if not os.path.exists(BASE_PATH):
    store = EmbeddingStore(vocab=vocab, dim=32)
    store.initialize()
    store.save(BASE_PATH)
    print("✅ Base embeddings created")
else:
    store = EmbeddingStore.load(BASE_PATH)
    print("ℹ️ Base embeddings loaded from disk")


token_id = vocab[TOKEN_TO_TAMPER]
original_vector = store.get_vector(token_id)

print(f"\n🔹 Original embedding for '{TOKEN_TO_TAMPER}':")
print(original_vector[:5])


# -----------------------------
# Step 3: Tamper the embedding
# -----------------------------
tampered_vector = original_vector.clone()
tampered_vector += TAMPER_SCALE * torch.randn_like(tampered_vector)

store.update_vector(token_id, tampered_vector)

print(f"\n⚠️ Tampered embedding for '{TOKEN_TO_TAMPER}':")
print(tampered_vector[:5])


# -----------------------------
# Step 4: Save tampered embeddings (VERSIONED)
# -----------------------------
timestamp = int(time.time())
tampered_path = f"embeddings/tampered_embeddings_{timestamp}.safetensors"

store.save(tampered_path)

print(f"\n💾 Tampered embeddings saved at: {tampered_path}")


# -----------------------------
# Step 5: Measure difference
# -----------------------------
difference = torch.norm(original_vector - tampered_vector).item()
print(f"\n📊 L2 Distance after tampering: {difference:.6f}")
