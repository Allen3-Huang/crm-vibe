import { BrowserRouter, Routes, Route, NavLink, Navigate, useLocation } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import Dashboard from './pages/Dashboard';
import Customers from './pages/Customers';
import CustomerDetail from './pages/CustomerDetail';
import Events from './pages/Events';
import Courses from './pages/Courses';
import Analytics from './pages/Analytics';
import Login from './pages/Login';
import './App.css';

function ProtectedRoute({ children, allowedEmail }: { children: React.ReactNode; allowedEmail?: string }) {
  const { user, isLoading } = useAuth();
  const location = useLocation();

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  if (!user) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  if (allowedEmail && user.email !== allowedEmail) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}

function AppContent() {
  const { user, logout, isLoading } = useAuth();
  const location = useLocation();

  // 登入頁面不顯示側邊欄
  if (location.pathname === '/login') {
    return (
      <Routes>
        <Route path="/login" element={<Login />} />
      </Routes>
    );
  }

  if (isLoading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <div className="app">
      <nav className="sidebar">
        <div className="logo">CRM</div>
        <NavLink to="/" end>儀表板</NavLink>
        {user?.email === 'a126b2003@gmail.com' && (
          <NavLink to="/customers">顧客</NavLink>
        )}
        <NavLink to="/events">活動</NavLink>
        <NavLink to="/courses">課程</NavLink>
        <NavLink to="/analytics">分析</NavLink>

        {user && (
          <div className="user-section">
            <div className="user-info">
              {user.picture && (
                <img src={user.picture} alt={user.name} className="user-avatar" />
              )}
              <span className="user-name">{user.name}</span>
            </div>
            <button onClick={logout} className="logout-button">
              登出
            </button>
          </div>
        )}
      </nav>
      <main className="content">
        <Routes>
          <Route path="/" element={<ProtectedRoute><Dashboard /></ProtectedRoute>} />
          <Route path="/customers" element={<ProtectedRoute allowedEmail="a126b2003@gmail.com"><Customers /></ProtectedRoute>} />
          <Route path="/customers/:email" element={<ProtectedRoute allowedEmail="a126b2003@gmail.com"><CustomerDetail /></ProtectedRoute>} />
          <Route path="/events" element={<ProtectedRoute><Events /></ProtectedRoute>} />
          <Route path="/courses" element={<ProtectedRoute><Courses /></ProtectedRoute>} />
          <Route path="/analytics" element={<ProtectedRoute><Analytics /></ProtectedRoute>} />
          <Route path="/login" element={<Login />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;
