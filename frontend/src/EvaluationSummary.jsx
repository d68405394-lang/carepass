import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_URL = 'http://localhost:8000/api/evaluation/summary/';

const EvaluationSummary = () => {
  const [summaryData, setSummaryData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const response = await axios.get(API_URL);
        setSummaryData(response.data);
        setLoading(false);
      } catch (err) {
        setError('人事評価サマリーデータの取得に失敗しました。バックエンドAPIが起動しているか確認してください。');
        setLoading(false);
        console.error('API Error:', err);
      }
    };

    fetchSummary();
  }, []);

  if (loading) {
    return <div style={{ padding: '50px', textAlign: 'center' }}>データを読み込み中...</div>;
  }

  if (error) {
    return <div style={{ padding: '50px', textAlign: 'center', color: 'red' }}>エラー: {error}</div>;
  }

  if (summaryData.length === 0) {
    return <div style={{ padding: '50px', textAlign: 'center' }}>評価データがありません。勤務記録と相互評価を登録してください。</div>;
  }

  // グラフデータの整形 (recharts用にキー名を調整)
  const chartData = summaryData.map(item => ({
    name: item.staff_name,
    貢献度: item.contribution_score,
    協調性: item.cooperation_score,
    総合評価: item.overall_score,
  }));

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h1>人事評価サマリー</h1>
      <p>職員の貢献度（FTE寄与）と協調性（相互評価）を統合した総合評価スコアです。</p>

      {/* グラフ表示エリア */}
      <div style={{ width: '100%', height: 400, marginBottom: '40px' }}>
        <h2>総合評価スコア比較</h2>
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            data={chartData}
            margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis domain={[0, 5]} />
            <Tooltip />
            <Legend />
            <Bar dataKey="総合評価" fill="#8884d8" />
            <Bar dataKey="貢献度" fill="#82ca9d" />
            <Bar dataKey="協調性" fill="#ffc658" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* 詳細テーブル表示エリア */}
      <h2>詳細スコア一覧</h2>
      <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }}>
        <thead>
          <tr style={{ borderBottom: '2px solid #333' }}>
            <th style={{ padding: '10px' }}>職員名</th>
            <th style={{ padding: '10px' }}>総合評価スコア (Max 5.0)</th>
            <th style={{ padding: '10px' }}>貢献度スコア (FTE寄与)</th>
            <th style={{ padding: '10px' }}>協調性スコア (相互評価)</th>
          </tr>
        </thead>
        <tbody>
          {summaryData.map((item, index) => (
            <tr key={index} style={{ borderBottom: '1px solid #eee', backgroundColor: index % 2 === 0 ? '#f9f9f9' : 'white' }}>
              <td style={{ padding: '10px', fontWeight: 'bold' }}>{item.staff_name}</td>
              <td style={{ padding: '10px', color: item.overall_score >= 4.0 ? '#4CAF50' : '#FF9800' }}>{item.overall_score}</td>
              <td style={{ padding: '10px' }}>{item.contribution_score}</td>
              <td style={{ padding: '10px' }}>{item.cooperation_score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default EvaluationSummary;
