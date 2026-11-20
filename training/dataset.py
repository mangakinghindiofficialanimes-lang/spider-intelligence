"""Text loading, train/validation split, and batches."""
from pathlib import Path
import torch
def load_text_files(paths):
 chunks=[Path(p).read_text(encoding="utf-8",errors="replace") for p in paths if Path(p).is_file()]
 if not chunks: raise FileNotFoundError("No text files found.")
 return "\n\n".join(chunks)
def encode_dataset(text,tokenizer):
 ids=torch.tensor(tokenizer.encode(text),dtype=torch.long)
 if len(ids)<30: raise ValueError("Dataset too small; add more text.")
 split=max(2,int(len(ids)*0.9)); return ids[:split],ids[split:]
def get_batch(split_ids,block_size,batch_size,device):
 if len(split_ids)<=block_size+1: raise ValueError("Split too short; add text or reduce block_size.")
 starts=torch.randint(0,len(split_ids)-block_size-1,(batch_size,))
 x=torch.stack([split_ids[i:i+block_size] for i in starts]); y=torch.stack([split_ids[i+1:i+block_size+1] for i in starts]); return x.to(device),y.to(device)
