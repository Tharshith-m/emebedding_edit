import hashlib
import torch


def hash_tensor(tensor: torch.Tensor) -> str:
    """
    Generate a SHA256 hash for a tensor.
    """
    tensor_bytes = tensor.detach().cpu().numpy().tobytes()
    return hashlib.sha256(tensor_bytes).hexdigest()
