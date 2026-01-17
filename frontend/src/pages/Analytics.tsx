import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { Analytics as AnalyticsType } from '../types';

export default function Analytics() {
  const [analytics, setAnalytics] = useState<AnalyticsType | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getAnalytics()
      .then(setAnalytics)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">載入中...</div>;
  if (!analytics) return <div className="error">無法載入資料</div>;

  return (
    <div className="analytics-page">
      <h1>活動與課程關聯性分析</h1>

      <section className="summary-section">
        <h2>整體轉換統計</h2>
        <div className="stats-grid">
          <div className="stat-card">
            <h3>活動參加者</h3>
            <p className="stat-number">{analytics.conversion_stats.total_event_attendees}</p>
          </div>
          <div className="stat-card">
            <h3>課程購買者</h3>
            <p className="stat-number">{analytics.conversion_stats.total_course_buyers}</p>
          </div>
          <div className="stat-card">
            <h3>已轉換顧客</h3>
            <p className="stat-number">{analytics.conversion_stats.converted_customers}</p>
          </div>
          <div className="stat-card highlight">
            <h3>轉換率</h3>
            <p className="stat-number">{analytics.conversion_stats.conversion_rate}%</p>
          </div>
        </div>
      </section>

      <section className="correlations-section">
        <h2>各活動轉換分析</h2>
        <p className="description">
          分析每個活動的參加者有多少人後續購買了課程，以及他們購買了哪些課程。
        </p>

        <table className="data-table">
          <thead>
            <tr>
              <th>活動名稱</th>
              <th>參加人數</th>
              <th>轉換人數</th>
              <th>轉換率</th>
              <th>熱門購買課程</th>
            </tr>
          </thead>
          <tbody>
            {analytics.event_correlations.map((corr) => (
              <tr key={corr.event_id}>
                <td>
                  <strong>{corr.event_name}</strong>
                  <br />
                  <span className="event-id">{corr.event_id}</span>
                </td>
                <td>{corr.event_attendees}</td>
                <td>{corr.converted_to_course}</td>
                <td className={corr.conversion_rate > 0 ? 'positive' : ''}>
                  {corr.conversion_rate}%
                </td>
                <td>
                  {corr.top_courses.length === 0 ? (
                    <span className="empty">-</span>
                  ) : (
                    <ul className="course-list">
                      {corr.top_courses.map((c, idx) => (
                        <li key={idx}>
                          {c.course_name} ({c.count})
                        </li>
                      ))}
                    </ul>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </div>
  );
}
