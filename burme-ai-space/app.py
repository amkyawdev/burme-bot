"""
Burme AI - Gradio Space
HuggingFace Space for amkyawdev/kyaw-mm-v1 model
"""

import os
import gradio as gr

# Get API token from environment - will be set in Space secrets
HF_TOKEN = os.environ.get("HF_TOKEN", "") or os.environ.get("HF_TOKEN", "")
MODEL_ID = "amkyawdev/kyaw-mm-v1"

# System prompt
SYSTEM_PROMPT = """You are Burme AI, a helpful Burmese AI assistant. Respond in Burmese (မြန်မာဘာသာ) or English depending on the user's language. Be concise and friendly."""


def generate(prompt: str, history: list = None, max_tokens: int = 512) -> str:
    """Generate response using HuggingFace Inference API"""
    import requests
    
    if not HF_TOKEN:
        return "Error: HF_TOKEN not configured. ပါဋိပါ၊"
    
    # Build conversation context
    conversation = SYSTEM_PROMPT + "\n\n"
    
    if history:
        for user_msg, bot_msg in history:
            conversation += f"User: {user_msg}\nAssistant: {bot_msg}\n\n"
    
    conversation += f"User: {prompt}\nAssistant:"
    
    # Use the Inference API endpoint
    api_url = f"https://api-inference.huggingface.co/pipelines/text_generation/{MODEL_ID}"
    
    try:
        response = requests.post(
            api_url,
            headers={
                "Authorization": f"Bearer {HF_TOKEN}",
                "Content-Type": "application/json"
            },
            json={
                "inputs": conversation,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True,
                }
            },
            timeout=120
        )
        
        if response.status_code == 200:
            data = response.json()
            output = data[0].get("generated_text", "")
            # Extract response after "Assistant:"
            if "Assistant:" in output:
                output = output.split("Assistant:")[-1].strip()
            return output if output else "ပြန်ပါ မယ်။"
        elif response.status_code == 403:
            return "Error: မလုပ်ပါ။ Pro plan လိုအပ်ပါ။"
        else:
            return f"Error: {response.status_code}"
            
    except Exception as e:
        return f"Error: {str(e)}"


def chat(message: str, history: list):
    """Gradio chat function"""
    if not message.strip():
        return history, ""
    
    history = history or []
    history.append([message, "🤔 စဉ်းပါ..."])
    
    # Generate response
    response = generate(message, history[:-1])
    
    history[-1][1] = response
    
    return history, response


# Glassmorphism CSS
CSS = """
.gradio-container {
    background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%) !important;
    min-height: 100vh;
}

.main-title {
    background: linear-gradient(90deg, #a855f7, #06b6d4, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem !important;
    font-weight: bold !important;
}

.chat-message {
    border-radius: 16px !important;
}

.user-message {
    background: rgba(168, 85, 247, 0.2) !important;
    border: 1px solid rgba(168, 85, 247, 0.3) !important;
}

.bot-message {
    background: rgba(6, 182, 212, 0.15) !important;
    border: 1px solid rgba(6, 182, 212, 0.3) !important;
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
"""


with gr.Blocks(css=CSS, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Burme AI", elem_classes=["main-title"])
    gr.Markdown("### မြန်မာဘာသာ AI Assistant | Myanmar Chatbot")
    
    chatbot = gr.Chatbot(
        label="Chat History",
        height=500,
        bubble_full_width=False,
    )
    
    with gr.Row():
        msg = gr.Textbox(
            label="Message",
            placeholder="မင်္ဂလာပါ၊ ဘာပမ်းလိုပါ၊",
            lines=2,
            scale=4,
            show_label=False
        )
        send = gr.Button("📤 Send", variant="primary", scale=1)
    
    with gr.Row():
        clear = gr.Button("🗑️ Clear Chat")
        gr.Markdown("*First message may take time to load model*")
    
    # Event handlers
    send.click(chat, inputs=[msg, chatbot], outputs=[chatbot, msg])
    msg.submit(chat, inputs=[msg, chatbot], outputs=[chatbot, msg])
    clear.click(lambda: (None, None), outputs=[chatbot, msg])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)