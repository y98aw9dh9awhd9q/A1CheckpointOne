import torch, json
from pathlib import Path

dirOfAI = Path(__file__).parent

class chatModel(torch.nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_size, num_layers):
        super().__init__()
        self.hidden_size, self.num_layers = hidden_size, num_layers
        self.embed = torch.nn.Embedding(vocab_size, embed_dim)
        self.lstm = torch.nn.LSTM(embed_dim, hidden_size, num_layers, batch_first=True)
        self.fc = torch.nn.Linear(hidden_size, vocab_size)
        if embed_dim == hidden_size:
            self.fc.weight = self.embed.weight

    def forward(self, x, hidden=None):
        out, hidden = self.lstm(self.embed(x), hidden)
        return self.fc(out), hidden

deviceCudaMaybe = torch.device("cuda" if torch.cuda.is_available() else "cpu")
aiModel = torch.load(dirOfAI / "model.pt", map_location=deviceCudaMaybe)
vocabulary = json.loads((dirOfAI / "modelVocab.json").read_text())
charactersToIndex, indexToChar = vocabulary["char2idx"], vocabulary["idx2char"]
configurator = aiModel["config"]
THEBIGMODEL = chatModel(aiModel["vocab_size"], configurator["embed_dim"], configurator["hidden_size"], configurator["num_layers"]).to(deviceCudaMaybe)
THEBIGMODEL.load_state_dict(aiModel["model_state"])
THEBIGMODEL.eval()

@torch.no_grad()
def generateText(text: str, length: int = 100, temperature: float = 0.001) -> str:
    chars = [charactersToIndex[c] for c in text if c in charactersToIndex] or [0]
    h = (torch.zeros(configurator["num_layers"], 1, configurator["hidden_size"], device=deviceCudaMaybe),
         torch.zeros(configurator["num_layers"], 1, configurator["hidden_size"], device=deviceCudaMaybe))
    if len(chars) > 1:
        _, h = THEBIGMODEL(torch.tensor([chars[:-1]], device=deviceCudaMaybe), h)
    cur = torch.tensor([[chars[-1]]], device=deviceCudaMaybe)
    out = list(text)
    for _ in range(length):
        logits, h = THEBIGMODEL(cur, h)
        probs = torch.softmax(logits[0, -1] / temperature, dim=-1)
        idx = torch.multinomial(probs, 1).item()
        out.append(indexToChar[str(idx)])
        cur = torch.tensor([[idx]], device=deviceCudaMaybe)
    return "".join(out).strip()