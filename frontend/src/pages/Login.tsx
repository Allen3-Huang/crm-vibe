import { useNavigate } from 'react-router-dom';
import { GoogleLogin } from '@react-oauth/google';
import type { CredentialResponse } from '@react-oauth/google';
import { useAuth } from '../contexts/AuthContext';
import { useState } from 'react';

export default function Login() {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [error, setError] = useState<string | null>(null);

  const handleSuccess = async (credentialResponse: CredentialResponse) => {
    try {
      if (!credentialResponse.credential) {
        setError('No credential received from Google');
        return;
      }
      await login(credentialResponse.credential);
      navigate('/');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Login failed');
    }
  };

  const handleError = () => {
    setError('Google login failed');
  };

  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-header">
          <h1>CRM System</h1>
          <p>Please sign in with your Google account</p>
        </div>

        {error && <div className="login-error">{error}</div>}

        <div className="login-button">
          <GoogleLogin
            onSuccess={handleSuccess}
            onError={handleError}
            useOneTap
            theme="outline"
            size="large"
            text="signin_with"
            shape="rectangular"
          />
        </div>
      </div>
    </div>
  );
}
