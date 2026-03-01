import { useState, useEffect, useCallback } from 'react'
import ConversationCard from './ConversationCard'
import CalendarView from './CalendarView'
import ChatView from './ChatView'
import { fetchAllConversations, markAllRead, summarizeAll } from '../middleware/api'
import '../styles/SummaryPanel.css'

type PanelTab = 'messages' | 'calendar' | 'chat'

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

function SummaryPanel() {
    const [activeTab, setActiveTab] = useState<PanelTab>('messages')
    const [conversations, setConversations] = useState<Conversation[]>([])
    const [unreadCount, setUnreadCount] = useState(0)
    const [loading, setLoading] = useState(true)
    const [summarizingAll, setSummarizingAll] = useState(false)

    const loadConversations = useCallback(async () => {
        try {
            const data = await fetchAllConversations()
            const sorted = (data.conversations || []).sort(
                (a: Conversation, b: Conversation) => b.last_activity - a.last_activity
            )
            setConversations(sorted)
            setUnreadCount(data.unread_count || 0)
        } catch (err) {
            console.error('Failed to load conversations:', err)
        }
        setLoading(false)
    }, [])

    useEffect(() => {
        loadConversations()
        const interval = setInterval(loadConversations, 8000)
        return () => clearInterval(interval)
    }, [loadConversations])

    const handleClose = () => {
        if (window.electronAPI) {
            window.electronAPI.closeSummary()
        }
    }

    const handleMarkAllRead = async () => {
        await markAllRead()
        loadConversations()
    }

    const handleSummarizeAll = async () => {
        setSummarizingAll(true)
        try {
            await summarizeAll()
            await loadConversations()
        } catch (err) {
            console.error('Failed to summarize all:', err)
        }
        setSummarizingAll(false)
    }

    return (
        <div className="summary-panel">
            <div className="summary-panel__header">
                <div className="summary-panel__title-row">
                    <div className="summary-panel__icon">🐰</div>
                    <h2 className="summary-panel__title">TamaBotchi</h2>
                </div>
                <button className="summary-panel__close" onClick={handleClose}>✕</button>
            </div>

            <div className="summary-panel__tabs">
                <button
                    className={`summary-panel__tab ${activeTab === 'messages' ? 'summary-panel__tab--active' : ''}`}
                    onClick={() => setActiveTab('messages')}
                >
                    Messages
                    {unreadCount > 0 && (
                        <span className="summary-panel__tab-badge">{unreadCount}</span>
                    )}
                </button>
                <button
                    className={`summary-panel__tab ${activeTab === 'calendar' ? 'summary-panel__tab--active' : ''}`}
                    onClick={() => setActiveTab('calendar')}
                >
                    Calendar
                </button>
                <button
                    className={`summary-panel__tab ${activeTab === 'chat' ? 'summary-panel__tab--active' : ''}`}
                    onClick={() => setActiveTab('chat')}
                >
                    Chat
                </button>
            </div>

            {activeTab === 'messages' && (
                <>
                    <div className="summary-panel__actions">
                        <button
                            className="summary-panel__btn summary-panel__btn--secondary"
                            onClick={handleMarkAllRead}
                            disabled={unreadCount === 0}
                        >
                            Mark All Read
                        </button>
                        <button
                            className="summary-panel__btn summary-panel__btn--primary"
                            onClick={handleSummarizeAll}
                            disabled={summarizingAll || conversations.length === 0}
                        >
                            {summarizingAll ? 'Summarizing...' : 'Summarize All'}
                        </button>
                    </div>

                    <div className="summary-panel__list">
                        {loading && (
                            <div className="summary-panel__empty">
                                <div className="summary-panel__loader" />
                                <p>Loading conversations...</p>
                            </div>
                        )}

                        {!loading && conversations.length === 0 && (
                            <div className="summary-panel__empty">
                                <div className="summary-panel__empty-icon">💤</div>
                                <p>No conversations yet</p>
                                <span>When someone messages you, TamaBotchi will let you know!</span>
                            </div>
                        )}

                        {conversations.map((convo) => (
                            <ConversationCard
                                key={convo.conversation_id}
                                conversation={convo}
                                onRead={loadConversations}
                            />
                        ))}
                    </div>
                </>
            )}

            {activeTab === 'calendar' && (
                <div className="summary-panel__tab-content">
                    <CalendarView />
                </div>
            )}

            {activeTab === 'chat' && (
                <div className="summary-panel__tab-content summary-panel__tab-content--chat">
                    <ChatView />
                </div>
            )}

            <div className="summary-panel__footer">
                <span>TamaBotchi — Jesh's personal AI assistant</span>
            </div>
        </div>
    )
}

export default SummaryPanel
