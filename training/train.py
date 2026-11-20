"""Training and validation loop."""
from pathlib import Path
import torch
from brain.tokenizer import BPETokenizer
from brain.model import SpiderBrain
from training.dataset import load_text_files,encode_dataset,get_batch
from training.config import CONFIG
@torch.no_grad()
def evaluate(model,train_ids,val_ids,device):
 model.eval(); out={}
 for label,ids in (("train",train_ids),("val",val_ids)):
  losses=[]
  for _ in range(CONFIG["eval_batches"]):
   x,y=get_batch(ids,CONFIG["block_size"],CONFIG["batch_size"],device); _,loss=model(x,y); losses.append(loss.item())
  out[label]=sum(losses)/len(losses)
 model.train(); return out
def main():
 torch.manual_seed(CONFIG["seed"]); device="cuda" if torch.cuda.is_available() else "cpu"; print("Device:",device)
 text=load_text_files(["data/training.txt"]); tokenizer=BPETokenizer(CONFIG["vocab_size"]).train(text); train_ids,val_ids=encode_dataset(text,tokenizer)
 model=SpiderBrain(tokenizer.vocab_size,CONFIG["block_size"],CONFIG["embedding_dim"],CONFIG["heads"],CONFIG["layers"]).to(device); opt=torch.optim.AdamW(model.parameters(),lr=CONFIG["learning_rate"])
 for step in range(CONFIG["steps"]):
  x,y=get_batch(train_ids,CONFIG["block_size"],CONFIG["batch_size"],device); _,loss=model(x,y); opt.zero_grad(set_to_none=True); loss.backward(); torch.nn.utils.clip_grad_norm_(model.parameters(),1.0); opt.step()
  if step%CONFIG["eval_interval"]==0:
   metrics=evaluate(model,train_ids,val_ids,device); print(f"step {step} train={metrics['train']:.3f} val={metrics['val']:.3f}")
 Path("checkpoints").mkdir(exist_ok=True); tokenizer.save("checkpoints/tokenizer.json"); torch.save({"model_state":model.state_dict(),"config":CONFIG},"checkpoints/spider_brain_v0_2.pt"); print("Checkpoint saved.")
if __name__=="__main__": main()
