import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { api } from '../services/api';
import type { CustomerSummary } from '../types';

export default function Customers() {
  const [customers, setCustomers] = useState<CustomerSummary[]>([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    api.getCustomers()
      .then(setCustomers)
      .finally(() => setLoading(false));
  }, []);

  const filtered = customers.filter(c =>
    c.name.includes(search) || c.email.includes(search)
  );

  if (loading) return <div className="loading">載入中...</div>;

  return (
    <div className="customers-page">
      <h1>顧客列表</h1>

      <div className="search-bar">
        <input
          type="text"
          placeholder="搜尋姓名或 Email..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      <p className="result-count">共 {filtered.length} 位顧客</p>

      <table className="data-table">
        <thead>
          <tr>
            <th>姓名</th>
            <th>Email</th>
            <th>參加活動數</th>
            <th>購買課程數</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          {filtered.map((customer) => (
            <tr key={customer.email}>
              <td>{customer.name}</td>
              <td>{customer.email}</td>
              <td>{customer.event_count}</td>
              <td>{customer.course_count}</td>
              <td>
                <Link to={`/customers/${encodeURIComponent(customer.email)}`} className="btn-detail">
                  詳情
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
