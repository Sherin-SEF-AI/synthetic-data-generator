"""
AI-Powered Data Generator

Uses AI models to generate realistic text content.
"""

import random
from typing import Any, Dict, List, Optional
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
from .base_generator import BaseGenerator


class AIGenerator(BaseGenerator):
    """Generator using AI models for realistic text generation."""
    
    def __init__(self, seed: Optional[int] = None, model_name: str = "gpt2"):
        super().__init__(seed)
        self.model_name = model_name
        self.text_generator = None
        self._load_model()
    
    def _load_model(self):
        """Load the AI model for text generation."""
        try:
            # Use a smaller model for Hugging Face Spaces
            if self.model_name == "gpt2":
                self.text_generator = pipeline(
                    "text-generation",
                    model="gpt2",
                    tokenizer="gpt2",
                    max_length=100,
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=50256
                )
            else:
                # Fallback to a smaller model
                self.text_generator = pipeline(
                    "text-generation",
                    model="distilgpt2",
                    max_length=50,
                    do_sample=True,
                    temperature=0.7
                )
        except Exception as e:
            print(f"Warning: Could not load AI model: {e}")
            self.text_generator = None
    
    def generate(self, count: int, prompt: str = "", text_type: str = "description", **kwargs) -> List[str]:
        """Generate AI-powered text content."""
        if not self.text_generator:
            # Fallback to basic text generation
            return [f"AI Generated Text {i+1}" for i in range(count)]
        
        data = []
        
        for i in range(count):
            try:
                if text_type == "description":
                    generated_text = self._generate_description(prompt, **kwargs)
                elif text_type == "product_name":
                    generated_text = self._generate_product_name(prompt, **kwargs)
                elif text_type == "review":
                    generated_text = self._generate_review(prompt, **kwargs)
                elif text_type == "email":
                    generated_text = self._generate_email_content(prompt, **kwargs)
                else:
                    generated_text = self._generate_generic_text(prompt, **kwargs)
                
                data.append(generated_text)
            except Exception as e:
                # Fallback to basic text
                data.append(f"Generated Content {i+1}")
        
        return data
    
    def _generate_description(self, prompt: str = "", **kwargs) -> str:
        """Generate product descriptions."""
        if not prompt:
            prompts = [
                "This product is",
                "The features include",
                "This innovative solution",
                "Our latest offering",
                "This high-quality item"
            ]
            prompt = random.choice(prompts)
        
        try:
            result = self.text_generator(
                prompt,
                max_length=len(prompt.split()) + 20,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
            return result[0]['generated_text'].strip()
        except:
            return f"{prompt} designed to meet your needs with excellent quality and performance."
    
    def _generate_product_name(self, prompt: str = "", **kwargs) -> str:
        """Generate product names."""
        if not prompt:
            prompts = [
                "Smart",
                "Pro",
                "Ultra",
                "Advanced",
                "Premium"
            ]
            prompt = random.choice(prompts)
        
        try:
            result = self.text_generator(
                prompt,
                max_length=len(prompt.split()) + 5,
                num_return_sequences=1,
                temperature=0.8,
                do_sample=True
            )
            return result[0]['generated_text'].strip()
        except:
            return f"{prompt} Product {random.randint(100, 999)}"
    
    def _generate_review(self, prompt: str = "", **kwargs) -> str:
        """Generate product reviews."""
        if not prompt:
            prompts = [
                "This product is amazing",
                "I love this item",
                "Great quality and",
                "Highly recommend this",
                "Excellent value for"
            ]
            prompt = random.choice(prompts)
        
        try:
            result = self.text_generator(
                prompt,
                max_length=len(prompt.split()) + 15,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
            return result[0]['generated_text'].strip()
        except:
            return f"{prompt} and I would definitely buy it again!"
    
    def _generate_email_content(self, prompt: str = "", **kwargs) -> str:
        """Generate email content."""
        if not prompt:
            prompts = [
                "Dear customer,",
                "Thank you for your",
                "We are pleased to",
                "Your order has been",
                "We would like to"
            ]
            prompt = random.choice(prompts)
        
        try:
            result = self.text_generator(
                prompt,
                max_length=len(prompt.split()) + 25,
                num_return_sequences=1,
                temperature=0.6,
                do_sample=True
            )
            return result[0]['generated_text'].strip()
        except:
            return f"{prompt} and we appreciate your business."
    
    def _generate_generic_text(self, prompt: str = "", **kwargs) -> str:
        """Generate generic text content."""
        if not prompt:
            prompt = "The following information"
        
        try:
            result = self.text_generator(
                prompt,
                max_length=len(prompt.split()) + 10,
                num_return_sequences=1,
                temperature=0.7,
                do_sample=True
            )
            return result[0]['generated_text'].strip()
        except:
            return f"{prompt} is important for your understanding."
