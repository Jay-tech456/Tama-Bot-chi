import { useState, useEffect, useCallback } from 'react'
import NotificationBadge from './NotificationBadge'
import { fetchUnreadCount } from '../middleware/api'
import '../styles/BunnyPet.css'

function BunnyPet() {
    const [unreadCount, setUnreadCount] = useState(0)
    const [mood, setMood] = useState<'idle' | 'excited' | 'sleeping'>('idle')
    const [blinking, setBlinking] = useState(false)
    const [bouncing, setBouncing] = useState(false)
    const [showIntro, setShowIntro] = useState(true)

    useEffect(() => {
        const timer = setTimeout(() => setShowIntro(false), 4500)
        return () => clearTimeout(timer)
    }, [])

    const pollUnread = useCallback(async () => {
        try {
            const count = await fetchUnreadCount()
            setUnreadCount(count)
            if (count > 0) {
                setMood('excited')
                setBouncing(true)
                setTimeout(() => setBouncing(false), 2000)
            } else {
                setMood('idle')
            }
        } catch {
            setMood('idle')
        }
    }, [])

    useEffect(() => {
        pollUnread()
        const interval = setInterval(pollUnread, 5000)
        return () => clearInterval(interval)
    }, [pollUnread])

    useEffect(() => {
        const blinkInterval = setInterval(() => {
            setBlinking(true)
            setTimeout(() => setBlinking(false), 200)
        }, 3000 + Math.random() * 2000)
        return () => clearInterval(blinkInterval)
    }, [])

    const handleClick = () => {
        if (window.electronAPI) {
            window.electronAPI.toggleSummary()
        }
        setBouncing(true)
        setTimeout(() => setBouncing(false), 600)
    }

    const speechText = showIntro
        ? "Hi! I'm TamaBotchi"
        : mood === 'excited'
        ? `${unreadCount} new!`
        : null

    return (
        <div className="bunny-container" onClick={handleClick}>
            <NotificationBadge count={unreadCount} />

            {speechText && (
                <div className={`bunny-speech-bubble ${showIntro ? 'bunny-speech-bubble--intro' : ''}`}>
                    <span>{speechText}</span>
                </div>
            )}

            <svg
                className={`bunny-svg ${bouncing ? 'bunny-svg--bounce' : ''} ${mood === 'excited' && !showIntro ? 'bunny-svg--excited' : ''}`}
                viewBox="0 0 120 140"
                width="120"
                height="140"
                xmlns="http://www.w3.org/2000/svg"
            >
                {/* Left Ear */}
                <ellipse cx="38" cy="28" rx="14" ry="32" fill="#f5f0eb" stroke="#e8ddd4" strokeWidth="1.5" />
                <ellipse cx="38" cy="28" rx="8" ry="24" fill="#ffc0cb" opacity="0.5" />

                {/* Right Ear */}
                <ellipse cx="82" cy="28" rx="14" ry="32" fill="#f5f0eb" stroke="#e8ddd4" strokeWidth="1.5" />
                <ellipse cx="82" cy="28" rx="8" ry="24" fill="#ffc0cb" opacity="0.5" />

                {/* Body */}
                <ellipse cx="60" cy="100" rx="36" ry="30" fill="#f5f0eb" stroke="#e8ddd4" strokeWidth="1.5" />

                {/* Head */}
                <circle cx="60" cy="68" r="30" fill="#f5f0eb" stroke="#e8ddd4" strokeWidth="1.5" />

                {/* Fluffy cheeks */}
                <circle cx="38" cy="74" r="10" fill="#fff5f5" opacity="0.7" />
                <circle cx="82" cy="74" r="10" fill="#fff5f5" opacity="0.7" />

                {/* Eyes */}
                {blinking ? (
                    <>
                        <line x1="48" y1="64" x2="56" y2="64" stroke="#4a4a4a" strokeWidth="2" strokeLinecap="round" />
                        <line x1="64" y1="64" x2="72" y2="64" stroke="#4a4a4a" strokeWidth="2" strokeLinecap="round" />
                    </>
                ) : (
                    <>
                        <ellipse cx="50" cy="63" rx="5" ry="6" fill="#4a4a4a" />
                        <ellipse cx="70" cy="63" rx="5" ry="6" fill="#4a4a4a" />
                        <circle cx="48" cy="61" r="2" fill="#ffffff" />
                        <circle cx="68" cy="61" r="2" fill="#ffffff" />
                    </>
                )}

                {/* Nose */}
                <ellipse cx="60" cy="72" rx="3" ry="2.5" fill="#ffb6c1" />

                {/* Mouth */}
                <path d="M 56 75 Q 60 79 64 75" fill="none" stroke="#d4a0a0" strokeWidth="1.2" strokeLinecap="round" />

                {/* Blush */}
                <circle cx="42" cy="72" r="5" fill="#ffb6c1" opacity="0.3" />
                <circle cx="78" cy="72" r="5" fill="#ffb6c1" opacity="0.3" />

                {/* Left Paw */}
                <ellipse cx="36" cy="118" rx="10" ry="6" fill="#f5f0eb" stroke="#e8ddd4" strokeWidth="1" />

                {/* Right Paw */}
                <ellipse cx="84" cy="118" rx="10" ry="6" fill="#f5f0eb" stroke="#e8ddd4" strokeWidth="1" />

                {/* Tail (fluffy circle behind) */}
                <circle cx="60" cy="128" r="8" fill="#f5f0eb" stroke="#e8ddd4" strokeWidth="1" />

                {/* Fluffy tummy detail */}
                <ellipse cx="60" cy="98" rx="18" ry="14" fill="#fffaf5" opacity="0.6" />
            </svg>

            <div className="bunny-shadow" />
        </div>
    )
}

export default BunnyPet
