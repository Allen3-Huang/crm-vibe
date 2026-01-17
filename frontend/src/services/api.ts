import type { CustomerSummary, Customer, Event, Course, Analytics } from '../types';
import { getStoredToken } from '../contexts/AuthContext';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api';

async function fetchJson<T>(url: string): Promise<T> {
  const token = getStoredToken();
  const headers: Record<string, string> = {};

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const response = await fetch(url, { headers });

  if (response.status === 401) {
    // Token 過期或無效，清除本地存儲並跳轉到登入頁
    localStorage.removeItem('crm_auth_token');
    localStorage.removeItem('crm_auth_user');
    window.location.href = '/login';
    throw new Error('Unauthorized');
  }

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json();
}

export const api = {
  getCustomers: () => fetchJson<CustomerSummary[]>(`${API_BASE}/customers`),
  getCustomer: (email: string) => fetchJson<Customer>(`${API_BASE}/customers/${encodeURIComponent(email)}`),
  getEvents: () => fetchJson<Event[]>(`${API_BASE}/events`),
  getCourses: () => fetchJson<Course[]>(`${API_BASE}/courses`),
  getAnalytics: () => fetchJson<Analytics>(`${API_BASE}/analytics`),
};
