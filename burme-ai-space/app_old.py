"""
Burme AI - Gradio Space
Myanmar AI Chatbot using amkyawdev/kyaw-mm-v1 model
"""

import os
import warnings
warnings.filterwarnings('ignore')

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import gradio as gr

# Model configuration
MODEL_NAME = "amkyawdev/kyaw-mm-v1"
MAX_NEW_TOKENS = 512
TEMPERATURE = 0.7
TOP_P = 0.9

# Global variables to store model and tokenizer
model = None
tokenizer = None
is_loaded = False


def load_model():
    """Load the model and tokenizer"""
    global model, tokenizer, is_loaded
    
    if is_loaded:
        return True
    
    try:
        print(f"Loading model: {MODEL_NAME}")
        
        # Configure quantization
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        # Load tokenizer
        tokenizer = AutoTokenizer.from_pretrained(
            MODEL_NAME,
            trust_remote_code=True
        )
        
        # Set padding token
        if tokenizer.pad_token is None:
            tokenizer.pad_token = tokenizer.eos_token
        
        # Load model with quantization
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_NAME,
            quantization_config=quantization_config,
            device_map="auto",
            trust_remote_code=True,
            torch_dtype=torch.float16
        )
        
        is_loaded = True
        print("Model loaded successfully!")
        return True
        
    except Exception as e:
        print(f"Error loading model: {e}")
        return False


def generate_response(prompt: str, history: list = None) -> str:
    """Generate response from the model"""
    global model, tokenizer
    
    if not is_loaded:
        if not load_model():
            return "Error: Could not load model. Please try again."
    
    try:
        # Build conversation context
        conversation = prompt
        
        if history:
            for user_msg, bot_msg in history:
                conversation += f"\n\nUser: {user_msg}\nAssistant: {bot_msg}"
        
        conversation += "\n\nAssistant:"
        
        # Tokenize input
        inputs = tokenizer(
            conversation,
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=2048
        )
        
        # Move to same device as model
        inputs = {k: v.to(model.device) for k, v in inputs.items()}
        
        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=MAX_NEW_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                do_sample=True,
                pad_token_id=tokenizer.pad_token_id,
                eos_token_id=tokenizer.eos_token_id,
            )
        
        # Decode response
        full_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
        
        # Extract just the response part
        response = full_output[len(conversation):].strip()
        
        # Clean up response
        if "User:" in response:
            response = response.split("User:")[0].strip()
        
        return response if response else "Sorry, I couldn't generate a response."
        
    except Exception as e:
        print(f"Error generating: {e}")
        return f"Error: {str(e)}"


def chat(message: str, history: list):
    """Gradio chat function"""
    if not message.strip():
        return history, ""
    
    # Add user message to history
    history = history or []
    history.append([message, ""])
    
    # Generate response
    response = generate_response(message, history)
    
    # Update history
    history[-1][1] = response
    
    return history, response


# Custom CSS for ruv.io style
CSS = """
.gradio-container {
    background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%) !important;
}

.main-title {
    font-family: 'Inter', sans-serif;
    background: linear-gradient(90deg, #a855f7, #06b6d4, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 0 30px rgba(168, 85, 247, 0.5);
}

.chatbot .message {
    border-radius: 16px !important;
}

.user-message {
    background: rgba(168, 85, 247, 0.2) !important;
    border: 1px solid rgba(168, 85, 247, 0.3) !important;
}

.bot-message {
    background: rgba(6, 182, 212, 0.1) !important;
    border: 1px solid rgba(6, 182, 212, 0.2) !important;
}

.input-area textarea {
    background: rgba(255, 255, 255, 0.05) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: 12px !important;
    color: white !important;
}

.input-area textarea::placeholder {
    color: rgba(255, 255, 255, 0.4) !important;
}

.submit-button {
    background: linear-gradient(135deg, #a855f7, #06b6d4) !important;
    border: none !important;
}

.clear-button {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
}
"""


# Gradio Interface
with gr.Blocks(css=CSS, theme=gr.themes.Soft()) as demo:
    gr.Markdown("""
    # 🤖 Burme AI
    ### မြန်မာဘာသာ AI စကားပါးစပ်ပါ
    """, elem_classes=["main-title"])
    
    gr.Markdown("*First message will load the model (may take 1-2 minutes)*")
    
    chatbot = gr.Chatbot(
        label="Chat History",
        bubble_full_width=False,
        height=500,
        avatar_images=(None, None),
    )
    
    with gr.Row():
        msg_input = gr.Textbox(
            label="Message",
            placeholder="မင်္ဂလာပါ၊ ဘာပမ်းလိုပါ၊",
            lines=2,
            scale=4,
        )
        send_btn = gr.Button("📤 Send", variant="primary", scale=1)
    
    with gr.Row():
        clear_btn = gr.Button("🗑️ Clear", variant="secondary")
    
    # Event handlers
    send_btn.click(chat, inputs=[msg_input, chatbot], outputs=[chatbot, msg_input])
    msg_input.submit(chat, inputs=[msg_input, chatbot], outputs=[chatbot, msg_input])
    clear_btn.click(lambda: (None, None), outputs=[chatbot, msg_input])


if __name__ == "__main__":
    print("Starting Burme AI Space...")
    print(f"Model: {MODEL_NAME}")
    demo.launch(server_name="0.0.0.0", server_port=7860)