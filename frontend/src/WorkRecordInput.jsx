import React, { useState } from 'react';
import axios from 'axios';

// APIエンドポイント
const API_URL = 'http://localhost:8000/api/workrecords/';

// サービス種別の選択肢（仮）
// 実際にはAPIから取得するか、設定ファイルから読み込む
const SERVICE_TYPES = [
  { id: 'Hodei', name: '放課後等デイサービス' },
  { id: 'Miniha', name: '児童発達支援' },
  { id: 'Jiritsu', name: '自立訓練' },
];

// UI/UX原則: ワンタップ操作とフィードバックの最小化
const WorkRecordInput = () => {
  const [isWorking, setIsWorking] = useState(false); // 勤務中かどうか
  const [staffId, setStaffId] = useState(1); // 🚨 仮の職員ID。実際はログイン情報から取得
  const [selectedService, setSelectedService] = useState(null); // 選択されたサービス種別
  const [showServiceModal, setShowServiceModal] = useState(false); // サービス選択モーダルの表示
  const [message, setMessage] = useState(''); // ユーザーへのフィードバックメッセージ

  // 勤務開始/終了ボタンのスタイル
  const buttonStyle = {
    width: '200px',
    height: '200px',
    borderRadius: '50%',
    fontSize: '24px',
    fontWeight: 'bold',
    color: 'white',
    cursor: 'pointer',
    border: 'none',
    boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
    transition: 'background-color 0.3s, transform 0.1s',
    margin: '20px',
  };

  // 勤務開始処理
  const handleStartWork = async (serviceId) => {
    setShowServiceModal(false);
    setMessage('送信中...');
    
    try {
      // 勤務開始APIコール
      const response = await axios.post(API_URL, {
        staff: staffId,
        service_type: serviceId,
        start_time: new Date().toISOString(), // 現在時刻をISO形式で送信
        # end_time は null のまま
      });

      // 成功
      setIsWorking(true);
      setSelectedService(serviceId);
      setMessage(`✅ 勤務開始: ${SERVICE_TYPES.find(s => s.id === serviceId).name}。頑張ってください！`);

    } catch (error) {
      // 失敗（主に兼務専従違反エラー）
      const errorMessage = error.response?.data?.non_field_errors?.[0] || '勤務開始に失敗しました。';
      setMessage(`❌ 勤務開始失敗: ${errorMessage}`);
      console.error('勤務開始エラー:', error.response?.data || error.message);
    }
  };

  // 勤務終了処理
  const handleEndWork = async () => {
    setMessage('送信中...');
    
    try {
      // 勤務終了APIコール
      // 実際には、進行中のWorkRecordのIDを取得し、PATCH/PUTでend_timeを更新するが、
      // 今回は簡略化のため、新しいレコードとして終了時刻を送信する（バックエンドで処理が必要）
      // 🚨 現状のAPI設計では進行中のレコードの特定が困難なため、ここでは**仮の終了処理**とする
      
      // 実際には進行中のWorkRecordのIDを取得し、PATCH/PUTでend_timeを更新する
      // 例: await axios.patch(`${API_URL}${currentWorkRecordId}/`, { end_time: new Date().toISOString() });

      // 🚨 暫定対応: 勤務中フラグをリセットし、メッセージを表示
      setIsWorking(false);
      setSelectedService(null);
      setMessage(`✅ 勤務終了: お疲れ様でした！`);

    } catch (error) {
      setMessage('❌ 勤務終了処理に失敗しました。');
      console.error('勤務終了エラー:', error.response?.data || error.message);
    }
  };

  // メインボタンのクリックハンドラ
  const handleMainButtonClick = () => {
    if (isWorking) {
      handleEndWork();
    } else {
      // 勤務開始時はサービス種別を選択させる
      setShowServiceModal(true);
    }
  };

  // サービス選択モーダル
  const ServiceModal = () => (
    <div style={{
      position: 'fixed', top: 0, left: 0, right: 0, bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.5)',
      display: 'flex', justifyContent: 'center', alignItems: 'center',
      zIndex: 1000,
    }}>
      <div style={{
        backgroundColor: 'white', padding: '30px', borderRadius: '10px',
        textAlign: 'center', width: '300px',
      }}>
        <h3>サービス種別を選択してください</h3>
        {SERVICE_TYPES.map(service => (
          <button
            key={service.id}
            onClick={() => handleStartWork(service.id)}
            style={{
              padding: '10px 20px', margin: '10px',
              fontSize: '16px', cursor: 'pointer',
              backgroundColor: '#4CAF50', color: 'white', border: 'none',
              borderRadius: '5px',
            }}
          >
            {service.name}
          </button>
        ))}
        <button
          onClick={() => setShowServiceModal(false)}
          style={{
            padding: '10px 20px', margin: '10px',
            fontSize: '16px', cursor: 'pointer',
            backgroundColor: '#f44336', color: 'white', border: 'none',
            borderRadius: '5px',
          }}
        >
          キャンセル
        </button>
      </div>
    </div>
  );

  return (
    <div style={{ 
      display: 'flex', flexDirection: 'column', alignItems: 'center', 
      padding: '50px', fontFamily: 'Arial, sans-serif' 
    }}>
      <h1>職員勤務入力（打刻）</h1>
      
      {/* フィードバックメッセージ */}
      {message && (
        <div style={{ 
          padding: '15px', margin: '20px 0', 
          backgroundColor: message.startsWith('✅') ? '#e6ffe6' : '#ffe6e6',
          border: `1px solid ${message.startsWith('✅') ? '#4CAF50' : '#f44336'}`,
          borderRadius: '5px', width: '80%', textAlign: 'center'
        }}>
          {message}
        </div>
      )}

      {/* 勤務状況表示 */}
      <div style={{ margin: '20px 0', fontSize: '18px', color: isWorking ? '#4CAF50' : '#f44336' }}>
        {isWorking 
          ? `🟢 勤務中: ${SERVICE_TYPES.find(s => s.id === selectedService)?.name}` 
          : '🔴 勤務外'}
      </div>

      {/* メインボタン */}
      <button
        onClick={handleMainButtonClick}
        style={{
          ...buttonStyle,
          backgroundColor: isWorking ? '#f44336' : '#4CAF50', // 退勤は赤、出勤は緑
          transform: showServiceModal ? 'scale(0.95)' : 'scale(1)',
        }}
        disabled={showServiceModal}
      >
        {isWorking ? '退勤' : '出勤'}
      </button>

      {/* サービス選択モーダル */}
      {showServiceModal && <ServiceModal />}
    </div>
  );
};

export default WorkRecordInput;
