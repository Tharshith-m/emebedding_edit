# Embeddings Integrity

A Python project for ensuring the integrity and security of word embeddings in machine learning models. This toolkit provides mechanisms to detect tampering, maintain audit logs, and verify the authenticity of embedding vectors.

## Features

- **Secure Embedding Storage**: Store embeddings using SafeTensors format for secure serialization
- **Integrity Verification**: Hash-based verification to detect unauthorized modifications
- **Audit Logging**: Track integrity violations and security events
- **Tamper Detection**: Demonstrate and detect embedding tampering attacks
- **Versioned Storage**: Timestamp-based versioning for embedding files

## Project Structure

```
embeddings-integrity/
├── README.md
├── requirements.txt
├── data/
│   └── vocab.txt
├── embeddings/
│   ├── __init__.py
│   ├── embedding_store.py    # Core embedding management
│   ├── integrity.py          # Integrity verification system
│   └── audit.py              # Audit logging functionality
├── experiments/
│   └── tamper_demo.py        # Demonstration of tamper detection
├── model/
│   └── simple_lm.py          # Placeholder for language model integration
└── utils/
    └── hashing.py            # SHA256 hashing utilities
```

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory.

2. **Create a virtual environment**:
   ```bash
   python -m venv myenv
   ```

3. **Activate the virtual environment**:
   - On Windows:
     ```bash
     myenv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source myenv/bin/activate
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Tamper Demo

The `tamper_demo.py` script demonstrates how to create embeddings, tamper with them, and measure the impact:

```bash
python experiments/tamper_demo.py
```

This will:
- Create or load base embeddings
- Tamper with a specific token's embedding vector
- Save the tampered embeddings with a timestamp
- Calculate and display the L2 distance between original and tampered vectors

### Using the Embedding Store

```python
from embeddings.embedding_store import EmbeddingStore

# Define vocabulary
vocab = {"python": 0, "java": 1, "ai": 2}

# Create and initialize store
store = EmbeddingStore(vocab=vocab, dim=32)
store.initialize()

# Save embeddings
store.save("embeddings/my_embeddings.safetensors")

# Load embeddings
loaded_store = EmbeddingStore.load("embeddings/my_embeddings.safetensors")
```

### Integrity Verification

```python
from embeddings.integrity import EmbeddingIntegrityRegistry

# Register trusted embeddings
registry = EmbeddingIntegrityRegistry()
registry.register(store.embedding.weight)

# Verify integrity
results = registry.verify(store.embedding.weight)
print(results)  # {token_id: True/False}
```

### Audit Logging

```python
from embeddings.audit import AuditLogger

logger = AuditLogger()
logger.log_integrity_violation(tampered_tokens, vocab, "embeddings/file.safetensors")
```

## Dependencies

- `torch`: PyTorch for tensor operations and embeddings
- `numpy`: Numerical computing
- `safetensors`: Secure tensor serialization

## Security Considerations

- Embeddings are stored in SafeTensors format for security
- SHA256 hashing is used for integrity verification
- Audit logs track all integrity violations
- Versioned files prevent accidental overwrites

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure integrity checks pass
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.