import streamlit as st
st.set_page_config(page_title="Smart Immunization Assistant")

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
from vaccine_utils import load_vaccine_data, extract_age, recommend_vaccines
from prompt_templates import generate_response_prompt
import torch

print("GPU Available:", torch.cuda.is_available())
print("Current GPU:", torch.cuda.get_device_name(0))


@st.cache_resource
def load_model():
    model_id = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",             # Auto maps to GPU if available
        torch_dtype=torch.float16      # FP16: balanced memory & speed
    )

    return pipeline("text-generation", model=model, tokenizer=tokenizer)


chat = load_model()

st.title("Smart Immunization Assistant")


user_query = st.text_input("Ask about your child's vaccination needs:")

if user_query:
    data = load_vaccine_data()
    age_str = extract_age(user_query)
    matched_vaccines = recommend_vaccines(age_str, data) if age_str else []
    prompt = generate_response_prompt(user_query, matched_vaccines)

    with st.spinner("Thinking..."):
        result = chat(prompt, max_new_tokens=400)[0]['generated_text']
        response = result.split(prompt)[-1].strip()
        st.markdown(response)

