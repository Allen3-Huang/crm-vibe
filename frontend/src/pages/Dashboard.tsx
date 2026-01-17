import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import type { Analytics } from '../types';

export default function Dashboard() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getAnalytics()
      .then(setAnalytics)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">載入中...</div>;
  if (!analytics) return <div className="error">無法載入資料</div>;

  return (
    <div className="dashboard">
      <h1>CRM 儀表板</h1>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>總顧客數</h3>
          <p className="stat-number">{analytics.total_customers}</p>
        </div>
        <div className="stat-card">
          <h3>活動數</h3>
          <p className="stat-number">{analytics.total_events}</p>
        </div>
        <div className="stat-card">
          <h3>課程數</h3>
          <p className="stat-number">{analytics.total_courses}</p>
        </div>
        <div className="stat-card highlight">
          <h3>活動轉課程轉換率</h3>
          <p className="stat-number">{analytics.conversion_stats.conversion_rate}%</p>
        </div>
      </div>

      <div className="conversion-details">
        <h2>轉換統計</h2>
        <ul>
          <li>活動參加者: {analytics.conversion_stats.total_event_attendees} 人</li>
          <li>課程購買者: {analytics.conversion_stats.total_course_buyers} 人</li>
          <li>已轉換顧客 (參加活動且購買課程): {analytics.conversion_stats.converted_customers} 人</li>
        </ul>
      </div>

      <div className="quick-links">
        <h2>快速導航</h2>
        <div className="link-grid">
          <Link to="/customers" className="quick-link">顧客列表</Link>
          <Link to="/events" className="quick-link">活動列表</Link>
          <Link to="/courses" className="quick-link">課程列表</Link>
          <Link to="/analytics" className="quick-link">詳細分析</Link>
        </div>
      </div>
    </div>
  );
}
