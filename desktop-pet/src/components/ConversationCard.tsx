import { useState } from 'react'
import { summarizeConversation, markConversationRead } from '../middleware/api'
import '../styles/SummaryPanel.css'

interface Message {
    from: string
    text: string
    timestamp: number
}

interface Summary {
    who: string
    intent: string
    requirements: string[]
    urgency: string
    sentiment: string
    action_items: string[]
    one_liner: string
}

interface Conversation {
    sender: string
    conversation_id: string
    started_at: number
    last_activity: number
    messages: Message[]
    read: boolean
    summary: Summary | null
}

interface ConversationCardProps {
    conversation: Conversation
    onRead: () => void
}

function ConversationCard({ conversation, onRead }: ConversationCardProps) {
    const [summary, setSummary] = useState<Summary | null>(conversation.summary)
    const [loading, setLoading] = useState(false)
    const [expanded, setExpanded] = useState(false)

    const handleSummarize = async () => {
        setLoading(true)
        try {
            const result = await summarizeConversation(conversation.conversation_id)
            setSummary(result)
            await markConversationRead(conversation.conversation_id)
            onRead()
        } catch (err) {
            console.error('Failed to summarize:', err)
        }
        setLoading(false)
    }

    const handleClick = () => {
        if (!summary) {
            handleSummarize()
        } else {
            setExpanded(!expanded)
        }
        if (!conversation.read) {
            markConversationRead(conversation.conversation_id)
            onRead()
        }
    }

    const timeAgo = (ts: number) => {
        const seconds = Math.floor(Date.now() / 1000 - ts)
        if (seconds < 60) return 'just now'
        if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
        if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
        return `${Math.floor(seconds / 86400)}d ago`
    }

    const urgencyColor = (urgency: string) => {
        switch (urgency) {
            case 'high': return '#ff4757'
            case 'medium': return '#ffa502'
            case 'low': return '#2ed573'
            default: return '#a0a0a0'
        }
    }

    const messageCount = conversation.messages.length
    const lastMessage = conversation.messages[messageCount - 1]

    return (
        <div className={`conversation-card ${!conversation.read ? 'conversation-card--unread' : ''}`} onClick={handleClick}>
            <div className="conversation-card__header">
                <div className="conversation-card__avatar">
                    {conversation.sender.slice(-2)}
                </div>
                <div className="conversation-card__info">
                    <div className="conversation-card__sender">{conversation.sender}</div>
                    <div className="conversation-card__time">{timeAgo(conversation.last_activity)}</div>
                </div>
                {!conversation.read && <div className="conversation-card__dot" />}
            </div>

            {!summary && !loading && (
                <div className="conversation-card__preview">
                    <p className="conversation-card__last-msg">
                        {lastMessage ? lastMessage.text.slice(0, 80) + (lastMessage.text.length > 80 ? '...' : '') : 'No messages'}
                    </p>
                    <span className="conversation-card__msg-count">{messageCount} messages</span>
                </div>
            )}

            {loading && (
                <div className="conversation-card__loading">
                    <div className="conversation-card__spinner" />
                    <span>Summarizing with AI...</span>
                </div>
            )}

            {summary && (
                <div className={`conversation-card__summary ${expanded ? 'conversation-card__summary--expanded' : ''}`}>
                    <div className="conversation-card__one-liner">{summary.one_liner}</div>

                    {expanded && (
                        <>
                            <div className="conversation-card__detail">
                                <span className="conversation-card__label">Who:</span>
                                <span>{summary.who}</span>
                            </div>
                            <div className="conversation-card__detail">
                                <span className="conversation-card__label">Intent:</span>
                                <span>{summary.intent}</span>
                            </div>
                            <div className="conversation-card__detail">
                                <span className="conversation-card__label">Urgency:</span>
                                <span className="conversation-card__urgency" style={{ color: urgencyColor(summary.urgency) }}>
                                    {summary.urgency.toUpperCase()}
                                </span>
                            </div>

                            {summary.requirements.length > 0 && (
                                <div className="conversation-card__section">
                                    <span className="conversation-card__label">Requirements:</span>
                                    <ul className="conversation-card__list">
                                        {summary.requirements.map((req, i) => (
                                            <li key={i}>{req}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}

                            {summary.action_items.length > 0 && (
                                <div className="conversation-card__section">
                                    <span className="conversation-card__label">Action Items:</span>
                                    <ul className="conversation-card__list conversation-card__list--actions">
                                        {summary.action_items.map((item, i) => (
                                            <li key={i}>{item}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </>
                    )}

                    <div className="conversation-card__expand-hint">
                        {expanded ? 'click to collapse' : 'click for details'}
                    </div>
                </div>
            )}
        </div>
    )
}

export default ConversationCard
