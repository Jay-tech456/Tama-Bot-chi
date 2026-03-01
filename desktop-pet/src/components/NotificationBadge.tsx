import '../styles/NotificationBadge.css'

interface NotificationBadgeProps {
    count: number
}

function NotificationBadge({ count }: NotificationBadgeProps) {
    if (count <= 0) return null

    return (
        <div className="notification-badge">
            <span className="notification-badge__count">
                {count > 99 ? '99+' : count}
            </span>
        </div>
    )
}

export default NotificationBadge
