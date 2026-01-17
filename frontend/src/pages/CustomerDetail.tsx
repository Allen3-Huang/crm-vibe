import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { api } from '../services/api';
import type { Customer } from '../types';

export default function CustomerDetail() {
  const { email } = useParams<{ email: string }>();
  const [customer, setCustomer] = useState<Customer | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!email) return;
    api.getCustomer(email)
      .then(setCustomer)
      .catch(() => setError('找不到此顧客'))
      .finally(() => setLoading(false));
  }, [email]);

  if (loading) return <div className="loading">載入中...</div>;
  if (error) return <div className="error">{error}</div>;
  if (!customer) return <div className="error">無資料</div>;

  return (
    <div className="customer-detail">
      <Link to="/customers" className="back-link">← 返回列表</Link>

      <h1>{customer.name}</h1>
      <p className="email">{customer.email}</p>

      <div className="detail-grid">
        <section className="events-section">
          <h2>參加活動 ({customer.event_count})</h2>
          {customer.events.length === 0 ? (
            <p className="empty">尚未參加任何活動</p>
          ) : (
            <ul className="detail-list">
              {customer.events.map((event, idx) => (
                <li key={idx}>
                  <strong>{event.event_name}</strong>
                  <span className="date">{event.date}</span>
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="courses-section">
          <h2>購買課程 ({customer.course_count})</h2>
          {customer.courses.length === 0 ? (
            <p className="empty">尚未購買任何課程</p>
          ) : (
            <ul className="detail-list">
              {customer.courses.map((course, idx) => (
                <li key={idx}>
                  <strong>{course.course_name}</strong>
                  <span className="date">{course.date}</span>
                </li>
              ))}
            </ul>
          )}
        </section>
      </div>
    </div>
  );
}
