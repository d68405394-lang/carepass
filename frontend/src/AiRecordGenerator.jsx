import React, { useState, useEffect } from 'react';
import axios from 'axios';

const AiRecordGenerator = () => {
  const [clients, setClients] = useState([]);
  const [selectedClientId, setSelectedClientId] = useState('');
  const [inputText, setInputText] = useState('');
  const [generatedRecord, setGeneratedRecord] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');

  // 利用者一覧を取得
  useEffect(() => {
    const fetchClients = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/clients/');
        setClients(response.data);
      } catch (error) {
        console.error("利用者一覧の取得に失敗しました:", error);
      }
    };
    fetchClients();
  }, []);

  // AI記録生成を実行
  const handleGenerateRecord = async () => {
    if (!selectedClientId || !inputText) {
      setError('利用者と入力テキストを選択してください。');
      return;
    }

    setLoading(true);
    setError('');
    setSuccessMessage('');
    setGeneratedRecord('');

    try {
      const response = await axios.post('http://localhost:8000/api/ai_record_generation/', {
        client_id: selectedClientId,
        input_text: inputText
      });

      setGeneratedRecord(response.data.draft_record);
      setSuccessMessage('記録ドラフトが生成されました！内容を確認して、必要に応じて編集してください。');
    } catch (error) {
      console.error("AI記録生成に失敗しました:", error);
      setError('AI記録生成中にエラーが発生しました。もう一度お試しください。');
    } finally {
      setLoading(false);
    }
  };

  // 生成された記録をクリア
  const handleClear = () => {
    setInputText('');
    setGeneratedRecord('');
    setError('');
    setSuccessMessage('');
  };

  // 生成された記録を承認（実際にはProgressAssessmentに保存）
  const handleApprove = async () => {
    if (!generatedRecord) {
      setError('承認する記録がありません。');
      return;
    }

    // 実際には、ProgressAssessmentに保存するAPIを呼び出す
    alert('記録が承認されました！（実装予定: ProgressAssessmentに保存）');
    handleClear();
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ borderBottom: '2px solid #333', paddingBottom: '10px' }}>
        🤖 AI記録自動生成
      </h1>
      <p style={{ color: '#666', marginBottom: '20px' }}>
        職員の断片的な入力（音声メモ、箇条書き）から、法定形式の進捗記録を自動生成します。
      </p>

      {/* 利用者選択 */}
      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
          利用者を選択:
        </label>
        <select
          value={selectedClientId}
          onChange={(e) => setSelectedClientId(e.target.value)}
          style={{
            width: '100%',
            padding: '10px',
            fontSize: '16px',
            border: '1px solid #ccc',
            borderRadius: '4px'
          }}
        >
          <option value="">-- 利用者を選択してください --</option>
          {clients.map((client) => (
            <option key={client.id} value={client.id}>
              {client.full_name} ({client.client_code})
            </option>
          ))}
        </select>
      </div>

      {/* 断片的な入力 */}
      <div style={{ marginBottom: '20px' }}>
        <label style={{ display: 'block', fontWeight: 'bold', marginBottom: '5px' }}>
          断片的な入力（音声メモ、箇条書き）:
        </label>
        <textarea
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          placeholder="例: 今日は挨拶ができた。バランスボールで5分遊んだ。集中して取り組めた。"
          style={{
            width: '100%',
            minHeight: '120px',
            padding: '10px',
            fontSize: '16px',
            border: '1px solid #ccc',
            borderRadius: '4px',
            resize: 'vertical'
          }}
        />
      </div>

      {/* 生成ボタン */}
      <div style={{ marginBottom: '20px' }}>
        <button
          onClick={handleGenerateRecord}
          disabled={loading}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            fontWeight: 'bold',
            color: 'white',
            backgroundColor: loading ? '#ccc' : '#4CAF50',
            border: 'none',
            borderRadius: '4px',
            cursor: loading ? 'not-allowed' : 'pointer',
            marginRight: '10px'
          }}
        >
          {loading ? '生成中...' : '🤖 AI記録を生成'}
        </button>
        <button
          onClick={handleClear}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            fontWeight: 'bold',
            color: 'white',
            backgroundColor: '#9E9E9E',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          クリア
        </button>
      </div>

      {/* エラーメッセージ */}
      {error && (
        <div style={{
          padding: '15px',
          marginBottom: '20px',
          backgroundColor: '#FFEBEE',
          border: '1px solid #EF5350',
          borderRadius: '4px',
          color: '#C62828'
        }}>
          ⚠️ {error}
        </div>
      )}

      {/* 成功メッセージ */}
      {successMessage && (
        <div style={{
          padding: '15px',
          marginBottom: '20px',
          backgroundColor: '#E8F5E9',
          border: '1px solid #66BB6A',
          borderRadius: '4px',
          color: '#2E7D32'
        }}>
          ✅ {successMessage}
        </div>
      )}

      {/* 生成された記録 */}
      {generatedRecord && (
        <div style={{
          padding: '20px',
          backgroundColor: '#F5F5F5',
          border: '2px solid #4CAF50',
          borderRadius: '8px',
          marginBottom: '20px'
        }}>
          <h3 style={{ marginTop: 0, color: '#4CAF50' }}>
            📝 生成された記録ドラフト
          </h3>
          <div style={{
            padding: '15px',
            backgroundColor: 'white',
            border: '1px solid #ddd',
            borderRadius: '4px',
            marginBottom: '15px',
            lineHeight: '1.6',
            fontSize: '16px'
          }}>
            {generatedRecord}
          </div>
          <div style={{ display: 'flex', gap: '10px' }}>
            <button
              onClick={handleApprove}
              style={{
                padding: '10px 20px',
                fontSize: '16px',
                fontWeight: 'bold',
                color: 'white',
                backgroundColor: '#2196F3',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              ✅ 承認して保存
            </button>
            <button
              onClick={() => setGeneratedRecord('')}
              style={{
                padding: '10px 20px',
                fontSize: '16px',
                fontWeight: 'bold',
                color: 'white',
                backgroundColor: '#F44336',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              ❌ 破棄
            </button>
          </div>
        </div>
      )}

      {/* 使い方ガイド */}
      <div style={{
        padding: '20px',
        backgroundColor: '#E3F2FD',
        border: '1px solid #2196F3',
        borderRadius: '8px',
        marginTop: '30px'
      }}>
        <h3 style={{ marginTop: 0, color: '#1976D2' }}>
          💡 使い方ガイド
        </h3>
        <ol style={{ lineHeight: '1.8', paddingLeft: '20px' }}>
          <li>利用者を選択します</li>
          <li>断片的な入力（音声メモ、箇条書き）を入力します</li>
          <li>「🤖 AI記録を生成」ボタンをクリックします</li>
          <li>生成された記録ドラフトを確認します</li>
          <li>必要に応じて編集し、「✅ 承認して保存」をクリックします</li>
        </ol>
        <p style={{ marginBottom: 0, color: '#666' }}>
          <strong>ヒント:</strong> 断片的な入力は、箇条書きや短い文章で構いません。AIが個別支援計画書の情報を参照して、法定形式の記録を生成します。
        </p>
      </div>
    </div>
  );
};

export default AiRecordGenerator;
