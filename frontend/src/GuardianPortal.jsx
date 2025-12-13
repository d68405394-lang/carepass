import React, { useState, useEffect } from 'react';
import './GuardianPortal.css';

function GuardianPortal() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [clientId, setClientId] = useState(null);
  const [clientName, setClientName] = useState('');
  const [dashboardData, setDashboardData] = useState(null);
  const [activities, setActivities] = useState([]);
  const [unreadMessages, setUnreadMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  // ログイン処理
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/api/guardian/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      const data = await response.json();

      if (data.success) {
        setIsLoggedIn(true);
        setClientId(data.client_id);
        setClientName(data.client_name);
        loadDashboardData(data.client_id);
      } else {
        setMessage(`❌ ${data.error}`);
      }
    } catch (error) {
      setMessage(`❌ エラーが発生しました: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  // ダッシュボードデータを読み込む
  const loadDashboardData = async (clientIdParam) => {
    try {
      const response = await fetch(`http://localhost:8000/api/guardian/dashboard/${clientIdParam}/`);
      const data = await response.json();

      if (data.success) {
        setDashboardData(data.data);
      }
    } catch (error) {
      console.error('Error loading dashboard:', error);
    }
  };

  // 活動記録を読み込む
  const loadActivities = async () => {
    if (!clientId) return;

    try {
      const response = await fetch(`http://localhost:8000/api/guardian/activities/${clientId}/`);
      const data = await response.json();

      if (data.success) {
        setActivities(data.logs);
      }
    } catch (error) {
      console.error('Error loading activities:', error);
    }
  };

  // 未読メッセージを読み込む
  const loadUnreadMessages = async () => {
    if (!clientId) return;

    try {
      const response = await fetch(`http://localhost:8000/api/email/unread/${clientId}/`);
      const data = await response.json();

      if (data.success) {
        setUnreadMessages(data.messages);
      }
    } catch (error) {
      console.error('Error loading unread messages:', error);
    }
  };

  // ログアウト処理
  const handleLogout = async () => {
    try {
      await fetch('http://localhost:8000/api/guardian/logout/', {
        method: 'POST',
      });

      setIsLoggedIn(false);
      setClientId(null);
      setClientName('');
      setDashboardData(null);
      setActivities([]);
      setUnreadMessages([]);
      setEmail('');
      setPassword('');
    } catch (error) {
      console.error('Error logging out:', error);
    }
  };

  // ログイン後にデータを読み込む
  useEffect(() => {
    if (isLoggedIn && clientId) {
      loadActivities();
      loadUnreadMessages();
    }
  }, [isLoggedIn, clientId]);

  // ログインフォーム
  if (!isLoggedIn) {
    return (
      <div className="guardian-portal">
        <div className="login-container">
          <h2>🏠 保護者ポータル</h2>
          <p>お子様の活動記録やメッセージを確認できます</p>

          {message && (
            <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
              {message}
            </div>
          )}

          <form onSubmit={handleLogin}>
            <div className="form-group">
              <label htmlFor="email">メールアドレス</label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="example@email.com"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="password">パスワード</label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="パスワード"
                required
              />
            </div>

            <button type="submit" disabled={loading} className="login-btn">
              {loading ? 'ログイン中...' : 'ログイン'}
            </button>
          </form>
        </div>
      </div>
    );
  }

  // ダッシュボード
  return (
    <div className="guardian-portal">
      <div className="portal-header">
        <h2>🏠 保護者ポータル</h2>
        <div className="header-info">
          <span className="client-name">{clientName}さん</span>
          <button onClick={handleLogout} className="logout-btn">ログアウト</button>
        </div>
      </div>

      {dashboardData && (
        <div className="dashboard-summary">
          <div className="summary-card">
            <h3>📬 未読メッセージ</h3>
            <p className="count">{dashboardData.unread_messages}件</p>
          </div>

          <div className="summary-card">
            <h3>📝 最新活動</h3>
            <p className="count">{dashboardData.latest_activities.length}件</p>
          </div>

          {dashboardData.ai_analysis && (
            <div className="summary-card">
              <h3>🤖 AI分析</h3>
              <p className="sentiment">{dashboardData.ai_analysis.sentiment}</p>
            </div>
          )}
        </div>
      )}

      {/* 未読メッセージ */}
      {unreadMessages.length > 0 && (
        <div className="section">
          <h3>📬 未読メッセージ</h3>
          <div className="message-list">
            {unreadMessages.map(msg => (
              <div key={msg.recipient_id} className="message-item">
                <div className="message-header">
                  <strong>{msg.subject}</strong>
                  <span className="message-date">{new Date(msg.sent_at).toLocaleDateString('ja-JP')}</span>
                </div>
                <p className="message-body">{msg.body.substring(0, 100)}...</p>
                <span className="sender">送信者: {msg.sender}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* 活動記録 */}
      <div className="section">
        <h3>📝 活動記録</h3>
        {activities.length > 0 ? (
          <div className="activity-list">
            {activities.map(activity => (
              <div key={activity.id} className="activity-item">
                <div className="activity-header">
                  <span className="activity-type">{activity.activity_type}</span>
                  <span className="activity-date">{new Date(activity.date).toLocaleDateString('ja-JP')}</span>
                </div>
                <p className="activity-description">{activity.description}</p>
                {activity.staff_comment && (
                  <p className="staff-comment">💬 {activity.staff_comment}</p>
                )}
                {activity.has_photo && (
                  <div className="activity-photo">
                    <img src={activity.photo_url} alt="活動写真" />
                  </div>
                )}
              </div>
            ))}
          </div>
        ) : (
          <p>まだ活動記録がありません</p>
        )}
      </div>
    </div>
  );
}

export default GuardianPortal;
