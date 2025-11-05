import { app, BrowserWindow, ipcMain } from 'electron';
import { join } from 'node:path';
import { format } from 'node:url';

const isDebug = !app.isPackaged;

async function createWindow() {
  const mainWindow = new BrowserWindow({
    width: 1280,
    height: 720,
    minWidth: 1024,
    minHeight: 600,
    webPreferences: {
      preload: join(__dirname, 'preload.js'),
      contextIsolation: true,
      nodeIntegration: false
    },
    show: false
  });

  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    if (isDebug) {
      mainWindow.webContents.openDevTools({ mode: 'detach' });
    }
  });

  if (isDebug) {
    await mainWindow.loadURL('http://localhost:5173');
  } else {
    await mainWindow.loadURL(
      format({
        pathname: join(__dirname, '../dist-renderer/index.html'),
        protocol: 'file',
        slashes: true
      })
    );
  }
}

app.whenReady().then(createWindow);

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('activate', async () => {
  if (BrowserWindow.getAllWindows().length === 0) {
    await createWindow();
  }
});

ipcMain.handle('app:get-version', () => app.getVersion());
