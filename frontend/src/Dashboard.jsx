import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import SignaturePad from './SignaturePad';
import DashboardSettings from './DashboardSettings';
import HelpTooltip from './HelpTooltip';
// 実際の API 通信ロジックを実装します

const API_URL = 'http://localhost:8000/api/dashboard/fte/';

// --- 異常値アラート表示コンポーネント ---
const AlertCard = ({ title, message, isWarning }) => (
  <div style={{
    padding: '15px',
    borderRadius: '8px',
    margin: '10px',
    boxShadow: '0 4px 8px rgba(0,0,0,0.1)',
    // 警告レベルに応じて色を変える
    backgroundColor: isWarning ? '#FEF2F2' : '#F0FFF4', // Tailwind-like colors
    border: `1px solid ${isWarning ? '#F87171' : '#34D399'}`, // Tailwind-like colors
    width: '30%',
    minWidth: '280px',
    flex: '1 1 280px',
  }}>
    <h3 style={{ color: isWarning ? 'darkred' : 'darkgreen' }}>{title}</h3>
    <p>{message}</p>
  </div>
);

// --- メインダッシュボードコンポーネント ---
const Dashboard = () => {
  const [fteStatus, setFteStatus] = useState([]);
  const [clients, setClients] = useState([]);
  const [analysisResults, setAnalysisResults] = useState([]);
  const [churnPredictions, setChurnPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [roleSettings, setRoleSettings] = useState({
    showFTE: true,
    showCSVExport: true,
    showPDF: true,
    showAIAnalysis: true,
    showChurnPrediction: true,
    showSignature: true,
    showFinancialForecast: true,
  });

  useEffect(() => {
    // 経営ダッシュボードAPIからデータを取得する
    const fetchFTEData = async () => {
      try {
        // Django APIはポート0000で稼働
        const response = await axios.get(API_URL);
        setFteStatus(response.data);
      } catch (error) {
        console.error("APIデータの取得に失敗しました:", error);
        // エラー発生時は空のデータで続行
        setFteStatus([]);
      } finally {
        setLoading(false);
      }
    };
    
    // 利用者一覧を取得する
    const fetchClients = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/clients/');
        setClients(response.data);
      } catch (error) {
        console.error("利用者データの取得に失敗しました:", error);
        setClients([]);
      }
    };
    
    // AI分析結果を取得する
    const fetchAnalysisResults = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/analysis_results/');
        setAnalysisResults(response.data);
      } catch (error) {
        console.error("AI分析結果の取得に失敗しました:", error);
        setAnalysisResults([]);
      }
    };
    
    // 離脱リスク予測を取得する
    const fetchChurnPredictions = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/churn_prediction/');
        setChurnPredictions(response.data);
      } catch (error) {
        console.error("離脱リスク予測の取得に失敗しました:", error);
        setChurnPredictions({ predictions: [] });
      }
    };

    fetchFTEData();
    fetchClients();
    fetchAnalysisResults();
    fetchChurnPredictions();
  }, []);

  if (loading) {
    return <div>データをロード中...</div>;
  }
  
  // --- グラフコンポーネント ---
