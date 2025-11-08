const { contextBridge, ipcRenderer } = require('electron');
const os = require('os');
const path = require('path');

console.log('Preload script is running');

// Expose protected methods that allow the renderer process to use
// the ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('api', {
    getVideoInfo: (url) => ipcRenderer.invoke('get-video-info', url),
    downloadVideo: (options) => ipcRenderer.invoke('download-video', options),
    selectDirectory: () => ipcRenderer.invoke('select-directory'),
    onDownloadProgress: (callback) => {
        ipcRenderer.on('download-progress', (event, data) => callback(data));
    },
    // System utilities
    getHomeDir: () => os.homedir(),
    getDownloadsDir: () => path.join(os.homedir(), 'Downloads')
});

console.log('window.api exposed successfully');
