import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Layout, Typography, message } from 'antd';
import { UserWithRecommendations } from './types';
import Dashboard from './Dashboard/Dashboard';
import UserDetails from './UserDetails/UserDetails';

const { Header, Content } = Layout;
const { Title } = Typography;

const App: React.FC = () => {
  const [usersWithRecommendations, setUsersWithRecommendations] = useState<
    UserWithRecommendations[]
  >([]);
  const [loading, setLoading] = useState(false);
  const [selectedUser, setSelectedUser] =
    useState<UserWithRecommendations | null>(null);

  useEffect(() => {
    fetchAllUsersRecommendations();
  }, []);

  const fetchAllUsersRecommendations = async () => {
    setLoading(true);
    try {
      const response = await axios.get<UserWithRecommendations[]>(
        'http://localhost:8000/api/all-users-recommendations'
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

  const handleUserSelect = (user: UserWithRecommendations) => {
    console.log('Selected user:', user);
    setSelectedUser(user);
  };

  const handleBackToDashboard = () => {
    setSelectedUser(null);
  };

  return (
    <Layout className="layout" style={{ minHeight: '100vh' }}>
      <Header style={{ display: 'flex', alignItems: 'center' }}>
        <Title level={3} style={{ color: 'white', margin: 0 }}>
          Just Friends Email Marketing Dashboard
        </Title>
      </Header>

      <Content style={{ padding: '24px' }}>
        {selectedUser ? (
          <UserDetails
            userWithRecommendations={selectedUser}
            onBack={handleBackToDashboard}
          />
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