const FTEChart = ({ data }) => {
  // グラフ表示用にデータを整形
  const chartData = data.map(item => ({
    name: item.location_name,
    '専門職FTE': item.specialist_fte,
    '目標FTE': item.required_fte_for_kasan,
  }));

  return (
    <div style={{ width: '100%', height: 300 }}>
      <ResponsiveContainer width="100%" height="100%">
        <BarChart
          data={chartData}
          margin={{
            top: 5,
            right: 30,
            left: 20,
            bottom: 5,
          }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis domain={[0, 'auto']} />
          <Tooltip />
          <Legend />
          <Bar dataKey="専門職FTE" fill="#8884d8" />
          <Bar dataKey="目標FTE" fill="#82ca9d" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

// --- アラート表示ロジック ---
  const kasanAlerts = fteStatus
    .filter(status => !status.is_kasan_sufficient)
    .map(status => ({
      title: `🚨 加算充足率警告: ${status.location_name}`,
      message: `専門職 FTE が目標 ${status.required_fte_for_kasan} に対し ${status.specialist_fte} で、${(status.required_fte_for_kasan - status.specialist_fte).toFixed(2)} 人分不足しています。`,
      isWarning: true,
    }));

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1 style={{ borderBottom: '2px solid #333', paddingBottom: '10px' }}>🟥 管理者ダッシュボード</h1>
      
      {/* 役職別ダッシュボード設定 */}
      <DashboardSettings onRoleChange={setRoleSettings} />
      
      {/* 異常値アラートエリア (レイヤー 1: 最優先) */}
      <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        {kasanAlerts.length > 0 ? (
          kasanAlerts.map((alert, index) => <AlertCard key={index} {...alert} />)
        ) : (
          <AlertCard 
            title="✅ 加算充足率" 
            message="全事業所で加算基準を満たしています。現状維持。" 
            isWarning={false} 
          />
        )}
        
        {/* 兼務専従リスクカード (モックデータ) */}
        <AlertCard 
          title="⚠️ 兼務専従違反リスク" 
          message="過去 7 日間で 3 件の登録試行をブロック。要確認。" 
          isWarning={true} 
        />
        
        {/* 利用者離脱リスクカード (モックデータ) */}
        <AlertCard 
          title="📉 利用者離脱リスク" 
          message="今月、サービス利用が不安定な利用者が 2 名います。早期の面談が必要です。" 
          isWarning={true} 
        />
      </div>

      {/* CSV出力ボタンエリア */}
      {roleSettings.showCSVExport && (
      <>
      <h2 style={{ borderBottom: '1px solid #ccc', paddingBottom: '5px', marginTop: '20px' }}>
        💾 CSV出力
        <HelpTooltip
          title="CSV出力機能"
          content="国保連請求、給与計算、会計データをCSV形式で出力できます。外部システムとの連携に便利です。"
        />
      </h2>
      <div style={{ marginTop: '20px', marginBottom: '20px', display: 'flex', gap: '15px', flexWrap: 'wrap' }}>
        {/* 国保連CSV出力ボタン */}
        <button
          onClick={() => {
            window.location.href = 'http://localhost:8000/api/export/kokuhoren_csv/';
          }}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            fontWeight: 'bold',
            color: 'white',
            backgroundColor: '#2563EB',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#1D4ED8'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#2563EB'}
        >
          📥 国保連CSV出力
        </button>
        
        {/* 給与CSV出力ボタン */}
        <button
          onClick={() => {
            window.location.href = 'http://localhost:8000/api/export/payroll_csv/';
          }}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            fontWeight: 'bold',
            color: 'white',
            backgroundColor: '#059669',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#047857'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#059669'}
        >
          💵 給与CSV出力
        </button>
        
        {/* 会計CSV出力ボタン */}
        <button
          onClick={() => {
            window.location.href = 'http://localhost:8000/api/export/accounting_csv/';
          }}
          style={{
            padding: '12px 24px',
            fontSize: '16px',
            fontWeight: 'bold',
            color: 'white',
            backgroundColor: '#DC2626',
            border: 'none',
            borderRadius: '8px',
            cursor: 'pointer',
            boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
          }}
          onMouseOver={(e) => e.target.style.backgroundColor = '#B91C1C'}
          onMouseOut={(e) => e.target.style.backgroundColor = '#DC2626'}
        >
          📊 会計CSV出力
        </button>
      </div>
      </>
      )}

      {roleSettings.showFTE && (
      <>
      <h2 style={{ borderBottom: '1px solid #ccc', paddingBottom: '5px', marginTop: '20px' }}>
        📊 専門職FTEと目標FTEの比較
        <HelpTooltip
          title="FTE（常勤換算）機能"
          content="職員の勤務時間を常勤換算し、加算要件を満たしているかを自動判定します。専門職の配置が不足している場合は警告が表示されます。"
        />
      </h2>
      {/* FTE グラフのコンポーネント */}
      <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px 0' }}>
        {fteStatus.length > 0 ? (
          <FTEChart data={fteStatus} />
        ) : (
          <p>表示するFTEデータがありません。</p>
        )}
      </div>
      </>
      )}
      
      {/* 個別支援計画書PDF出力セクション */}
      {roleSettings.showPDF && (
      <>
      <h2 style={{ borderBottom: '1px solid #ccc', paddingBottom: '5px', marginTop: '30px' }}>
        📝 個別支援計画書PDF出力
        <HelpTooltip
          title="個別支援計画書PDF出力"
          content="利用者ごとの個別支援計画書をPDF形式で出力できます。指導監査や保護者への提供に使用できます。"
        />
      </h2>
      <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px 0' }}>
        {clients.length > 0 ? (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f3f4f6' }}>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>利用者コード</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>氏名</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>生年月日</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>受給者番号</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>アクション</th>
              </tr>
            </thead>
            <tbody>
              {clients.map((client) => (
                <tr key={client.id}>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>{client.client_code}</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>{client.full_name}</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>{client.birth_date}</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd' }}>{client.recipient_number}</td>
                  <td style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>
                    <button
                      onClick={() => {
                        window.location.href = `http://localhost:8000/api/export/support_plan_pdf/${client.id}/`;
                      }}
                      style={{
                        padding: '8px 16px',
                        fontSize: '14px',
                        fontWeight: 'bold',
                        color: 'white',
                        backgroundColor: '#7C3AED',
                        border: 'none',
                        borderRadius: '6px',
                        cursor: 'pointer',
                        boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
                      }}
                      onMouseOver={(e) => e.target.style.backgroundColor = '#6D28D9'}
                      onMouseOut={(e) => e.target.style.backgroundColor = '#7C3AED'}
                    >
                      📝 PDF出力
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p>表示する利用者データがありません。</p>
        )}
      </div>
      </>
      )}
      
      {/* AI分析結果表示セクション */}
      {roleSettings.showAIAnalysis && (
      <>
      <h2 style={{ borderBottom: '1px solid #ccc', paddingBottom: '5px', marginTop: '30px' }}>
        🤖 AI記録品質分析結果
        <HelpTooltip
          title="AI記録品質分析"
          content="AIが進捗記録の品質を分析し、感情スコアや改善提案を提供します。記録の質を向上させ、利用者理解を深めることができます。"
        />
      </h2>
      <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px 0' }}>
        {analysisResults.length > 0 ? (
          <table style={{ width: '100%', borderCollapse: 'collapse' }}>
            <thead>
              <tr style={{ backgroundColor: '#f3f4f6' }}>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>利用者</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>評価日</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>成長スコア</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>感情スコア</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>記録の質</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>キーワード</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>AI改善提案</th>
                <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>担当職員</th>
              </tr>
            </thead>
            <tbody>
              {analysisResults.map((result) => {
                // 記録の質スコアに応じて色を変える
                let qualityColor = '#10B981'; // 緑（高品質）
                if (result.record_quality_score <= 2) {
                  qualityColor = '#EF4444'; // 赤（低品質）
                } else if (result.record_quality_score <= 3) {
                  qualityColor = '#F59E0B'; // 黄（中品質）
                }
                
                return (
                  <tr key={result.id}>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                      {result.client_name}<br/>
                      <small style={{ color: '#666' }}>({result.client_code})</small>
                    </td>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>{result.assessment_date}</td>
                    <td style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>
                      <strong>{result.progress_score.toFixed(1)}</strong> / 5.0
                    </td>
                    <td style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>
                      <span style={{ 
                        padding: '4px 8px', 
                        borderRadius: '4px', 
                        backgroundColor: result.sentiment_score >= 0.5 ? '#D1FAE5' : '#FEE2E2',
                        color: result.sentiment_score >= 0.5 ? '#065F46' : '#991B1B'
                      }}>
                        {result.sentiment_score >= 0 ? '+' : ''}{result.sentiment_score.toFixed(1)}
                      </span>
                    </td>
                    <td style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>
                      <span style={{ 
                        padding: '4px 8px', 
                        borderRadius: '4px', 
                        backgroundColor: qualityColor,
                        color: 'white',
                        fontWeight: 'bold'
                      }}>
                        {result.record_quality_score} / 5
                      </span>
                    </td>
                    <td style={{ padding: '10px', border: '1px solid #ddd', fontSize: '12px' }}>{result.keywords}</td>
                    <td style={{ padding: '10px', border: '1px solid #ddd', fontSize: '12px' }}>{result.feedback}</td>
                    <td style={{ padding: '10px', border: '1px solid #ddd' }}>{result.staff_name}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        ) : (
          <p>AI分析結果がありません。進捗記録を入力し、AI分析を実行してください。</p>
        )}
      </div>
      </>
      )}
      
      {/* 離脱リスク予測アラートセクション */}
      {roleSettings.showChurnPrediction && (
      <>
      <h2 style={{ borderBottom: '1px solid #ccc', paddingBottom: '5px', marginTop: '30px' }}>
        🚨 利用者離脱リスク予測
        <HelpTooltip
          title="離脱リスク予測"
          content="AIが利用者の成長スコア、記録頻度、感情スコアなどを分析し、離脱リスクを予測します。早期に対応することで、利用者の定着率を向上させることができます。"
        />
      </h2>
      <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px 0' }}>
        {churnPredictions.predictions && churnPredictions.predictions.length > 0 ? (
          <>
            {/* サマリー情報 */}
            <div style={{ marginBottom: '20px', padding: '15px', backgroundColor: '#f9fafb', borderRadius: '8px' }}>
              <h3 style={{ marginTop: 0 }}>📊 リスクサマリー</h3>
              <div style={{ display: 'flex', gap: '20px', flexWrap: 'wrap' }}>
                <div style={{ flex: '1', minWidth: '150px' }}>
                  <div style={{ fontSize: '14px', color: '#666' }}>総利用者数</div>
                  <div style={{ fontSize: '24px', fontWeight: 'bold' }}>{churnPredictions.total_clients}名</div>
                </div>
                <div style={{ flex: '1', minWidth: '150px' }}>
                  <div style={{ fontSize: '14px', color: '#666' }}>🔴 高リスク</div>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#EF4444' }}>{churnPredictions.high_risk_count}名</div>
                </div>
                <div style={{ flex: '1', minWidth: '150px' }}>
                  <div style={{ fontSize: '14px', color: '#666' }}>🟠 中リスク</div>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#F59E0B' }}>{churnPredictions.medium_risk_count}名</div>
                </div>
                <div style={{ flex: '1', minWidth: '150px' }}>
                  <div style={{ fontSize: '14px', color: '#666' }}>🟢 低リスク</div>
                  <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#10B981' }}>{churnPredictions.low_risk_count}名</div>
                </div>
              </div>
            </div>
            
            {/* リスク予測テーブル */}
            <table style={{ width: '100%', borderCollapse: 'collapse' }}>
              <thead>
                <tr style={{ backgroundColor: '#f3f4f6' }}>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>利用者</th>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>離脱リスク</th>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>レベル</th>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>アラート</th>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'left' }}>推奨アクション</th>
                  <th style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>詳細指標</th>
                </tr>
              </thead>
              <tbody>
                {churnPredictions.predictions.map((prediction) => {
                  // リスクレベルに応じて背景色を変える
                  let rowBgColor = '#ffffff';
                  if (prediction.risk_level === '高') {
                    rowBgColor = '#FEE2E2'; // 赤系
                  } else if (prediction.risk_level === '中') {
                    rowBgColor = '#FEF3C7'; // 黄系
                  }
                  
                  return (
                    <tr key={prediction.client_id} style={{ backgroundColor: rowBgColor }}>
                      <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                        <strong>{prediction.client_name}</strong><br/>
                        <small style={{ color: '#666' }}>({prediction.client_code})</small>
                      </td>
                      <td style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>
                        <div style={{ fontSize: '24px', fontWeight: 'bold' }}>
                          {prediction.churn_risk_score}%
                        </div>
                      </td>
                      <td style={{ padding: '10px', border: '1px solid #ddd', textAlign: 'center' }}>
                        <span style={{
                          padding: '6px 12px',
                          borderRadius: '6px',
                          fontWeight: 'bold',
                          backgroundColor: prediction.risk_color === 'red' ? '#EF4444' : (prediction.risk_color === 'orange' ? '#F59E0B' : '#10B981'),
                          color: 'white'
                        }}>
                          {prediction.risk_level}
                        </span>
                      </td>
                      <td style={{ padding: '10px', border: '1px solid #ddd' }}>
                        {prediction.alert_message}
                      </td>
                      <td style={{ padding: '10px', border: '1px solid #ddd', fontSize: '12px' }}>
                        {prediction.recommended_actions.length > 0 ? (
                          <ul style={{ margin: 0, paddingLeft: '20px' }}>
                            {prediction.recommended_actions.map((action, idx) => (
                              <li key={idx}>{action}</li>
                            ))}
                          </ul>
                        ) : (
                          <span>特になし</span>
                        )}
                      </td>
                      <td style={{ padding: '10px', border: '1px solid #ddd', fontSize: '11px' }}>
                        <div>成長: {prediction.metrics.avg_progress_score} ({prediction.metrics.progress_change_rate >= 0 ? '+' : ''}{prediction.metrics.progress_change_rate}%)</div>
                        <div>記録: {prediction.metrics.record_count}回 ({prediction.metrics.record_frequency_rate}%)</div>
                        <div>感情: {prediction.metrics.avg_sentiment_score} ({prediction.metrics.sentiment_change_rate >= 0 ? '+' : ''}{prediction.metrics.sentiment_change_rate}%)</div>
                        <div>品質: {prediction.metrics.avg_quality_score} ({prediction.metrics.quality_change_rate >= 0 ? '+' : ''}{prediction.metrics.quality_change_rate}%)</div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </>
        ) : (
          <p>離脱リスク予測データがありません。進捗記録を入力してください。</p>
        )}
      </div>
      </>
      )}
      
      {/* 電子サインセクション */}
      {roleSettings.showSignature && (
      <>
      <h2 style={{ borderBottom: '1px solid #ccc', paddingBottom: '5px', marginTop: '30px' }}>
        ✍️ 電子サイン（個別支援計画書用）
        <HelpTooltip
          title="電子サイン機能"
          content="タブレットで保護者の署名を取得し、デジタル保存できます。ペーパーレス化を実現し、管理が簡単になります。"
        />
      </h2>
      <div style={{ border: '1px solid #ccc', padding: '15px', margin: '10px 0' }}>
        <p style={{ marginBottom: '20px', color: '#555' }}>
          以下から利用者を選択し、保護者の電子サインを取得してください。
        </p>
        {clients.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
            {clients.map((client) => (
              <div key={client.id} style={{
                border: '1px solid #e5e7eb',
                borderRadius: '8px',
                padding: '20px',
                backgroundColor: '#f9fafb'
              }}>
                <SignaturePad
                  clientId={client.id}
                  clientName={client.full_name}
                  onSignatureSaved={(data) => {
                    console.log('署名が保存されました:', data);
                  }}
                />
              </div>
            ))}
          </div>
        ) : (
          <p>表示する利用者データがありません。</p>
        )}
      </div>
      </>
      )}
      
    </div>
  );
};

export default Dashboard;
