"""
Burme AI - Gradio Space (Fast API Version)
Uses HuggingFace Inference API for faster response
"""

import os
import gradio as gr

# Get API token from environment
HF_TOKEN = os.environ.get("HF_TOKEN", "")
MODEL_ID = "amkyawdev/kyaw-mm-v1"

# System prompt for Burmese assistant
SYSTEM_PROMPT = """You are Burme AI, a helpful Burmese AI assistant. Respond in Burmese (မြန်မာဘာသာ) or English depending on the user's language. Be concise and friendly."""


def generate(prompt: str, history: list = None, max_tokens: int = 512) -> str:
    """Generate response using Inference API"""
    import requests
    
    if not HF_TOKEN:
        return "Error: HF_TOKEN not set. Please configure your HuggingFace token."
    
    # Build conversation
    conversation = SYSTEM_PROMPT + "\n\n"
    
    if history:
        for user_msg, bot_msg in history:
            conversation += f"User: {user_msg}\nAssistant: {bot_msg}\n\n"
    
    conversation += f"User: {prompt}\nAssistant:"
    
    # Call Inference API
    api_url = f"https://api-inference.huggingface.co/pipelines/text_generation/{MODEL_ID}"
    
    try:
        response = requests.post(
            api_url,
            headers={"Authorization": f"Bearer {HF_TOKEN}"},
            json={
                "inputs": conversation,
                "parameters": {
                    "max_new_tokens": max_tokens,
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True,
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            data = response.json()
            output = data[0]["generated_text"]
            # Extract response after "Assistant:"
            if "Assistant:" in output:
                output = output.split("Assistant:")[-1].strip()
            return output
        else:
            return f"Error: {response.status_code} - {response.text}"
            
    except Exception as e:
        return f"Error: {str(e)}"


def chat(message: str, history: list):
    """Gradio chat function"""
    if not message.strip():
        return history, ""
    
    history = history or []
    history.append([message, "Loading..."])
    
    # Generate response
    response = generate(message, history[:-1])
    
    history[-1][1] = response
    
    return history, response


# CSS for glassmorphism
CSS = """
.gradio-container {
    background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%) !important;
}

.main-title {
    background: linear-gradient(90deg, #a855f7, #06b6d4, #22d3ee);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.chat-message {
    border-radius: 16px !important;
}
"""


with gr.Blocks(css=CSS, theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Burme AI")
    gr.Markdown("### မြန်မာဘာသာ AI Assistant")
    
    chatbot = gr.Chatbot(height=500)
    
    with gr.Row():
        msg = gr.Textbox(label="Message", placeholder="မင်္ဂလာပါ၊", lines=2, scale=4)
        send = gr.Button("Send", variant="primary")
    
    clear = gr.Button("Clear Chat")
    
    send.click(chat, inputs=[msg, chatbot], outputs=[chatbot, msg])
    msg.submit(chat, inputs=[msg, chatbot], outputs=[chatbot, msg])
    clear.click(lambda: (None, None), outputs=[chatbot, msg])


if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)