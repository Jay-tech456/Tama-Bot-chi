/// <reference types="vite/client" />

interface ElectronAPI {
    openSummary: () => void
    closeSummary: () => void
    toggleSummary: () => void
}

interface Window {
    electronAPI?: ElectronAPI
}
