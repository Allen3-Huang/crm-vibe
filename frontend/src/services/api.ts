import type { CustomerSummary, Customer, Event, Course, Analytics } from '../types';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000/api';

async function fetchJson<T>(url: string): Promise<T> {
  const response = await fetch(url);
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
