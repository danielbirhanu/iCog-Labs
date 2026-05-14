import torch
from model import GPTLanguageModel


device = "cuda" if torch.cuda.is_available() else "cpu"

checkpoint = torch.load("gpt_shakespeare.pth", map_location=device)

stoi = checkpoint["stoi"]
itos = checkpoint["itos"]
vocab_size = checkpoint["vocab_size"]
block_size = checkpoint["block_size"]

decode = lambda l: "".join([itos[i] for i in l])


model = GPTLanguageModel(
    vocab_size=vocab_size,
    block_size=block_size,
    n_embd=128,
    num_heads=4,
    num_layers=4,
    dropout=0.2
)

model.load_state_dict(checkpoint["model_state_dict"])
model.to(device)
model.eval()


context = torch.zeros((1, 1), dtype=torch.long, device=device)

output = model.generate(context, max_new_tokens=1000)[0].tolist()

print(decode(output))