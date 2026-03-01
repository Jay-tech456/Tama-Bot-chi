import { useState, useEffect } from 'react'
import { fetchCalendarEvents, fetchReminders, scheduleEvent } from '../middleware/api'

interface CalendarEvent {
    title: string
    start: string
    end: string
    calendar: string
    notes: string
}

interface Reminder {
    name: string
    due: string | null
    list: string
    body: string
}

interface ScheduleForm {
    title: string
    date: string
    startTime: string
    endTime: string
    notes: string
    calendarName: string
}

const EMPTY_FORM: ScheduleForm = {
    title: '',
    date: '',
    startTime: '',
    endTime: '',
    notes: '',
    calendarName: 'Calendar',
}

function CalendarView() {
    const [events, setEvents] = useState<CalendarEvent[]>([])
    const [reminders, setReminders] = useState<Reminder[]>([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState<string | null>(null)
    const [showForm, setShowForm] = useState(false)
    const [scheduling, setScheduling] = useState(false)
    const [successMsg, setSuccessMsg] = useState<string | null>(null)
    const [form, setForm] = useState<ScheduleForm>(EMPTY_FORM)

    useEffect(() => {
        loadData()
    }, [])

    const loadData = async () => {
        setLoading(true)
        setError(null)
        try {
            const [eventsData, remindersData] = await Promise.all([
                fetchCalendarEvents(14),
                fetchReminders(),
            ])
            // Backend returns permission_error instead of throwing 500
            const permErr = eventsData.permission_error || remindersData.permission_error
            if (permErr) {
                setError(permErr)
            }
            setEvents(eventsData.events || [])
            setReminders(remindersData.reminders || [])
        } catch {
            setError(
                'Could not reach the TamaBotchi agent. Make sure it is running on port 5000.'
            )
        }
        setLoading(false)
    }

    const handleFormChange = (field: keyof ScheduleForm, value: string) => {
        setForm((prev) => ({ ...prev, [field]: value }))
    }

    const handleSchedule = async (e: React.FormEvent) => {
        e.preventDefault()
        if (!form.title.trim() || !form.date || !form.startTime || !form.endTime) return
        setScheduling(true)
        try {
            await scheduleEvent({
                title: form.title.trim(),
                start_iso: `${form.date}T${form.startTime}:00`,
                end_iso: `${form.date}T${form.endTime}:00`,
                notes: form.notes.trim(),
                calendar_name: form.calendarName || 'Calendar',
            })
            setForm(EMPTY_FORM)
            setShowForm(false)
            setSuccessMsg('Event added to Calendar!')
            setTimeout(() => setSuccessMsg(null), 3000)
            loadData()
        } catch {
            setSuccessMsg('Failed to create event. Check Calendar permissions.')
            setTimeout(() => setSuccessMsg(null), 4000)
        }
        setScheduling(false)
    }

    const formatDate = (iso: string) =>
        new Date(iso).toLocaleDateString('en-US', {
            weekday: 'short',
            month: 'short',
            day: 'numeric',
        })

    const formatTime = (iso: string) =>
        new Date(iso).toLocaleTimeString('en-US', { hour: 'numeric', minute: '2-digit' })

    const formatDue = (due: string | null): string => {
        if (!due) return 'No due date'
        const d = new Date(due)
        const now = new Date()
        const diff = d.getTime() - now.getTime()
        if (diff < 0) return 'Overdue'
        if (diff < 86400000) return 'Today'
        if (diff < 172800000) return 'Tomorrow'
        return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })
    }

    const groupByDate = (evts: CalendarEvent[]): Record<string, CalendarEvent[]> => {
        const groups: Record<string, CalendarEvent[]> = {}
        evts.forEach((evt) => {
            const key = formatDate(evt.start)
            if (!groups[key]) groups[key] = []
            groups[key].push(evt)
        })
        return groups
    }

    if (loading) {
        return (
            <div className="calendar-view calendar-view--loading">
                <div className="calendar-view__spinner" />
                <p>Loading Calendar...</p>
            </div>
        )
    }

    if (error && events.length === 0 && reminders.length === 0) {
        return (
            <div className="calendar-view calendar-view--error">
                <div className="calendar-view__error-icon">🔒</div>
                <p className="calendar-view__error-title">Permission Required</p>
                <p className="calendar-view__error-msg">
                    Go to <strong>System Settings &gt; Privacy &amp; Security &gt; Calendar</strong> (and Reminders) and grant access to <strong>Terminal</strong>.
                </p>
                <button className="calendar-view__retry-btn" onClick={loadData}>
                    Retry
                </button>
            </div>
        )
    }

    const grouped = groupByDate(events)

    return (
        <div className="calendar-view">
            {successMsg && <div className="calendar-view__toast">{successMsg}</div>}

            <div className="calendar-view__section-header">
                <span className="calendar-view__section-title">Upcoming — 14 days</span>
                <button
                    className="calendar-view__add-btn"
                    onClick={() => setShowForm((v) => !v)}
                >
                    {showForm ? 'Cancel' : '+ Schedule'}
                </button>
            </div>

            {showForm && (
                <form className="calendar-view__form" onSubmit={handleSchedule}>
                    <input
                        className="calendar-view__input"
                        type="text"
                        placeholder="Event title"
                        value={form.title}
                        onChange={(e) => handleFormChange('title', e.target.value)}
                        required
                    />
                    <input
                        className="calendar-view__input"
                        type="date"
                        value={form.date}
                        onChange={(e) => handleFormChange('date', e.target.value)}
                        required
                    />
                    <div className="calendar-view__time-row">
                        <input
                            className="calendar-view__input calendar-view__input--half"
                            type="time"
                            value={form.startTime}
                            onChange={(e) => handleFormChange('startTime', e.target.value)}
                            required
                        />
                        <span className="calendar-view__time-sep">to</span>
                        <input
                            className="calendar-view__input calendar-view__input--half"
                            type="time"
                            value={form.endTime}
                            onChange={(e) => handleFormChange('endTime', e.target.value)}
                            required
                        />
                    </div>
                    <input
                        className="calendar-view__input"
                        type="text"
                        placeholder="Calendar name (default: Calendar)"
                        value={form.calendarName}
                        onChange={(e) => handleFormChange('calendarName', e.target.value)}
                    />
                    <textarea
                        className="calendar-view__input calendar-view__textarea"
                        placeholder="Notes (optional)"
                        value={form.notes}
                        onChange={(e) => handleFormChange('notes', e.target.value)}
                        rows={2}
                    />
                    <button
                        className="calendar-view__submit-btn"
                        type="submit"
                        disabled={scheduling}
                    >
                        {scheduling ? 'Scheduling...' : 'Add to Calendar'}
                    </button>
                </form>
            )}

            {events.length === 0 && (
                <div className="calendar-view__empty">
                    <p>No upcoming events in the next 14 days</p>
                </div>
            )}

            {Object.entries(grouped).map(([dateLabel, dayEvents]) => (
                <div key={dateLabel} className="calendar-view__day-group">
                    <div className="calendar-view__day-label">{dateLabel}</div>
                    {dayEvents.map((evt, i) => (
                        <div key={i} className="calendar-view__event-card">
                            <div className="calendar-view__event-dot" />
                            <div className="calendar-view__event-info">
                                <div className="calendar-view__event-title">{evt.title}</div>
                                <div className="calendar-view__event-time">
                                    {formatTime(evt.start)} – {formatTime(evt.end)}
                                    <span className="calendar-view__event-cal"> · {evt.calendar}</span>
                                </div>
                                {evt.notes && (
                                    <div className="calendar-view__event-notes">{evt.notes}</div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            ))}

            {reminders.length > 0 && (
                <>
                    <div className="calendar-view__section-header calendar-view__section-header--reminders">
                        <span className="calendar-view__section-title">Reminders</span>
                        <span className="calendar-view__reminder-count">{reminders.length}</span>
                    </div>
                    {reminders.map((r, i) => (
                        <div key={i} className="calendar-view__reminder-card">
                            <div
                                className={`calendar-view__reminder-due ${
                                    r.due && new Date(r.due) < new Date()
                                        ? 'calendar-view__reminder-due--overdue'
                                        : ''
                                }`}
                            >
                                {formatDue(r.due)}
                            </div>
                            <div className="calendar-view__reminder-name">{r.name}</div>
                            <div className="calendar-view__reminder-list">{r.list}</div>
                        </div>
                    ))}
                </>
            )}
        </div>
    )
}

export default CalendarView
