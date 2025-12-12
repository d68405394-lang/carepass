import React, { useState } from 'react';
import axios from 'axios';

// APIエンドポイント
const API_URL = 'http://localhost:8000/api/progress/';

// UI/UX原則: 入力の最小化（音声入力）と視覚的証明（画像・動画）
const ProgressRecordInput = () => {
  const [textInput, setTextInput] = useState(''); // 音声入力されたテキスト
  const [mediaFile, setMediaFile] = useState(null); // アップロードされた画像/動画ファイル
  const [message, setMessage] = useState(''); // ユーザーへのフィードバックメッセージ
  const [isRecording, setIsRecording] = useState(false); // 録音中かどうか

  // アイコンのスタイル
  const iconStyle = {
    fontSize: '48px',
    cursor: 'pointer',
    margin: '20px',
    padding: '20px',
    borderRadius: '50%',
    border: '2px solid #ccc',
    transition: 'all 0.3s',
  };

  // 録音開始/停止のシミュレーション
  const handleRecordToggle = () => {
    if (isRecording) {
      // 録音停止
      setIsRecording(false);
      setMessage('🎙️ 録音を停止しました。テキストボックスに内容が入力されます。');
      // 🚨 実際にはここで音声認識APIを叩き、結果をsetTextInputにセットする
      setTextInput('利用者A様は、本日も笑顔で活動に参加されました。特にブロック遊びに集中し、新しい形のタワーを完成させました。');
    } else {
      // 録音開始
      setIsRecording(true);
      setMessage('🔴 録音中... 話し始めてください。');
    }
  };

  // ファイル選択の処理
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setMediaFile(file);
      setMessage(`📸 ファイルを選択しました: ${file.name}`);
    }
  };

  // 送信処理
  const handleSubmit = async () => {
    if (!textInput && !mediaFile) {
      setMessage('⚠️ 記録内容（テキストまたはメディア）を入力してください。');
      return;
    }

    setMessage('送信中...');
    
    // 🚨 実際にはFormDataを使ってファイルとテキストを同時に送信する
    // 簡略化のため、ここではテキストのみを送信するAPIコールをシミュレーション
    try {
      // 実際には、利用者ID、職員ID、記録日時なども含める
    // 🚨 ProgressAssessmentモデルには、staff, assessment_date, notes, media_url が必要
    // media_url はファイルアップロードが完了した後のURLを想定

    try {
      const payload = {
        staff: 1, // 仮の職員ID
        assessment_date: new Date().toISOString(),
        notes: textInput,
        # media_url: mediaFile ? 'uploaded_url_placeholder' : null, // ファイルアップロードロジックは省略
      };

      // APIコール
      const response = await axios.post(API_URL, payload);

      // 成功
      setMessage('✅ 進捗記録が正常に送信されました。');
      setTextInput('');
      setMediaFile(null);

    } catch (error) {
      setMessage('❌ 進捗記録の送信に失敗しました。');
      console.error('送信エラー:', error.response?.data || error.message);
    }
  };

  return (
    <div style={{ 
      display: 'flex', flexDirection: 'column', alignItems: 'center', 
      padding: '50px', fontFamily: 'Arial, sans-serif' 
    }}>
      <h1>進捗記録入力（音声・画像）</h1>
      
      {/* フィードバックメッセージ */}
      {message && (
        <div style={{ 
          padding: '15px', margin: '20px 0', 
          backgroundColor: message.startsWith('✅') ? '#e6ffe6' : (message.startsWith('❌') ? '#ffe6e6' : '#fffbe6'),
          border: `1px solid ${message.startsWith('✅') ? '#4CAF50' : (message.startsWith('❌') ? '#f44336' : '#ffc107')}`,
          borderRadius: '5px', width: '80%', textAlign: 'center'
        }}>
          {message}
        </div>
      )}

      {/* 音声入力エリア */}
      <div style={{ display: 'flex', alignItems: 'center', margin: '20px 0' }}>
        <div 
          onClick={handleRecordToggle}
          style={{
            ...iconStyle,
            color: isRecording ? 'white' : '#333',
            backgroundColor: isRecording ? '#f44336' : 'transparent',
            borderColor: isRecording ? '#f44336' : '#ccc',
            transform: isRecording ? 'scale(1.1)' : 'scale(1)',
          }}
        >
          {isRecording ? '■' : '🎙️'}
        </div>
        <p style={{ marginLeft: '20px', color: isRecording ? '#f44336' : '#333' }}>
          {isRecording ? 'タップで停止' : 'タップで録音開始'}
        </p>
      </div>

      {/* テキスト入力エリア */}
      <textarea
        value={textInput}
        onChange={(e) => setTextInput(e.target.value)}
        placeholder="音声認識されたテキスト、または手動入力"
        rows="6"
        style={{ width: '80%', padding: '10px', fontSize: '16px', borderRadius: '5px', border: '1px solid #ccc' }}
      />

      {/* 画像/動画入力エリア */}
      <div style={{ display: 'flex', alignItems: 'center', margin: '20px 0' }}>
        <label htmlFor="media-upload" style={{ ...iconStyle, borderColor: '#2196F3', color: '#2196F3' }}>
          📸
        </label>
        <input
          type="file"
          id="media-upload"
          accept="image/*,video/*"
          onChange={handleFileChange}
          style={{ display: 'none' }}
        />
        <p style={{ marginLeft: '20px' }}>
          {mediaFile ? `選択中: ${mediaFile.name}` : 'タップで写真/動画を選択'}
        </p>
      </div>
      
      {/* 送信ボタン */}
      <button
        onClick={handleSubmit}
        style={{
          padding: '15px 40px',
          fontSize: '20px',
          fontWeight: 'bold',
          color: 'white',
          backgroundColor: '#4CAF50',
          border: 'none',
          borderRadius: '8px',
          cursor: 'pointer',
          marginTop: '30px',
          boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
        }}
      >
        記録を送信
      </button>
    </div>
  );
};

export default ProgressRecordInput;
