import { useState, useEffect, useRef } from 'react'
import { chatWithTamaBotchi } from '../middleware/api'

interface ChatMessage {
    role: 'user' | 'assistant'
    content: string
}

const GREETING: ChatMessage = {
    role: 'assistant',
    content:
        "Hi! I'm TamaBotchi, Jesh's personal AI assistant. I can help you schedule meetings, check reminders, summarize messages, or just chat. What do you need?",
}

function ChatView() {
    const [messages, setMessages] = useState<ChatMessage[]>([GREETING])
    const [input, setInput] = useState('')
    const [loading, setLoading] = useState(false)
    const bottomRef = useRef<HTMLDivElement>(null)
    const inputRef = useRef<HTMLTextAreaElement>(null)

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    const sendMessage = async () => {
        const text = input.trim()
        if (!text || loading) return

        const userMsg: ChatMessage = { role: 'user', content: text }
        const nextMessages = [...messages, userMsg]
        setMessages(nextMessages)
        setInput('')
        setLoading(true)

        try {
            // Build history from all messages after the initial greeting
            const history = nextMessages.slice(1).map((m) => ({
                role: m.role,
                content: m.content,
            }))
            // The last entry is the user message, remove it since we pass it separately
            const priorHistory = history.slice(0, -1)

            const result = await chatWithTamaBotchi(text, priorHistory)
            const reply: ChatMessage = { role: 'assistant', content: result.reply }
            setMessages((prev) => [...prev, reply])
        } catch {
            const errMsg: ChatMessage = {
                role: 'assistant',
                content: "Sorry, I couldn't connect right now. Make sure the TamaBotchi agent is running!",
            }
            setMessages((prev) => [...prev, errMsg])
        }

        setLoading(false)
        inputRef.current?.focus()
    }

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            sendMessage()
        }
    }

    const handleClear = () => {
        setMessages([GREETING])
        setInput('')
    }

    return (
        <div className="chat-view">
            <div className="chat-view__messages">
                {messages.map((msg, i) => (
                    <div
                        key={i}
                        className={`chat-view__bubble chat-view__bubble--${msg.role}`}
                    >
                        {msg.role === 'assistant' && (
                            <div className="chat-view__avatar">T</div>
                        )}
                        <div className="chat-view__text">{msg.content}</div>
                    </div>
                ))}
                {loading && (
                    <div className="chat-view__bubble chat-view__bubble--assistant">
                        <div className="chat-view__avatar">T</div>
                        <div className="chat-view__typing">
                            <span />
                            <span />
                            <span />
                        </div>
                    </div>
                )}
                <div ref={bottomRef} />
            </div>

            <div className="chat-view__footer">
                <button className="chat-view__clear-btn" onClick={handleClear} title="Clear chat">
                    ↺
                </button>
                <textarea
                    ref={inputRef}
                    className="chat-view__input"
                    placeholder="Ask TamaBotchi anything..."
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyDown={handleKeyDown}
                    rows={1}
                    disabled={loading}
                />
                <button
                    className="chat-view__send-btn"
                    onClick={sendMessage}
                    disabled={loading || !input.trim()}
                >
                    ↑
                </button>
            </div>
        </div>
    )
}

export default ChatView
