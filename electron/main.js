const { app, BrowserWindow, ipcMain } = require('electron');
const path = require('path');
const { PythonShell } = require('python-shell');

let mainWindow;
let pythonProcess = null;

function createWindow() {
    mainWindow = new BrowserWindow({
        width: 1200,
        height: 800,
        minWidth: 900,
        minHeight: 600,
        webPreferences: {
            nodeIntegration: false,
            contextIsolation: true,
            sandbox: false,  // Disable sandbox to allow preload script to use Node.js modules
            preload: path.join(__dirname, 'preload.js')
        },
        backgroundColor: '#1a1a2e',
        icon: path.join(__dirname, '../assets/icon.png')
    });

    mainWindow.loadFile(path.join(__dirname, '../web/index.html'));

    // Open DevTools in development mode
    if (process.argv.includes('--dev')) {
        mainWindow.webContents.openDevTools();
    }

    mainWindow.on('closed', () => {
        mainWindow = null;
        if (pythonProcess) {
            pythonProcess.kill();
        }
    });
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});

app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
        createWindow();
    }
});

// IPC Handlers for Python backend communication

// Get video info
ipcMain.handle('get-video-info', async (event, url) => {
    console.log('get-video-info called with URL:', url);
    
    return new Promise((resolve, reject) => {
        const options = {
            mode: 'text',  // Changed from 'json' to 'text' to see raw output
            pythonPath: path.join(__dirname, '../.venv/bin/python3'),
            scriptPath: path.join(__dirname, '../tools/youtube_downloader'),
            args: ['--get-info', url]
        };

        console.log('Python options:', options);

        let output = '';
        const pyshell = new PythonShell('api.py', options);

        pyshell.on('message', (message) => {
            console.log('Python message:', message);
            output += message;
        });

        pyshell.on('stderr', (stderr) => {
            console.error('Python stderr:', stderr);
        });

        pyshell.end((err, code, signal) => {
            console.log('Python script ended. Code:', code, 'Signal:', signal);
            
            if (err) {
                console.error('Python error:', err);
                reject(err);
            } else {
                try {
                    console.log('Raw output:', output);
                    const result = JSON.parse(output);
                    console.log('Parsed result:', result);
                    resolve(result);
                } catch (parseError) {
                    console.error('JSON parse error:', parseError);
                    reject(new Error('Failed to parse Python output: ' + output));
                }
            }
        });
    });
});

// Download video
ipcMain.handle('download-video', async (event, options) => {
    console.log('download-video called with options:', options);
    
    return new Promise((resolve, reject) => {
        const pythonOptions = {
            mode: 'text',
            pythonPath: path.join(__dirname, '../.venv/bin/python3'),
            scriptPath: path.join(__dirname, '../tools/youtube_downloader'),
            args: [
                '--download',
                '--url', options.url,
                '--quality', options.quality,
                '--format', options.format,
                '--output', options.outputPath
            ]
        };

        console.log('Python download options:', pythonOptions);

        const pyshell = new PythonShell('api.py', pythonOptions);

        pyshell.on('message', (message) => {
            console.log('Download progress message:', message);
            // Try to parse as JSON for progress updates
            try {
                const progressData = JSON.parse(message);
                if (mainWindow) {
                    mainWindow.webContents.send('download-progress', progressData);
                }
            } catch (e) {
                // Not JSON, just log it
                console.log('Non-JSON message:', message);
            }
        });

        pyshell.on('stderr', (stderr) => {
            console.error('Download stderr:', stderr);
        });

        pyshell.end((err, code, signal) => {
            console.log('Download script ended. Code:', code, 'Signal:', signal);
            
            if (err) {
                console.error('Download error:', err);
                reject(err);
            } else {
                resolve({ success: true, code });
            }
        });
    });
});

// Select directory
ipcMain.handle('select-directory', async () => {
    const { dialog } = require('electron');
    const result = await dialog.showOpenDialog(mainWindow, {
        properties: ['openDirectory']
    });
    
    if (!result.canceled && result.filePaths.length > 0) {
        return result.filePaths[0];
    }
    return null;
});
