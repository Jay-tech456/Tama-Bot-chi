import { contextBridge, ipcRenderer } from 'electron'

contextBridge.exposeInMainWorld('electronAPI', {
    openSummary: () => ipcRenderer.send('open-summary'),
    closeSummary: () => ipcRenderer.send('close-summary'),
    toggleSummary: () => ipcRenderer.send('toggle-summary'),
})
