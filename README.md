# Spider Intelligence

Experimental AI project. Spider Brain uses random initialization and a custom byte-level BPE tokenizer.

## V0.2
- BPE tokenizer
- Text dataset loader
- Train/validation split
- Random next-token batches
- Small causal Transformer
- Gradient clipping and validation-loss monitoring
- Checkpoint and tokenizer saving

## Colab
Open `notebooks/SpiderBrain_V0_2.ipynb`, select a GPU runtime if available, and run all cells. Add larger, diverse, legally obtained text to `data/training.txt` before meaningful training.

This starter corpus is only a demonstration; this model is not a conversational assistant.
