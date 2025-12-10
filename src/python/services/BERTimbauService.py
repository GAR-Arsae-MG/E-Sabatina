#! python3

# Authors:  Túlio Ferreira Horta - (TFH, Duke).
# Last modification: DUKE-10_dec_25

import torch
import numpy as np
from typing import List, Dict, Tuple
from transformers import AutoTokenizer, AutoModel


class BERTimbauService:
    
    def __init__(self, model_name: str = "neuralmind/bert-base-portuguese-cased"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name)
        self.model.eval()
        
        # Move to GPU if available
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
    
    def get_sentence_embedding(self, sentence: str) -> List[float]:
        # Tokenize
        inputs = self.tokenizer(
            sentence,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512
        )
        
        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Extract [CLS] token embedding (first token)
        cls_embedding = outputs.last_hidden_state[0, 0, :].cpu().numpy()
        
        return cls_embedding.tolist()
    
    def get_token_embeddings(self, sentence: str) -> Dict:
        # Tokenize with offset mapping to track original positions
        inputs = self.tokenizer(
            sentence,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=512,
            return_offsets_mapping=True
        )
        
        offset_mapping = inputs.pop("offset_mapping")[0]
        
        # Move to device
        inputs = {k: v.to(self.device) for k, v in inputs.items()}
        
        # Get embeddings
        with torch.no_grad():
            outputs = self.model(**inputs)
        
        # Extract all token embeddings
        token_embeddings = outputs.last_hidden_state[0].cpu().numpy()
        
        # Get token strings
        tokens = self.tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
        
        # Build result structure
        result = {
            "sentence": sentence,
            "tokens": [],
            "sentence_embedding": token_embeddings[0].tolist()  # [CLS] token
        }
        
        # Skip [CLS] and [SEP] tokens, keep actual content tokens
        for idx, (token, embedding, offset) in enumerate(
            zip(tokens[1:-1], token_embeddings[1:-1], offset_mapping[1:-1])
        ):
            # Clean up subword tokens (##)
            clean_token = token.replace("##", "")
            
            result["tokens"].append({
                "text": clean_token,
                "embedding": embedding.tolist(),
                "position": idx,
                "char_start": int(offset[0]),
                "char_end": int(offset[1])
            })
        
        return result
        
    def compute_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        vec1 = np.array(embedding1)
        vec2 = np.array(embedding2)
        
        # Cosine similarity
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
        
        similarity = dot_product / (norm1 * norm2)
        return float(similarity)

