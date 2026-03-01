"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const electron_1 = require("electron");
electron_1.contextBridge.exposeInMainWorld('electronAPI', {
    openSummary: () => electron_1.ipcRenderer.send('open-summary'),
    closeSummary: () => electron_1.ipcRenderer.send('close-summary'),
    toggleSummary: () => electron_1.ipcRenderer.send('toggle-summary'),
});
