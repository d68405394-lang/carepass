import React, { useRef, useState } from 'react';
import SignatureCanvas from 'react-signature-canvas';
import './SignaturePad.css';

const SignaturePad = ({ clientId, clientName, onSignatureSaved }) => {
  const sigCanvas = useRef(null);
  const [isSaving, setIsSaving] = useState(false);
  const [message, setMessage] = useState('');

  // 署名をクリアする
  const clearSignature = () => {
    sigCanvas.current.clear();
    setMessage('');
  };

  // 署名を保存する
  const saveSignature = async () => {
    if (sigCanvas.current.isEmpty()) {
      setMessage('署名を入力してください。');
      return;
    }

    setIsSaving(true);
    setMessage('');

    try {
      // 署名画像をBase64形式で取得
      const signatureData = sigCanvas.current.toDataURL('image/png');

      // バックエンドAPIに送信
      const response = await fetch(`/api/save_signature/${clientId}/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          signature_data: signatureData,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setMessage(`✅ ${data.message}`);
        sigCanvas.current.clear();
        
        // 親コンポーネントに通知
        if (onSignatureSaved) {
          onSignatureSaved(data);
        }
      } else {
        setMessage(`❌ エラー: ${data.error}`);
      }
    } catch (error) {
      setMessage(`❌ 通信エラー: ${error.message}`);
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <div className="signature-pad-container">
      <div className="signature-header">
        <h3>電子サイン</h3>
        <p className="client-info">
          利用者: <strong>{clientName}</strong>（ID: {clientId}）
        </p>
      </div>

      <div className="signature-canvas-wrapper">
        <SignatureCanvas
          ref={sigCanvas}
          canvasProps={{
            className: 'signature-canvas',
          }}
        />
      </div>

      <div className="signature-instructions">
        <p>📝 保護者の方は、上記のキャンバスに指またはペンで署名してください。</p>
      </div>

      <div className="signature-buttons">
        <button
          onClick={clearSignature}
          className="btn btn-secondary"
          disabled={isSaving}
        >
          クリア
        </button>
        <button
          onClick={saveSignature}
          className="btn btn-primary"
          disabled={isSaving}
        >
          {isSaving ? '保存中...' : '署名を保存'}
        </button>
      </div>

      {message && (
        <div className={`signature-message ${message.startsWith('✅') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}
    </div>
  );
};

export default SignaturePad;
