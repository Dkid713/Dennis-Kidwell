import { useState } from 'react'
import './index.css'
import {
  Plus,
  Link,
  Mic,
  ChevronDown,
  Paperclip,
  Info,
  MoreHorizontal,
  Image,
  FileText,
  MessageSquare
} from 'lucide-react'

// Get time-based greeting
const getGreeting = () => {
  const hour = new Date().getHours()
  if (hour < 12) return 'Good morning'
  if (hour < 18) return 'Good afternoon'
  return 'Good evening'
}

// Quick action chips
const quickActions = [
  'Write a first draft',
  'Get advice',
  'Learn something new',
  'Create an image',
  'Make a plan'
]

// Mock recent files
const recentFiles = [
  { name: 'Screenshot 2025-12-19 0644...', time: '52m ago', type: 'image' },
  { name: 'Screenshot 2025-12-19 0653...', time: '53m ago', type: 'image' },
  { name: 'NAD_Immunodynamics_Crux...', time: '3h ago', type: 'doc' }
]

// Mock apps
const apps = [
  { name: 'Canva', color: '#00C4CC', icon: '🎨' },
  { name: 'PowerPoint', color: '#D24726', icon: '📊' },
  { name: 'Spotify', color: '#1DB954', icon: '🎵' },
  { name: 'Settings', color: '#6B7280', icon: '⚙️' },
  { name: 'Files', color: '#F59E0B', icon: '📁' },
  { name: 'Office', color: '#D83B01', icon: '📝' }
]

// Mock conversations
const conversations = [
  { title: 'How can Copilot help me?', time: 'Just now' }
]

function App() {
  const [query, setQuery] = useState('')
  const [selectedModel, setSelectedModel] = useState('Smart (GPT-5)')

  return (
    <div className="gradient-bg">
      {/* Floral decoration at bottom */}
      <div className="floral-overlay" />

      {/* Window controls */}
      <div className="absolute top-4 right-4 flex gap-2">
        {['edit', 'minimize', 'maximize', 'close'].map((action, i) => (
          <button
            key={action}
            className="icon-btn text-white/60 hover:text-white"
          >
            {i === 3 ? '×' : i === 2 ? '□' : i === 1 ? '−' : '↗'}
          </button>
        ))}
      </div>

      {/* Main content */}
      <div className="flex flex-col items-center px-4 pt-16 pb-8 relative z-10">
        {/* Greeting */}
        <h1 className="text-4xl md:text-5xl font-light text-cyan-300 mb-2">
          {getGreeting()}
        </h1>
        <h2 className="text-2xl md:text-3xl font-light text-white mb-10">
          What can I help you with today?
        </h2>

        {/* Chat input */}
        <div className="input-glass w-full max-w-2xl p-4 mb-6">
          <input
            type="text"
            placeholder="Ask anything"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full bg-transparent text-white placeholder-white/40 text-lg outline-none mb-3"
          />

          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              {/* Copilot icon */}
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center">
                <span className="text-white text-sm">✦</span>
              </div>

              {/* Model selector */}
              <button className="model-selector text-white text-sm">
                {selectedModel}
                <ChevronDown size={14} />
              </button>
            </div>

            <div className="flex items-center gap-2">
              <button className="icon-btn">
                <Plus size={20} />
              </button>
              <button className="icon-btn">
                <Link size={20} />
              </button>
              <button className="icon-btn">
                <Mic size={20} />
              </button>
            </div>
          </div>
        </div>

        {/* Quick action chips */}
        <div className="flex flex-wrap justify-center gap-3 mb-16 max-w-2xl">
          {quickActions.map((action) => (
            <button key={action} className="chip">
              {action}
            </button>
          ))}
        </div>

        {/* Bottom panels */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 w-full max-w-5xl mt-auto">
          {/* Recent files panel */}
          <div className="panel-card">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2 text-white/60 text-sm">
                <Paperclip size={16} />
                Jump back in to your files
              </div>
              <button className="icon-btn p-1">
                <Info size={16} />
              </button>
            </div>

            <div className="space-y-1">
              {recentFiles.map((file, i) => (
                <div key={i} className="file-item">
                  <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                    file.type === 'image'
                      ? 'bg-gradient-to-br from-purple-500 to-pink-500'
                      : 'bg-blue-600'
                  }`}>
                    {file.type === 'image' ? <Image size={18} className="text-white" /> : <FileText size={18} className="text-white" />}
                  </div>
                  <div className="flex-1 min-w-0">
                    <p className="text-white text-sm truncate">{file.name}</p>
                    <p className="text-white/40 text-xs">{file.time}</p>
                  </div>
                  <button className="icon-btn p-1">
                    <MoreHorizontal size={16} />
                  </button>
                </div>
              ))}
            </div>
          </div>

          {/* Apps panel */}
          <div className="panel-card">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2 text-white/60 text-sm">
                <Link size={16} />
                Get guided help with your apps
              </div>
              <button className="icon-btn p-1">
                <Info size={16} />
              </button>
            </div>

            <div className="grid grid-cols-3 gap-3">
              {apps.map((app) => (
                <div
                  key={app.name}
                  className="app-icon"
                  style={{ backgroundColor: app.color }}
                  title={app.name}
                >
                  <span className="text-2xl">{app.icon}</span>
                </div>
              ))}
            </div>
          </div>

          {/* Conversations panel */}
          <div className="panel-card">
            <div className="flex items-center gap-2 text-white/60 text-sm mb-4">
              <MessageSquare size={16} />
              Keep talking to Copilot
            </div>

            <div className="space-y-2">
              {conversations.map((conv, i) => (
                <div key={i} className="file-item">
                  <div className="w-10 h-10 rounded-full bg-white/10 flex items-center justify-center">
                    <MessageSquare size={18} className="text-white/60" />
                  </div>
                  <div className="flex-1">
                    <p className="text-white text-sm">{conv.title}</p>
                    <p className="text-white/40 text-xs">{conv.time}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Footer */}
        <p className="text-white/30 text-xs mt-8">
          Copilot may make mistakes.
        </p>
      </div>
    </div>
  )
}

export default App
