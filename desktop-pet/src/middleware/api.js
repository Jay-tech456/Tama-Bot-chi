import axios from 'axios'

const AGENT_API_URL = 'http://127.0.0.1:5000'

const api = axios.create({
    baseURL: AGENT_API_URL,
    timeout: 30000,
    headers: {
        'Content-Type': 'application/json',
    },
})

export async function fetchAllConversations() {
    const response = await api.get('/pet/conversations')
    return response.data
}

export async function fetchUnreadConversations() {
    const response = await api.get('/pet/conversations/unread')
    return response.data
}

export async function fetchUnreadCount() {
    const response = await api.get('/pet/conversations/unread/count')
    return response.data.unread_count
}

export async function markConversationRead(conversationId) {
    const response = await api.post(`/pet/conversations/${conversationId}/read`)
    return response.data
}

export async function markAllRead() {
    const response = await api.post('/pet/conversations/read-all')
    return response.data
}

export async function summarizeConversation(conversationId) {
    const response = await api.post(`/pet/conversations/${conversationId}/summarize`)
    return response.data.summary
}

export async function summarizeAll() {
    const response = await api.post('/pet/summarize-all')
    return response.data
}

export async function checkHealth() {
    try {
        const response = await api.get('/health')
        return response.data.status === 'healthy'
    } catch {
        return false
    }
}

export async function fetchCalendarEvents(days = 14) {
    const response = await api.get('/pet/calendar/events', { params: { days } })
    return response.data
}

export async function fetchReminders() {
    const response = await api.get('/pet/calendar/reminders')
    return response.data
}

export async function scheduleEvent(data) {
    const response = await api.post('/pet/calendar/schedule', data)
    return response.data
}

export async function chatWithTamaBotchi(message, history = []) {
    const response = await api.post('/pet/chat', { message, history })
    return response.data
}

export default api
