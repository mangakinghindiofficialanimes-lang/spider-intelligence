"""Small causal Transformer."""
import torch
from torch import nn
import torch.nn.functional as F
class CausalBlock(nn.Module):
 def __init__(self,d,h):
  super().__init__(); self.attn=nn.MultiheadAttention(d,h,batch_first=True); self.n1=nn.LayerNorm(d); self.n2=nn.LayerNorm(d); self.ff=nn.Sequential(nn.Linear(d,4*d),nn.GELU(),nn.Linear(4*d,d))
 def forward(self,x):
  t=x.size(1); mask=torch.triu(torch.ones(t,t,device=x.device,dtype=torch.bool),diagonal=1); a,_=self.attn(x,x,x,attn_mask=mask,need_weights=False); x=self.n1(x+a); return self.n2(x+self.ff(x))
class SpiderBrain(nn.Module):
 def __init__(self,vocab_size,block_size=128,embedding_dim=128,heads=4,layers=3):
  super().__init__(); self.block_size=block_size; self.token_emb=nn.Embedding(vocab_size,embedding_dim); self.pos_emb=nn.Embedding(block_size,embedding_dim); self.blocks=nn.Sequential(*[CausalBlock(embedding_dim,heads) for _ in range(layers)]); self.norm=nn.LayerNorm(embedding_dim); self.head=nn.Linear(embedding_dim,vocab_size)
 def forward(self,idx,targets=None):
  b,t=idx.shape
  if t>self.block_size: raise ValueError("Input exceeds block_size")
  x=self.token_emb(idx)+self.pos_emb(torch.arange(t,device=idx.device)); x=self.blocks(x); logits=self.head(self.norm(x)); loss=F.cross_entropy(logits.reshape(-1,logits.size(-1)),targets.reshape(-1)) if targets is not None else None; return logits,loss
 @torch.no_grad()
 def generate(self,idx,max_new_tokens=100,temperature=0.8):
  self.eval()
  for _ in range(max_new_tokens):
   logits,_=self(idx[:,-self.block_size:]); probs=F.softmax(logits[:,-1,:]/max(temperature,1e-5),dim=-1); idx=torch.cat((idx,torch.multinomial(probs,1)),dim=1)
  return idx
