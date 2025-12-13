import React, { useState, useEffect } from 'react';
import './EmailComposer.css';

function EmailComposer() {
  const [clients, setClients] = useState([]);
  const [selectedClients, setSelectedClients] = useState([]);
  const [subject, setSubject] = useState('');
  const [body, setBody] = useState('');
  const [messageType, setMessageType] = useState('bulk');
  const [sending, setSending] = useState(false);
  const [message, setMessage] = useState('');

  // 利用者一覧を取得
  useEffect(() => {
    fetch('http://localhost:8000/api/clients/')
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          setClients(data.clients);
        }
      })
      .catch(error => console.error('Error fetching clients:', error));
  }, []);

  // 利用者選択のトグル
  const toggleClientSelection = (clientId) => {
    setSelectedClients(prev => {
      if (prev.includes(clientId)) {
        return prev.filter(id => id !== clientId);
      } else {
        return [...prev, clientId];
      }
    });
  };

  // 全選択/全解除
  const toggleSelectAll = () => {
    if (selectedClients.length === clients.length) {
      setSelectedClients([]);
    } else {
      setSelectedClients(clients.map(client => client.id));
    }
  };

  // メール送信
  const handleSendEmail = async () => {
    if (!subject || !body) {
      setMessage('件名と本文を入力してください');
      return;
    }

    if (selectedClients.length === 0) {
      setMessage('送信先を選択してください');
      return;
    }

    setSending(true);
    setMessage('');

    try {
      const response = await fetch('http://localhost:8000/api/email/send/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          subject,
          body,
          message_type: messageType,
          client_ids: selectedClients,
        }),
      });

      const data = await response.json();

      if (data.success) {
        setMessage(`✅ メールを送信しました（${data.sent_count}件）`);
        setSubject('');
        setBody('');
        setSelectedClients([]);
      } else {
        setMessage(`❌ 送信に失敗しました: ${data.error}`);
      }
    } catch (error) {
      setMessage(`❌ エラーが発生しました: ${error.message}`);
    } finally {
      setSending(false);
    }
  };

  return (
    <div className="email-composer">
      <h2>📧 メール送信</h2>

      {message && (
        <div className={`message ${message.includes('✅') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}

      <div className="form-group">
        <label>送信先選択</label>
        <div className="client-selection">
          <button onClick={toggleSelectAll} className="select-all-btn">
            {selectedClients.length === clients.length ? '全解除' : '全選択'}
          </button>
          <div className="client-list">
            {clients.map(client => (
              <label key={client.id} className="client-checkbox">
                <input
                  type="checkbox"
                  checked={selectedClients.includes(client.id)}
                  onChange={() => toggleClientSelection(client.id)}
                />
                <span>{client.name}</span>
                {client.guardian_email && (
                  <span className="email-address">({client.guardian_email})</span>
                )}
              </label>
            ))}
          </div>
          <p className="selected-count">
            選択中: {selectedClients.length}件
          </p>
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="subject">件名</label>
        <input
          type="text"
          id="subject"
          value={subject}
          onChange={(e) => setSubject(e.target.value)}
          placeholder="例: 明日の遠足について"
          maxLength={200}
        />
      </div>

      <div className="form-group">
        <label htmlFor="body">本文</label>
        <textarea
          id="body"
          value={body}
          onChange={(e) => setBody(e.target.value)}
          placeholder="メッセージを入力してください"
          rows={10}
        />
      </div>

      <div className="form-group">
        <label>メッセージタイプ</label>
        <select value={messageType} onChange={(e) => setMessageType(e.target.value)}>
          <option value="bulk">一斉配信</option>
          <option value="individual">個別送信</option>
        </select>
      </div>

      <div className="button-group">
        <button
          onClick={handleSendEmail}
          disabled={sending || !subject || !body || selectedClients.length === 0}
          className="send-btn"
        >
          {sending ? '送信中...' : '📤 送信'}
        </button>
      </div>
    </div>
  );
}

export default EmailComposer;
