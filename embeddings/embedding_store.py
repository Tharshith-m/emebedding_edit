# import torch
# from safetensors.torch import save_file, load_file
# from typing import Dict


# class EmbeddingStore:
#     """
#     Responsible for:
#     - Creating embeddings
#     - Loading embeddings
#     - Controlled access to vectors
#     """

#     def __init__(self, vocab: Dict[str, int], dim: int = 32):
#         self.vocab = vocab
#         self.dim = dim
#         self.embedding = torch.nn.Embedding(len(vocab), dim)

#     def initialize(self, seed: int = 42):
#         torch.manual_seed(seed)
#         torch.nn.init.normal_(self.embedding.weight, mean=0.0, std=0.02)

#     def save(self, path: str):
#         save_file(
#             {"embedding": self.embedding.weight},
#             path
#         )

#     @staticmethod
#     def load(path: str):
#         data = load_file(path)
#         weight = data["embedding"]

#         store = EmbeddingStore(
#             vocab={},
#             dim=weight.shape[1]
#         )
#         store.embedding.weight = torch.nn.Parameter(weight)
#         return store

#     def get_vector(self, token_id: int):
#         return self.embedding.weight[token_id].clone()

#     def update_vector(self, token_id: int, new_vector: torch.Tensor):
#         self.embedding.weight.data[token_id] = new_vector


import os
import torch
from safetensors.torch import save_file, load_file
from typing import Dict


class EmbeddingStore:
    def __init__(self, vocab: Dict[str, int], dim: int = 32):
        self.vocab = vocab
        self.dim = dim
        self.embedding = torch.nn.Embedding(len(vocab), dim)

    def initialize(self, seed: int = 42):
        torch.manual_seed(seed)
        torch.nn.init.normal_(self.embedding.weight, mean=0.0, std=0.02)

    def save(self, path: str, overwrite: bool = False):
        if os.path.exists(path) and not overwrite:
            raise FileExistsError(
                f"Embedding file already exists: {path}. "
                f"Use overwrite=True to replace it."
            )

        save_file(
            {"embedding": self.embedding.weight},
            path
        )

    @staticmethod
    def load(path: str):
        data = load_file(path)
        weight = data["embedding"]

        store = EmbeddingStore(
            vocab={},
            dim=weight.shape[1]
        )
        store.embedding.weight = torch.nn.Parameter(weight)
        return store

    def get_vector(self, token_id: int):
        return self.embedding.weight[token_id].clone()

    def update_vector(self, token_id: int, new_vector: torch.Tensor):
        self.embedding.weight.data[token_id] = new_vector


