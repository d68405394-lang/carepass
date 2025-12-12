import { useState } from 'react'
import PeerReviewForm from './PeerReviewForm'
import EvaluationSummary from './EvaluationSummary'
import AiRecordGenerator from './AiRecordGenerator'
import './responsive.css'

function App() {
  const [currentView, setCurrentView] = useState('ai-record'); // デフォルトでAI記録生成画面を表示

  return (
    <div>
      {/* ナビゲーションメニュー */}
      <nav style={{
        padding: '15px',
        backgroundColor: '#2196F3',
        color: 'white',
        marginBottom: '20px',
        position: 'sticky',
        top: 0,
        zIndex: 1000,
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h2 style={{ margin: 0, marginBottom: '10px' }}>福祉事業所向け請求管理システム</h2>
        <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <button
            onClick={() => setCurrentView('ai-record')}
            style={{
              padding: '10px 20px',
              fontSize: '14px',
              fontWeight: 'bold',
              color: currentView === 'ai-record' ? '#2196F3' : 'white',
              backgroundColor: currentView === 'ai-record' ? 'white' : 'transparent',
              border: '2px solid white',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            🤖 AI記録生成
          </button>
          <button
            onClick={() => setCurrentView('evaluation')}
            style={{
              padding: '10px 20px',
              fontSize: '14px',
              fontWeight: 'bold',
              color: currentView === 'evaluation' ? '#2196F3' : 'white',
              backgroundColor: currentView === 'evaluation' ? 'white' : 'transparent',
              border: '2px solid white',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            📈 評価サマリー
          </button>
          <button
            onClick={() => setCurrentView('peer-review')}
            style={{
              padding: '10px 20px',
              fontSize: '14px',
              fontWeight: 'bold',
              color: currentView === 'peer-review' ? '#2196F3' : 'white',
              backgroundColor: currentView === 'peer-review' ? 'white' : 'transparent',
              border: '2px solid white',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            👥 相互評価
          </button>
        </div>
      </nav>

      {/* 現在のビューを表示 */}
      {currentView === 'ai-record' && <AiRecordGenerator />}
      {currentView === 'evaluation' && <EvaluationSummary />}
      {currentView === 'peer-review' && <PeerReviewForm />}
    </div>
  )
}

export default App
