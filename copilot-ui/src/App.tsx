import { useState, CSSProperties } from 'react'

const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 18) return 'Good afternoon'
  return 'Good evening'
}

const quickActions = ['Write a first draft', 'Get advice', 'Learn something new', 'Create an image', 'Make a plan']

const recentFiles = [
  { name: 'Screenshot 2025-12-19 0644...', time: '52m ago', type: 'image' },
  { name: 'Screenshot 2025-12-19 0653...', time: '53m ago', type: 'image' },
  { name: 'NAD_Immunodynamics_Crux...', time: '3h ago', type: 'doc' }
]

const apps = [
  { name: 'Canva', color: '#00C4CC', icon: '🎨' },
  { name: 'PowerPoint', color: '#D24726', icon: '📊' },
  { name: 'Spotify', color: '#1DB954', icon: '🎵' },
  { name: 'Settings', color: '#6B7280', icon: '⚙️' },
  { name: 'Files', color: '#F59E0B', icon: '📁' },
  { name: 'Office', color: '#D83B01', icon: '📝' }
]

// Styles
const styles: Record<string, CSSProperties> = {
  app: {
    background: 'linear-gradient(180deg, #0a1628 0%, #1a2744 30%, #1e3a5f 60%, #2d4a6f 80%, #3d5a7f 100%)',
    minHeight: '100vh',
    fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif",
    color: 'white',
    position: 'relative',
    overflow: 'hidden',
  },
  windowControls: {
    position: 'fixed',
    top: 16,
    right: 16,
    display: 'flex',
    gap: 8,
    zIndex: 100,
  },
  windowBtn: {
    background: 'transparent',
    border: 'none',
    color: 'rgba(255,255,255,0.5)',
    fontSize: 18,
    cursor: 'pointer',
    padding: '4px 8px',
    borderRadius: 4,
  },
  main: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    padding: '60px 20px 40px',
    minHeight: '100vh',
    position: 'relative',
    zIndex: 10,
  },
  greeting: {
    fontSize: 48,
    fontWeight: 300,
    color: '#67e8f9',
    margin: '0 0 8px 0',
  },
  subtitle: {
    fontSize: 28,
    fontWeight: 300,
    margin: '0 0 40px 0',
  },
  inputContainer: {
    background: 'rgba(30, 41, 59, 0.9)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255,255,255,0.15)',
    borderRadius: 28,
    padding: '16px 20px',
    width: '100%',
    maxWidth: 640,
    marginBottom: 24,
  },
  input: {
    width: '100%',
    background: 'transparent',
    border: 'none',
    outline: 'none',
    color: 'white',
    fontSize: 18,
    marginBottom: 12,
  },
  inputFooter: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  inputLeft: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
  },
  inputRight: {
    display: 'flex',
    gap: 8,
  },
  copilotIcon: {
    width: 32,
    height: 32,
    background: 'linear-gradient(135deg, #3b82f6, #8b5cf6)',
    borderRadius: 8,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 14,
  },
  modelBtn: {
    background: 'rgba(59, 130, 246, 0.3)',
    border: 'none',
    borderRadius: 8,
    padding: '6px 12px',
    color: 'white',
    fontSize: 14,
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    gap: 6,
  },
  iconBtn: {
    background: 'transparent',
    border: 'none',
    color: 'rgba(255,255,255,0.6)',
    cursor: 'pointer',
    padding: 8,
    borderRadius: 8,
    fontSize: 18,
  },
  chips: {
    display: 'flex',
    flexWrap: 'wrap',
    justifyContent: 'center',
    gap: 12,
    marginBottom: 60,
    maxWidth: 640,
  },
  chip: {
    background: 'rgba(255,255,255,0.1)',
    border: '1px solid rgba(255,255,255,0.2)',
    borderRadius: 20,
    padding: '10px 18px',
    color: 'white',
    fontSize: 14,
    cursor: 'pointer',
  },
  panels: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: 16,
    width: '100%',
    maxWidth: 1000,
    marginTop: 'auto',
  },
  panel: {
    background: 'rgba(30, 41, 59, 0.6)',
    backdropFilter: 'blur(10px)',
    border: '1px solid rgba(255,255,255,0.08)',
    borderRadius: 16,
    padding: 16,
  },
  panelHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
    color: 'rgba(255,255,255,0.6)',
    fontSize: 13,
  },
  fileItem: {
    display: 'flex',
    alignItems: 'center',
    gap: 12,
    padding: 8,
    borderRadius: 8,
    cursor: 'pointer',
    marginBottom: 4,
  },
  fileIconImage: {
    width: 40,
    height: 40,
    borderRadius: 10,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 18,
    background: 'linear-gradient(135deg, #a855f7, #ec4899)',
  },
  fileIconDoc: {
    width: 40,
    height: 40,
    borderRadius: 10,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 18,
    background: '#2563eb',
  },
  fileInfo: {
    flex: 1,
    minWidth: 0,
  },
  fileName: {
    fontSize: 14,
    whiteSpace: 'nowrap',
    overflow: 'hidden',
    textOverflow: 'ellipsis',
  },
  fileTime: {
    fontSize: 12,
    color: 'rgba(255,255,255,0.4)',
  },
  appsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: 12,
  },
  appIcon: {
    width: 48,
    height: 48,
    borderRadius: 12,
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontSize: 24,
    cursor: 'pointer',
  },
  convIcon: {
    width: 40,
    height: 40,
    borderRadius: '50%',
    background: 'rgba(255,255,255,0.1)',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  footer: {
    color: 'rgba(255,255,255,0.3)',
    fontSize: 12,
    marginTop: 32,
  },
}

