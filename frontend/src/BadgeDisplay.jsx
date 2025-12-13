import React, { useState, useEffect } from 'react';
import './BadgeDisplay.css';

function BadgeDisplay({ clientId }) {
  const [badges, setBadges] = useState([]);
  const [points, setPoints] = useState(null);
  const [leaderboard, setLeaderboard] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (clientId) {
      loadBadges();
      loadPoints();
    }
    loadLeaderboard();
  }, [clientId]);

  // バッジを読み込む
  const loadBadges = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/gamification/badges/${clientId}/`);
      const data = await response.json();

      if (data.success) {
        setBadges(data.badges);
      }
    } catch (error) {
      console.error('Error loading badges:', error);
    }
  };

  // ポイントを読み込む
  const loadPoints = async () => {
    try {
      const response = await fetch(`http://localhost:8000/api/gamification/points/${clientId}/`);
      const data = await response.json();

      if (data.success) {
        setPoints(data.data);
      }
    } catch (error) {
      console.error('Error loading points:', error);
    } finally {
      setLoading(false);
    }
  };

  // ランキングを読み込む
  const loadLeaderboard = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/gamification/leaderboard/');
      const data = await response.json();

      if (data.success) {
        setLeaderboard(data.ranking);
      }
    } catch (error) {
      console.error('Error loading leaderboard:', error);
    }
  };

  // バッジチェックを実行
  const checkBadges = async () => {
    if (!clientId) return;

    try {
      const response = await fetch(`http://localhost:8000/api/gamification/check_badges/${clientId}/`, {
        method: 'POST',
      });
      const data = await response.json();

      if (data.success && data.newly_earned_count > 0) {
        alert(`🎉 新しいバッジを${data.newly_earned_count}個獲得しました！`);
        loadBadges();
        loadPoints();
      }
    } catch (error) {
      console.error('Error checking badges:', error);
    }
  };

  if (loading) {
    return <div className="badge-display">読み込み中...</div>;
  }

  return (
    <div className="badge-display">
      {/* ポイント表示 */}
      {points && (
        <div className="points-section">
          <h3>🏆 ポイント</h3>
          <div className="points-grid">
            <div className="point-card total">
              <div className="point-value">{points.total_points}</div>
              <div className="point-label">合計ポイント</div>
            </div>
            <div className="point-card">
              <div className="point-value">{points.attendance_points}</div>
              <div className="point-label">出席</div>
            </div>
            <div className="point-card">
              <div className="point-value">{points.activity_points}</div>
              <div className="point-label">活動</div>
            </div>
            <div className="point-card">
              <div className="point-value">{points.growth_points}</div>
              <div className="point-label">成長</div>
            </div>
          </div>
        </div>
      )}

      {/* バッジ表示 */}
      <div className="badges-section">
        <div className="section-header">
          <h3>🎖️ 獲得バッジ ({badges.length}個)</h3>
          {clientId && (
            <button onClick={checkBadges} className="check-btn">
              バッジをチェック
            </button>
          )}
        </div>

        {badges.length > 0 ? (
          <div className="badges-grid">
            {badges.map(badge => (
              <div key={badge.id} className="badge-card">
                <div className="badge-icon">{badge.icon}</div>
                <div className="badge-name">{badge.name}</div>
                <div className="badge-description">{badge.description}</div>
                <div className="badge-earned">
                  {new Date(badge.earned_at).toLocaleDateString('ja-JP')}
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="no-badges">まだバッジを獲得していません</p>
        )}
      </div>

      {/* ランキング */}
      <div className="leaderboard-section">
        <h3>📊 ランキング TOP10</h3>
        {leaderboard.length > 0 ? (
          <div className="leaderboard-table">
            <table>
              <thead>
                <tr>
                  <th>順位</th>
                  <th>名前</th>
                  <th>ポイント</th>
                  <th>バッジ</th>
                </tr>
              </thead>
              <tbody>
                {leaderboard.map(entry => (
                  <tr key={entry.rank} className={entry.client_id === clientId ? 'highlight' : ''}>
                    <td className="rank">
                      {entry.rank === 1 && '🥇'}
                      {entry.rank === 2 && '🥈'}
                      {entry.rank === 3 && '🥉'}
                      {entry.rank > 3 && entry.rank}
                    </td>
                    <td>{entry.client_name}</td>
                    <td>{entry.total_points}pt</td>
                    <td>{entry.badge_count}個</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <p>ランキングデータがありません</p>
        )}
      </div>
    </div>
  );
}

export default BadgeDisplay;
