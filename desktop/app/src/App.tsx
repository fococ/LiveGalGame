import { useEffect, useState } from 'react';

function App() {
  const [version, setVersion] = useState<string>('dev');

  useEffect(() => {
    async function fetchVersion() {
      try {
        const appVersion = await window.desktopAPI.getAppVersion();
        setVersion(appVersion);
      } catch (error) {
        console.error('Failed to retrieve app version', error);
      }
    }
    fetchVersion();
  }, []);

  return (
    <div className="app-root">
      <header className="app-header">
        <h1>LiveGalGame Desktop</h1>
        <p>Electron + Vite + React 模板</p>
      </header>
      <main className="app-main">
        <section className="card">
          <h2>开发状态</h2>
          <ul>
            <li>版本号：{version}</li>
            <li>后端服务：开发中</li>
            <li>语音识别：待接入</li>
          </ul>
        </section>
        <section className="card">
          <h2>下一步</h2>
          <ol>
            <li>完成 Python FastAPI 服务骨架</li>
            <li>定义前后端数据协议</li>
            <li>实现最小字幕闭环</li>
          </ol>
        </section>
      </main>
    </div>
  );
}

export default App;
