// API Check - Ensures window.api is available before app initializes
(function() {
    console.log('API Check running...');
    console.log('window.api available:', !!window.api);
    
    if (!window.api) {
        console.error('CRITICAL: window.api is not available!');
        console.error('This means the preload script did not execute properly.');
        console.error('Electron webPreferences should have:');
        console.error('  - nodeIntegration: false');
        console.error('  - contextIsolation: true');
        console.error('  - preload: path to preload.js');
        
        // Show error to user
        document.addEventListener('DOMContentLoaded', () => {
            document.body.innerHTML = `
                <div style="padding: 40px; font-family: Arial, sans-serif; text-align: center;">
                    <h1 style="color: #e74c3c;">⚠️ Application Error</h1>
                    <p style="font-size: 18px; color: #333;">
                        The application failed to initialize properly.
                    </p>
                    <p style="color: #666;">
                        The Electron preload script did not execute. Please check the console for details.
                    </p>
                    <button onclick="location.reload()" style="
                        margin-top: 20px;
                        padding: 10px 20px;
                        font-size: 16px;
                        background: #3498db;
                        color: white;
                        border: none;
                        border-radius: 5px;
                        cursor: pointer;
                    ">Reload</button>
                </div>
            `;
        });
    } else {
        console.log('✓ window.api is available');
        console.log('Available API methods:', Object.keys(window.api));
    }
})();
