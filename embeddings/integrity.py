from typing import Dict
import torch
from utils.hashing import hash_tensor


class EmbeddingIntegrityRegistry:
    """
    Stores and verifies trusted embedding hashes.
    """

    def __init__(self):
        self.reference_hashes: Dict[int, str] = {}

    def register(self, embedding_weight: torch.Tensor):
        """
        Register trusted hashes for all token embeddings.
        """
        for token_id in range(embedding_weight.size(0)):
            self.reference_hashes[token_id] = hash_tensor(
                embedding_weight[token_id]
            )

    def verify(self, embedding_weight: torch.Tensor) -> Dict[int, bool]:
        """
        Verify embeddings against trusted hashes.
        Returns a dict: token_id -> is_intact
        """
        results = {}

        for token_id, trusted_hash in self.reference_hashes.items():
            current_hash = hash_tensor(embedding_weight[token_id])
            results[token_id] = (current_hash == trusted_hash)

        return results
