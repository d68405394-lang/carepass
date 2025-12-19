import { Link } from 'react-router-dom';
import './LandingPage.css';

function LandingPage() {
  return (
    <div className="landing-container">
      <div className="landing-content">
        <div className="logo-section">
          <div className="logo-icon">🏥</div>
          <h1 className="logo-text">Care Pass</h1>
        </div>
        <h2 className="subtitle">福祉管理システム</h2>
        
        <div className="features-grid">
          <Link to="/progress" className="feature-card">
            <div className="feature-icon">📊</div>
            <h3>進捗管理</h3>
            <p>利用者の進捗状況をリアルタイムで追跡し、データ駆動型のケアプランを提供します。</p>
          </Link>
          
          <Link to="/ai-analysis" className="feature-card">
            <div className="feature-icon">🤖</div>
            <h3>AI分析</h3>
            <p>感情分析と予測機能により、より効果的な福祉サービスを実現します。</p>
          </Link>
          
          <Link to="/billing" className="feature-card">
            <div className="feature-icon">💰</div>
            <h3>請求管理</h3>
            <p>国保連請求や給与計算を自動化し、事務作業の負担を大幅に削減します。</p>
          </Link>
          
          <Link to="/guardian" className="feature-card">
            <div className="feature-icon">📱</div>
            <h3>保護者ポータル</h3>
            <p>保護者とのコミュニケーションを円滑にし、透明性の高いケアサービスを提供します。</p>
          </Link>
        </div>
        
        <div className="footer">
          <p>Django Backend API • PostgreSQL Database • AI Integration</p>
          <p>© 2024 Care Pass - 福祉管理システム</p>
        </div>
      </div>
    </div>
  );
}

export default LandingPage;
