'use client'

import { useState, useCallback } from 'react'
import { ChatInterface, ChatMessage } from '@/components/ChatInterface'

export default function Home() {
  const [messages, setMessages] = useState<ChatMessage[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleSendMessage = useCallback(async (content: string) => {
    const newMessages: ChatMessage[] = [...messages, { role: 'user', content }]
    setMessages(newMessages)
    setIsLoading(true)
    setError(null)

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ messages: newMessages }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.error || 'Something went wrong')
      }

      setMessages([...newMessages, { role: 'assistant', content: data.response }])
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to get response')
    } finally {
      setIsLoading(false)
    }
  }, [messages])

  const clearChat = () => {
    setMessages([])
    setError(null)
  }

  return (
    <main className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="py-6 px-4 border-b border-white/5">
        <div className="max-w-3xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-primary via-secondary to-accent bg-clip-text text-transparent text-glow-purple">
              Burme AI
            </h1>
            <p className="text-white/50 text-sm mt-1">Myanmar-first intelligent assistant</p>
          </div>
          {messages.length > 0 && (
            <button
              onClick={clearChat}
              className="text-sm text-white/40 hover:text-white/70 transition-colors"
            >
              ပြန်ရှင်းပါ
            </button>
          )}
        </div>
      </header>

      {/* Chat Area */}
      <div className="flex-1 flex flex-col">
        <ChatInterface
          messages={messages}
          onSendMessage={handleSendMessage}
          isLoading={isLoading}
        />
      </div>

      {/* Error Toast */}
      {error && (
        <div className="fixed bottom-20 left-1/2 -translate-x-1/2 glass rounded-xl px-4 py-2 border border-red-500/30 bg-red-500/10">
          <p className="text-red-400 text-sm">{error}</p>
        </div>
      )}
    </main>
  )
}