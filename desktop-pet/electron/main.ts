import { app, BrowserWindow, screen, ipcMain, Tray, Menu } from 'electron'
import * as path from 'path'

let petWindow: BrowserWindow | null = null
let summaryWindow: BrowserWindow | null = null
let tray: Tray | null = null

const PET_WIDTH = 220
const PET_HEIGHT = 380
const SUMMARY_WIDTH = 420
const SUMMARY_HEIGHT = 620

function createPetWindow() {
    const display = screen.getPrimaryDisplay()
    const { width: screenW, height: screenH } = display.workAreaSize

    petWindow = new BrowserWindow({
        width: PET_WIDTH,
        height: PET_HEIGHT,
        x: screenW - PET_WIDTH - 40,
        y: screenH - PET_HEIGHT - 40,
        frame: false,
        transparent: true,
        alwaysOnTop: true,
        resizable: false,
        skipTaskbar: true,
        hasShadow: false,
        focusable: true,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
    })

    petWindow.setVisibleOnAllWorkspaces(true, { visibleOnFullScreen: true })
    petWindow.setIgnoreMouseEvents(false)

    const isDev = !app.isPackaged
    if (isDev) {
        petWindow.loadURL('http://localhost:5173/#pet')
    } else {
        petWindow.loadFile(path.join(__dirname, '../dist/index.html'), { hash: 'pet' })
    }

    petWindow.on('closed', () => {
        petWindow = null
    })
}

function createSummaryWindow() {
    if (summaryWindow) {
        summaryWindow.show()
        summaryWindow.focus()
        return
    }

    const display = screen.getPrimaryDisplay()
    const { width: screenW, height: screenH } = display.workAreaSize

    summaryWindow = new BrowserWindow({
        width: SUMMARY_WIDTH,
        height: SUMMARY_HEIGHT,
        x: screenW - SUMMARY_WIDTH - PET_WIDTH - 60,
        y: screenH - SUMMARY_HEIGHT - 40,
        frame: false,
        transparent: true,
        alwaysOnTop: true,
        resizable: false,
        skipTaskbar: true,
        hasShadow: true,
        focusable: true,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js'),
            contextIsolation: true,
            nodeIntegration: false,
        },
    })

    summaryWindow.setVisibleOnAllWorkspaces(true)

    const isDev = !app.isPackaged
    if (isDev) {
        summaryWindow.loadURL('http://localhost:5173/#summary')
    } else {
        summaryWindow.loadFile(path.join(__dirname, '../dist/index.html'), { hash: 'summary' })
    }

    summaryWindow.on('closed', () => {
        summaryWindow = null
    })
}

function closeSummaryWindow() {
    if (summaryWindow) {
        summaryWindow.close()
        summaryWindow = null
    }
}

app.whenReady().then(() => {
    createPetWindow()

    ipcMain.on('open-summary', () => {
        createSummaryWindow()
    })

    ipcMain.on('close-summary', () => {
        closeSummaryWindow()
    })

    ipcMain.on('toggle-summary', () => {
        if (summaryWindow) {
            closeSummaryWindow()
        } else {
            createSummaryWindow()
        }
    })
})

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit()
    }
})

app.on('activate', () => {
    if (!petWindow) {
        createPetWindow()
    }
})
