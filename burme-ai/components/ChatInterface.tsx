'use client'

import { useState, useRef, useEffect } from 'react'
import { marked } from 'marked'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

interface ChatProps {
  messages: ChatMessage[]
  onSendMessage: (content: string) => void
  isLoading: boolean
}

export function ChatInterface({ messages, onSendMessage, isLoading }: ChatProps) {
  const [input, setInput] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = Math.min(textareaRef.current.scrollHeight, 150) + 'px'
    }
  }, [input])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim())
      setInput('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text)
  }

  return (
    <div className="flex flex-col h-full max-w-3xl mx-auto px-4">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto py-4 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full min-h-[200px]">
            <p className="text-white/50 text-center">
              မင်္ဂလာပါ၊ ပါဋိပါ၊ သုံးပျော်ပါဆိုပြီး ရေးပါ။
            </p>
          </div>
        ) : (
          messages.map((message, index) => (
            <div
              key={index}
              className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'} animate-fade-in`}
            >
              <div
                className={`max-w-[85%] rounded-2xl px-4 py-3 glass ${
                  message.role === 'user'
                    ? 'bg-primary/20 border-primary/30 neon-purple'
                    : 'bg-surface border-white/10'
                }`}
              >
                <div className="flex items-start gap-3">
                  {message.role === 'assistant' && (
                    <div className="w-8 h-8 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-sm font-bold shrink-0">
                      AI
                    </div>
                  )}
                  <div
                    className={`markdown-content text-white/90 ${message.role === 'user' ? 'text-right' : ''}`}
                    dangerouslySetInnerHTML={{
                      __html: marked(message.content, { async: false }) as string,
                    }}
                  />
                </div>
                {message.role === 'assistant' && (
                  <button
                    onClick={() => copyToClipboard(message.content)}
                    className="mt-2 text-xs text-white/40 hover:text-white/70 transition-colors"
                  >
                    ကူးယူပါ
                  </button>
                )}
              </div>
            </div>
          ))
        )}

        {isLoading && (
          <div className="flex justify-start animate-fade-in">
            <div className="glass rounded-2xl px-4 py-3 border border-white/10">
              <div className="flex items-center gap-3">
                <div className="w-8 h-8 rounded-full bg-gradient-to-r from-primary to-secondary flex items-center justify-center text-sm font-bold shrink-0">
                  AI
                </div>
                <div className="flex gap-1">
                  <span className="w-2 h-2 rounded-full bg-primary animate-pulse-slow" />
                  <span className="w-2 h-2 rounded-full bg-primary animate-pulse-slow" style={{ animationDelay: '0.2s' }} />
                  <span className="w-2 h-2 rounded-full bg-primary animate-pulse-slow" style={{ animationDelay: '0.4s' }} />
                </div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} className="py-4">
        <div className="glass rounded-2xl p-2 neon-cyan focus-within:neon-purple transition-all">
          <div className="flex items-end gap-2">
            <textarea
              ref={textareaRef}
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="မင်္ဂလာပါ၊ ဘာပမ်းပါ၊"
              className="flex-1 bg-transparent text-white placeholder-white/40 px-3 py-2 resize-none outline-none max-h-[150px]"
              rows={1}
            />
            <button
              type="submit"
              disabled={!input.trim() || isLoading}
              className="w-10 h-10 rounded-xl bg-gradient-to-r from-primary to-secondary flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed hover:opacity-80 transition-all shrink-0"
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
              </svg>
            </button>
          </div>
        </div>
      </form>
    </div>
  )
}