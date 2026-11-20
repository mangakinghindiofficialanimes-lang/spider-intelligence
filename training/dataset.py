"""Build next-character training examples."""

import torch

def make_dataset(text: str, tokenizer, block_size: int):
    encoded = torch.tensor(tokenizer.encode(text), dtype=torch.long)
    if len(encoded) <= block_size:
        raise ValueError("Training text must be longer than block_size.")
    inputs, targets = [], []
    for start in range(len(encoded) - block_size):
        inputs.append(encoded[start:start + block_size])
        targets.append(encoded[start + block_size])
    return torch.stack(inputs), torch.stack(targets)
