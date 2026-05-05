import { NextRequest, NextResponse } from 'next/server'

interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export async function POST(req: NextRequest) {
  try {
    const { messages } = await req.json() as { messages: ChatMessage[] }

    if (!messages || !Array.isArray(messages)) {
      return NextResponse.json({ error: 'Invalid messages' }, { status: 400 })
    }

    const HF_API_URL = process.env.HUGGINGFACE_MODEL_URL || 'https://api-inference.huggingface.co/models/amkyawdev/kyaw-mm-v1'
    const HF_API_KEY = process.env.HUGGINGFACE_API_KEY

    if (!HF_API_KEY) {
      return NextResponse.json(
        { error: 'HUGGINGFACE_API_KEY not configured' },
        { status: 500 }
      )
    }

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
      return NextResponse.json(
        { error: error || 'Model is loading, please wait...' },
        { status: response.status }
      )
    }

    const data = await response.json()
    const generated_text = data[0]?.generated_text || ''

    // Extract the response (after "Assistant:")
    const responsePart = generated_text.split('Assistant:').pop() || generated_text
    const cleanResponse = responsePart.trim()

    return NextResponse.json({ response: cleanResponse })
  } catch (error) {
    console.error('Chat API error:', error)
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    )
  }
}

function buildPrompt(messages: ChatMessage[]): string {
  const systemPrompt = `You are Burme AI, a helpful Burmese AI assistant. Respond in Burmese (မြန်မာဘာသာ) or English depending on the user's language. Be concise and helpful.`

  const conversation = messages
    .map((m) => `${m.role === 'user' ? 'User' : 'Assistant'}: ${m.content}`)
    .join('\n\n')

  return `${systemPrompt}\n\n${conversation}\n\nAssistant:`
}