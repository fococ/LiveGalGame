import { contextBridge, ipcRenderer } from 'electron';

contextBridge.exposeInMainWorld('desktopAPI', {
  getAppVersion: async () => ipcRenderer.invoke('app:get-version')
});

declare global {
  interface Window {
    desktopAPI: {
      getAppVersion: () => Promise<string>;
    };
  }
}
