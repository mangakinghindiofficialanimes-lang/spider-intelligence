"""Training entry point for Spider Brain V0.1."""

from pathlib import Path
import torch
import torch.nn.functional as F
from brain.tokenizer import CharTokenizer
from brain.model import SpiderBrain
from training.dataset import make_dataset

DATA_PATH = Path("data/training.txt")
BLOCK_SIZE = 64


def main():
    text = DATA_PATH.read_text(encoding="utf-8")
    tokenizer = CharTokenizer(text)
    x, y = make_dataset(text, tokenizer, BLOCK_SIZE)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    x, y = x.to(device), y.to(device)
    model = SpiderBrain(tokenizer.vocab_size, BLOCK_SIZE).to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-3)

    for step in range(1000):
        logits = model(x)
        loss = F.cross_entropy(logits, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step % 100 == 0:
            print(f"step={step} loss={loss.item():.4f}")

    Path("checkpoints").mkdir(exist_ok=True)
    torch.save({"model": model.state_dict(), "vocab": tokenizer.vocab, "block_size": BLOCK_SIZE}, "checkpoints/spider_v0_1.pt")
    print("Saved checkpoint: checkpoints/spider_v0_1.pt")

if __name__ == "__main__":
    main()
