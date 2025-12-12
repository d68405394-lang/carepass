import React, { useState, useEffect } from 'react';

const DashboardSettings = ({ onRoleChange }) => {
  const [selectedRole, setSelectedRole] = useState('admin');

  // 役職の定義
  const roles = [
    { id: 'admin', name: '管理者', icon: '👑' },
    { id: 'manager', name: 'サービス管理責任者', icon: '📋' },
    { id: 'staff', name: '現場職員', icon: '👨‍⚕️' },
    { id: 'accountant', name: '経理担当', icon: '💰' },
  ];

  // 役職ごとの表示項目設定
  const roleSettings = {
    admin: {
      showFTE: true,
      showCSVExport: true,
      showPDF: true,
      showAIAnalysis: true,
      showChurnPrediction: true,
      showSignature: true,
      showFinancialForecast: true,
      priority: ['FTE', 'チャーン予測', '財務予測', 'CSV出力'],
    },
    manager: {
      showFTE: true,
      showCSVExport: false,
      showPDF: true,
      showAIAnalysis: true,
      showChurnPrediction: true,
      showSignature: true,
      showFinancialForecast: false,
      priority: ['チャーン予測', 'AI分析', '個別支援計画書'],
    },
    staff: {
      showFTE: false,
      showCSVExport: false,
      showPDF: true,
      showAIAnalysis: true,
      showChurnPrediction: false,
      showSignature: true,
      showFinancialForecast: false,
      priority: ['AI分析', '電子サイン', '個別支援計画書'],
    },
    accountant: {
      showFTE: true,
      showCSVExport: true,
      showPDF: false,
      showAIAnalysis: false,
      showChurnPrediction: false,
      showSignature: false,
      showFinancialForecast: true,
      priority: ['CSV出力', '財務予測', 'FTE'],
    },
  };

  useEffect(() => {
    // ローカルストレージから役職設定を読み込む
    const savedRole = localStorage.getItem('userRole');
    if (savedRole && roleSettings[savedRole]) {
      setSelectedRole(savedRole);
      onRoleChange(roleSettings[savedRole]);
    } else {
      onRoleChange(roleSettings['admin']);
    }
  }, []);

  const handleRoleChange = (roleId) => {
    setSelectedRole(roleId);
    localStorage.setItem('userRole', roleId);
    onRoleChange(roleSettings[roleId]);
  };

  return (
    <div style={{
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      padding: '20px',
      borderRadius: '12px',
      marginBottom: '20px',
      boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
    }}>
      <h3 style={{ color: 'white', marginBottom: '15px', fontSize: '18px' }}>
        👤 役職別ダッシュボード
      </h3>
      <p style={{ color: 'rgba(255,255,255,0.9)', fontSize: '14px', marginBottom: '15px' }}>
        あなたの役職に最適化された情報を表示します
      </p>
      <div style={{
        display: 'flex',
        gap: '10px',
        flexWrap: 'wrap',
      }}>
        {roles.map((role) => (
          <button
            key={role.id}
            onClick={() => handleRoleChange(role.id)}
            style={{
              padding: '12px 20px',
              fontSize: '14px',
              fontWeight: selectedRole === role.id ? 'bold' : 'normal',
              color: selectedRole === role.id ? '#667eea' : 'white',
              backgroundColor: selectedRole === role.id ? 'white' : 'rgba(255,255,255,0.2)',
              border: selectedRole === role.id ? '2px solid white' : '2px solid transparent',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              minWidth: '140px',
              minHeight: '44px',
            }}
            onMouseOver={(e) => {
              if (selectedRole !== role.id) {
                e.target.style.backgroundColor = 'rgba(255,255,255,0.3)';
              }
            }}
            onMouseOut={(e) => {
              if (selectedRole !== role.id) {
                e.target.style.backgroundColor = 'rgba(255,255,255,0.2)';
              }
            }}
          >
            {role.icon} {role.name}
          </button>
        ))}
      </div>
      
      {/* 優先表示項目の案内 */}
      <div style={{
        marginTop: '15px',
        padding: '12px',
        background: 'rgba(255,255,255,0.15)',
        borderRadius: '8px',
      }}>
        <p style={{ color: 'white', fontSize: '13px', margin: 0 }}>
          📌 優先表示: {roleSettings[selectedRole].priority.join(' → ')}
        </p>
      </div>
    </div>
  );
};

export default DashboardSettings;
