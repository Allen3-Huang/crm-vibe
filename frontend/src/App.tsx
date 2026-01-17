import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import CustomerDetail from './pages/CustomerDetail';
import Events from './pages/Events';
import Courses from './pages/Courses';
import Analytics from './pages/Analytics';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <nav className="sidebar">
          <div className="logo">CRM</div>
          <NavLink to="/" end>儀表板</NavLink>
          <NavLink to="/customers">顧客</NavLink>
          <NavLink to="/events">活動</NavLink>
          <NavLink to="/courses">課程</NavLink>
          <NavLink to="/analytics">分析</NavLink>
        </nav>
        <main className="content">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/customers" element={<Customers />} />
            <Route path="/customers/:email" element={<CustomerDetail />} />
            <Route path="/events" element={<Events />} />
            <Route path="/courses" element={<Courses />} />
            <Route path="/analytics" element={<Analytics />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
