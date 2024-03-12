from transformers import AutoModelForCausalLM, AutoTokenizer
import transformers
import torch
from langchain.llms.huggingface_pipeline import HuggingFacePipeline

model_id = "mistralai/Mixtral-8x7B-v0.1"


if __name__ == "__main__":
    print("running as daemon")
    model_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"
    hf = HuggingFacePipeline.from_model_id(
        model_id="mistralai/Mistral-7B-v0.1", task="text-generation", pipeline_kwargs={"max_new_tokens": 200, "pad_token_id": 50256},
    )
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model = AutoModelForCausalLM.from_pretrained(model_id, load_in_4bit=True)

    text = "Hello my name is"
    inputs = tokenizer(text, return_tensors="pt")

    outputs = model.generate(**inputs, max_new_tokens=20)
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
