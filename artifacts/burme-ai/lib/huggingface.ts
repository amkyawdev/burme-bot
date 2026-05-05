const HF_API_URL = process.env.HUGGINGFACE_MODEL_URL || 'https://api-inference.huggingface.co/models/amkyawdev/kyaw-mm-v1'
const HF_API_KEY = process.env.HUGGINGFACE_API_KEY

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export async function* streamChat(messages: ChatMessage[]): AsyncGenerator<string> {
  const prompt = buildPrompt(messages)

  const response = await fetch(HF_API_URL, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${HF_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      inputs: prompt,
      parameters: {
        max_new_tokens: 512,
        temperature: 0.7,
        top_p: 0.9,
        do_sample: true,
      },
      options: {
        use_cache: false,
      },
    }),
  })

  if (!response.ok) {
    const error = await response.text()
    throw new Error(`HF API Error: ${response.status} - ${error || 'Model is loading, please wait...'}`)
  }

  if (!response.body) {
    throw new Error('No response body')
  }

  const reader = response.body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break

    buffer += decoder.decode(value, { stream: true })
    const lines = buffer.split('\n')
    buffer = lines.pop() || ''

    for (const line of lines) {
      if (line.startsWith('data: ')) {
        const data = line.slice(6)
        try {
          const parsed = JSON.parse(data)
          if (parsed.token?.text) {
            yield parsed.token.text
          }
        } catch {
          // Skip invalid JSON
        }
      }
    }
  }
}

function buildPrompt(messages: ChatMessage[]): string {
  const systemPrompt = `You are Burme AI, a helpful Burmese AI assistant. Respond in Burmese (မြန်မာဘာသာ) or English depending on the user's language. Be concise and helpful.`

  const conversation = messages
    .map((m) => `${m.role === 'user' ? 'User' : 'Assistant'}: ${m.content}`)
    .join('\n\n')

  return `${systemPrompt}\n\n${conversation}\n\nAssistant:`
}

export async function sendChatMessage(messages: ChatMessage[]): Promise<string> {
  let fullResponse = ''
  for await (const chunk of streamChat(messages)) {
    fullResponse += chunk
  }
  return fullResponse
}