"""Trainable byte-level BPE tokenizer."""
from collections import Counter
class BPETokenizer:
    def __init__(self, vocab_size=512):
        if vocab_size < 256: raise ValueError("vocab_size must be at least 256")
        self.vocab_size=vocab_size; self.merges=[]; self.token_bytes={i:bytes([i]) for i in range(256)}
    def train(self,text):
        seqs=[list(text.encode("utf-8"))]; nxt=256
        while nxt<self.vocab_size:
            counts=Counter()
            for s in seqs: counts.update(zip(s,s[1:]))
            if not counts: break
            pair,freq=counts.most_common(1)[0]
            if freq<2: break
            self.merges.append(pair); a,b=pair; self.token_bytes[nxt]=self.token_bytes[a]+self.token_bytes[b]
            outseq=[]
            for s in seqs:
                out=[]; i=0
                while i<len(s):
                    if i+1<len(s) and (s[i],s[i+1])==pair: out.append(nxt); i+=2
                    else: out.append(s[i]); i+=1
                outseq.append(out)
            seqs=outseq; nxt+=1
        return self
    def encode(self,text):
        ids=list(text.encode("utf-8"))
        for new_id,pair in enumerate(self.merges,256):
            out=[]; i=0
            while i<len(ids):
                if i+1<len(ids) and (ids[i],ids[i+1])==pair: out.append(new_id); i+=2
                else: out.append(ids[i]); i+=1
            ids=out
        return ids
    def decode(self,ids): return b"".join(self.token_bytes[int(i)] for i in ids).decode("utf-8",errors="replace")
    @property
    def vocab_size(self): return 256+len(self.merges)
    def save(self,path):
        import json
        with open(path,"w",encoding="utf8") as f: json.dump({"vocab_size":self.vocab_size,"merges":self.merges},f)
    @classmethod
    def load(cls,path):
        import json
        with open(path,encoding="utf8") as f: d=json.load(f)
        obj=cls(d["vocab_size"]); obj.merges=[tuple(x) for x in d["merges"]]
        obj.token_bytes={i:bytes([i]) for i in range(256)}
        for n,(a,b) in enumerate(obj.merges,256): obj.token_bytes[n]=obj.token_bytes[a]+obj.token_bytes[b]
        return obj