function App() {
  const [query, setQuery] = useState('')
  const [selectedModel, setSelectedModel] = useState('Smart (GPT-5)')
  const models = ['Smart (GPT-5)', 'Creative (GPT-5)', 'Precise (GPT-4)']

  const cycleModel = () => {
    const idx = models.indexOf(selectedModel)
    setSelectedModel(models[(idx + 1) % models.length])
  }

  return (
    <div style={styles.app}>
      {/* Window controls */}
      <div style={styles.windowControls}>
        <button style={styles.windowBtn}>↗</button>
        <button style={styles.windowBtn}>−</button>
        <button style={styles.windowBtn}>□</button>
        <button style={styles.windowBtn}>×</button>
      </div>

      <main style={styles.main}>
        <h1 style={styles.greeting}>{getGreeting()}</h1>
        <h2 style={styles.subtitle}>What can I help you with today?</h2>

        {/* Input */}
        <div style={styles.inputContainer}>
          <input
            style={styles.input}
            type="text"
            placeholder="Ask anything"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <div style={styles.inputFooter}>
            <div style={styles.inputLeft}>
              <div style={styles.copilotIcon}>✦</div>
              <button style={styles.modelBtn} onClick={cycleModel}>
                {selectedModel} <span>▼</span>
              </button>
            </div>
            <div style={styles.inputRight}>
              <button style={styles.iconBtn}>+</button>
              <button style={styles.iconBtn}>🔗</button>
              <button style={styles.iconBtn}>🎤</button>
            </div>
          </div>
        </div>

        {/* Chips */}
        <div style={styles.chips}>
          {quickActions.map((action) => (
            <button key={action} style={styles.chip} onClick={() => setQuery(action)}>
              {action}
            </button>
          ))}
        </div>

        {/* Panels */}
        <div style={styles.panels}>
          {/* Files */}
          <div style={styles.panel}>
            <div style={styles.panelHeader}>
              <span>📎 Jump back in to your files</span>
              <button style={styles.iconBtn}>ⓘ</button>
            </div>
            {recentFiles.map((file, i) => (
              <div key={i} style={styles.fileItem}>
                <div style={file.type === 'image' ? styles.fileIconImage : styles.fileIconDoc}>
                  {file.type === 'image' ? '🖼' : '📄'}
                </div>
                <div style={styles.fileInfo}>
                  <div style={styles.fileName}>{file.name}</div>
                  <div style={styles.fileTime}>{file.time}</div>
                </div>
                <button style={styles.iconBtn}>⋯</button>
              </div>
            ))}
          </div>

          {/* Apps */}
          <div style={styles.panel}>
            <div style={styles.panelHeader}>
              <span>🔗 Get guided help with your apps</span>
              <button style={styles.iconBtn}>ⓘ</button>
            </div>
            <div style={styles.appsGrid}>
              {apps.map((app) => (
                <div key={app.name} style={{ ...styles.appIcon, backgroundColor: app.color }} title={app.name}>
                  {app.icon}
                </div>
              ))}
            </div>
          </div>

          {/* Conversations */}
          <div style={styles.panel}>
            <div style={styles.panelHeader}>
              <span>💬 Recent conversations</span>
            </div>
            <div style={styles.fileItem}>
              <div style={styles.convIcon}>💬</div>
              <div style={styles.fileInfo}>
                <div style={styles.fileName}>Getting started</div>
                <div style={styles.fileTime}>Just now</div>
              </div>
            </div>
          </div>
        </div>

        <p style={styles.footer}>AI responses may vary.</p>
      </main>
    </div>
  )
}

export default App
