import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Layout, Typography, message } from 'antd';
import { AllUsers } from './types';
import Dashboard from './Dashboard/Dashboard';
import UserDetails from './UserDetails/UserDetails';
import './App.css';

const { Header, Content } = Layout;

const App: React.FC = () => {
  const [usersWithRecommendations, setUsersWithRecommendations] = useState<
    AllUsers[]
  >([]);

  const [loading, setLoading] = useState(false);
  const [selectedUser, setSelectedUser] = useState<AllUsers | null>(null);

  useEffect(() => {
    fetchAllUsersRecommendations();
  }, []);

  const fetchAllUsersRecommendations = async () => {
    setLoading(true);
    try {
      const response = await axios.get<AllUsers[]>(
        'http://localhost:8000/api/all-users'
      );
      console.log('API response:', response.data);
      setUsersWithRecommendations(response.data);
    } catch (error) {
      console.error('Error fetching all users recommendations:', error);
      if (axios.isAxiosError(error)) {
        console.error('Error details:', error.response?.data);
      }
      message.error('Failed to fetch dashboard data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleUserSelect = (user: AllUsers) => {
    console.log('Selected user:', user);
    setSelectedUser(user);
  };

  const handleBackToDashboard = () => {
    setSelectedUser(null);
  };

  return (
    <Layout className="layout" style={{ minHeight: '100vh' }}>
      <Header className="app-header">
        <h3 className="app-title">Just Friends</h3>
        <span className="app-subtitle">email marketing dashboard</span>
      </Header>

      <Content className="app-content">
        {selectedUser ? (
          <UserDetails AllUsers={selectedUser} onBack={handleBackToDashboard} />
        ) : (
          <Dashboard
            usersWithRecommendations={usersWithRecommendations}
            loading={loading}
            onUserSelect={handleUserSelect}
          />
        )}
      </Content>
    </Layout>
  );
};

export default App;
