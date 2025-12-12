import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8000/api/peerreview/';

// 職員リスト（仮データ）
const STAFF_LIST = [
  { id: 1, name: '佐藤 太郎' },
  { id: 2, name: '田中 花子' },
  { id: 3, name: '山田 次郎' },
];

const PeerReviewForm = () => {
  // 🚨 実際はログインユーザーのIDを使用
  const [reviewerId, setReviewerId] = useState(1); 
  const [reviewedStaffId, setReviewedStaffId] = useState('');
  const [score, setScore] = useState(5); // 1-5のスコア
  const [comment, setComment] = useState('');
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!reviewedStaffId || !score || !comment) {
      setMessage('⚠️ 全ての項目を入力してください。');
      return;
    }

    setLoading(true);
    setMessage('送信中...');

    try {
      const payload = {
        reviewer: reviewerId,
        reviewed_staff: reviewedStaffId,
        score: score,
        comment: comment,
        review_date: new Date().toISOString(),
      };

      const response = await axios.post(API_URL, payload);

      setMessage('✅ 相互評価が正常に送信されました。ご協力ありがとうございます！');
      setReviewedStaffId('');
      setScore(5);
      setComment('');

    } catch (error) {
      setMessage('❌ 評価の送信に失敗しました。');
      console.error('評価送信エラー:', error.response?.data || error.message);
    } finally {
      setLoading(false);
    }
  };

  const formStyle = {
    display: 'flex',
    flexDirection: 'column',
    gap: '20px',
    width: '400px',
    padding: '20px',
    border: '1px solid #ccc',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
  };

  const inputStyle = {
    padding: '10px',
    borderRadius: '4px',
    border: '1px solid #ddd',
    fontSize: '16px',
  };

  const labelStyle = {
    fontWeight: 'bold',
    marginBottom: '5px',
  };

  return (
    <div style={{ 
      display: 'flex', flexDirection: 'column', alignItems: 'center', 
      padding: '50px', fontFamily: 'Arial, sans-serif' 
    }}>
      <h1>職員相互評価入力</h1>
      
      {/* フィードバックメッセージ */}
      {message && (
        <div style={{ 
          padding: '15px', margin: '20px 0', 
          backgroundColor: message.startsWith('✅') ? '#e6ffe6' : (message.startsWith('❌') ? '#ffe6e6' : '#fffbe6'),
          border: `1px solid ${message.startsWith('✅') ? '#4CAF50' : (message.startsWith('❌') ? '#f44336' : '#ffc107')}`,
          borderRadius: '5px', width: '400px', textAlign: 'center'
        }}>
          {message}
        </div>
      )}

      <form onSubmit={handleSubmit} style={formStyle}>
        
        {/* 評価者（ログインユーザー） */}
        <div>
          <div style={labelStyle}>評価者 (あなた):</div>
          <input type="text" value={STAFF_LIST.find(s => s.id === reviewerId)?.name || '未設定'} style={{...inputStyle, backgroundColor: '#eee'}} readOnly />
        </div>

        {/* 対象職員の選択 */}
        <div>
          <label htmlFor="reviewedStaff" style={labelStyle}>評価対象の職員:</label>
          <select
            id="reviewedStaff"
            value={reviewedStaffId}
            onChange={(e) => setReviewedStaffId(e.target.value)}
            style={inputStyle}
            required
          >
            <option value="">選択してください</option>
            {STAFF_LIST.filter(s => s.id !== reviewerId).map(staff => (
              <option key={staff.id} value={staff.id}>{staff.name}</option>
            ))}
          </select>
        </div>

        {/* スコアの入力 */}
        <div>
          <label style={labelStyle}>スコア (1-5): {score}</label>
          <div style={{ display: 'flex', justifyContent: 'space-between' }}>
            {[1, 2, 3, 4, 5].map(s => (
              <label key={s} style={{ cursor: 'pointer' }}>
                <input 
                  type="radio" 
                  name="score" 
                  value={s} 
                  checked={score === s} 
                  onChange={() => setScore(s)} 
                  required
                />
                {s}
              </label>
            ))}
          </div>
        </div>

        {/* コメントの入力 */}
        <div>
          <label htmlFor="comment" style={labelStyle}>コメント:</label>
          <textarea
            id="comment"
            value={comment}
            onChange={(e) => setComment(e.target.value)}
            placeholder="具体的な行動や貢献について記述してください"
            rows="4"
            style={{...inputStyle, resize: 'vertical'}}
            required
          />
        </div>

        {/* 送信ボタン */}
        <button
          type="submit"
          disabled={loading}
          style={{
            padding: '10px 20px',
            fontSize: '18px',
            fontWeight: 'bold',
            color: 'white',
            backgroundColor: loading ? '#ccc' : '#007bff',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
          }}
        >
          {loading ? '送信中...' : '評価を送信'}
        </button>
      </form>
    </div>
  );
};

export default PeerReviewForm;
