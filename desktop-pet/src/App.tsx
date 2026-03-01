import { useState, useEffect } from 'react'
import BunnyPet from './components/BunnyPet'
import SummaryPanel from './components/SummaryPanel'
import './styles/App.css'

function App() {
    const [view, setView] = useState<'pet' | 'summary'>('pet')

    useEffect(() => {
        const hash = window.location.hash.replace('#', '')
        if (hash === 'summary') {
            setView('summary')
        } else {
            setView('pet')
        }
    }, [])

    if (view === 'summary') {
        return <SummaryPanel />
    }

    return <BunnyPet />
}

export default App
