# 🤖 Burme AI

## မြန်မာဘာသာ AI Chatbot

Burme AI သည့် မြန်မာစကားပါ AI assistant ဖြစ်ပါ။

### 🔗 Links

- 🌐 **Web App**: [Vercel](https://vercel.com) မှာ deploy လုပ်ပါ
- 🤖 **HuggingFace Space**: [amkyawdev/burme-ai](https://huggingface.co/spaces/amkyawdev/burme-ai)
- 📄 **Model**: [amkyawdev/kyaw-mm-v1](https://huggingface.co/amkyawdev/kyaw-mm-v1)

### Features

- 🗣️ မြန်မာစကားပါ
- 🌙 Dark theme ဖြစ်တဲ့ glassmorphism UI
- 📱 Mobile responsive
- 🔄 Real-time streaming

### Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: HuggingFace Inference API
- **Model**: amkyawdev/kyaw-mm-v1 (Llama-3 8B)

### Project Structure

```
burme-ai/              # Next.js web app
├── app/              # App Router pages
├── components/       # React components
└── tailwind.config.js

burme-ai-space/       # HuggingFace Space
├── app_api.py         # Gradio app
├── Dockerfile        # Docker config
└── README.md
```

### Environment Variables

| Variable | Description |
|----------|------------|
| `HUGGINGFACE_API_KEY` | HuggingFace API Token |
| `HUGGINGFACE_MODEL_URL` | Model API URL |

### Local Development

```bash
# Next.js
cd burme-ai
npm install
npm run dev

# Docker
cd burme-ai-space
docker build -t burme-ai .
docker run -p 7860:7860 -e HF_TOKEN="..." burme-ai
```

### သုံးပါ

"မင်္ဂလာပါ" လို့ ရေးပါ။

### License

[Apache 2.0](./LICENSE)