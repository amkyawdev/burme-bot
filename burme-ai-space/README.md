# 🤖 Burme AI Space

## မြန်မာဘာသာ AI Chatbot

HuggingFace Space သည့် မြန်မာစကားပါ AI chatbot ပါ။ [amkyawdev/kyaw-mm-v1](https://huggingface.co/amkyawdev/kyaw-mm-v1) model သုံးပါ။

### Features

- 🗣️ မြန်မာဘာသာ စကားပါ
- 🌙 Dark theme ဖြစ်တဲ့ glassmorphism UI
- 📱 Mobile responsive
- 🔄 Real-time streaming response
- 🗑️ Clear chat button

### Tech Stack

- [Gradio](https://gradio.app/) - UI Framework
- [HuggingFace Inference API](https://huggingface.co/inference-api) - Model API
- Python 3.10+

### Local Run

```bash
# Build Docker
docker build -t burme-ai ./burme-ai-space

# Run
docker run -d -p 7860:7860 \
  -e HF_TOKEN="your_huggingface_token" \
  burme-ai
```

### Environment Variables

| Variable | Description |
|----------|------------|
| `HF_TOKEN` | HuggingFace API Token (required) |

### Deploy to HuggingFace Spaces

1. Create new Space: https://huggingface.co/spaces/new
2. Select Gradio SDK
3. Upload files from `burme-ai-space/` folder
4. Set `HF_TOKEN` in Space settings

### သုံးပါ

သုံးသူပါ၊ "မင်္ဂလာပါ" လို့ ရေးပါ။

### License

Apache 2.0