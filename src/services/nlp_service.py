import torch
from transformers import BertTokenizer, BertModel
from ..config import Config

class NLPService:
    def __init__(self):
        self.tokenizer = BertTokenizer.from_pretrained(Config.BERT_MODEL_NAME)
        self.model = BertModel.from_pretrained(Config.BERT_MODEL_NAME)
        self.device = torch.device(Config.DEVICE)
        self.model.to(self.device)
        self.model.eval()
    
    def get_prompt_embedding(self, prompt: str) -> torch.Tensor:
        """Process user prompt using BERT for contextual understanding"""
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=512,
            truncation=True,
            padding=True
        ).to(self.device)
        
        with torch.no_grad():
            outputs = self.model(**inputs)
            prompt_embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()
            
        return prompt_embedding