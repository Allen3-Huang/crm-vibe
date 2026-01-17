import { useEffect, useState } from 'react';
import { api } from '../services/api';
import type { Course } from '../types';

export default function Courses() {
  const [courses, setCourses] = useState<Course[]>([]);
  const [loading, setLoading] = useState(true);
  const [expanded, setExpanded] = useState<string | null>(null);

  useEffect(() => {
    api.getCourses()
      .then(setCourses)
      .finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="loading">載入中...</div>;

  return (
    <div className="courses-page">
      <h1>課程列表</h1>
      <p className="result-count">共 {courses.length} 個課程</p>

      <div className="courses-list">
        {courses.map((course) => (
          <div key={course.course_id} className="course-card">
            <div
              className="course-header"
              onClick={() => setExpanded(expanded === course.course_id ? null : course.course_id)}
            >
              <div>
                <h3>{course.course_name}</h3>
                <span className="course-id">{course.course_id}</span>
              </div>
              <span className="buyer-count">{course.buyer_count} 人購買</span>
            </div>

            {expanded === course.course_id && (
              <div className="buyers-list">
                <h4>購買者名單</h4>
                <table className="data-table">
                  <thead>
                    <tr>
                      <th>姓名</th>
                      <th>Email</th>
                      <th>日期</th>
                    </tr>
                  </thead>
                  <tbody>
                    {course.buyers.map((b, idx) => (
                      <tr key={idx}>
                        <td>{b.name}</td>
                        <td>{b.email}</td>
                        <td>{b.date}</td>
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
