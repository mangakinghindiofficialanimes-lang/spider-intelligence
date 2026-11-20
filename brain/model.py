"""A tiny neural language model initialized from random weights."""

import torch
from torch import nn

class SpiderBrain(nn.Module):
    def __init__(self, vocab_size: int, block_size: int = 64, embedding_dim: int = 64, hidden_dim: int = 128):
        super().__init__()
        self.block_size = block_size
        self.embedding = nn.Embedding(vocab_size, embedding_dim)
        self.position = nn.Embedding(block_size, embedding_dim)
        self.layers = nn.Sequential(
            nn.Linear(block_size * embedding_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, hidden_dim),
            nn.GELU(),
            nn.Linear(hidden_dim, vocab_size),
        )

    def forward(self, tokens: torch.Tensor) -> torch.Tensor:
        batch, length = tokens.shape
        if length != self.block_size:
            raise ValueError(f"Expected sequence length {self.block_size}, got {length}")
        positions = torch.arange(length, device=tokens.device)
        x = self.embedding(tokens) + self.position(positions)
        x = x.reshape(batch, -1)
        return self.layers(x)
