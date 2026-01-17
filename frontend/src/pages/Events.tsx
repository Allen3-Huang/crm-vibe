import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { Event } from '../types';

export default function Events() {
  const [events, setEvents] = useState<Event[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    api.getEvents()
      .then(setEvents)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">載入中...</div>;

  return (
    <div className="events-page">
      <h1>活動列表</h1>
      <p className="result-count">共 {events.length} 個活動</p>

      <div className="events-list">
        {events.map((event) => (
          <div key={event.event_id} className="event-card">
            <div
              className="event-header"
              onClick={() => setExpanded(expanded === event.event_id ? null : event.event_id)}
            >
              <div>
                <h3>{event.event_name}</h3>
                <span className="event-id">{event.event_id}</span>
              </div>
              <span className="attendee-count">{event.attendee_count} 人參加</span>
            </div>

            {expanded === event.event_id && (
              <div className="attendees-list">
                <h4>參加者名單</h4>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>姓名</th>
                      <th>Email</th>
                      <th>日期</th>
                    </tr>
                  </thead>
                  <tbody>
                    {event.attendees.map((a, idx) => (
                      <tr key={idx}>
                        <td>{a.name}</td>
                        <td>{a.email}</td>
                        <td>{a.date}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
