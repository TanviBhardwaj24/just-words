import React, { useEffect } from 'react';
import { Card, Table, Tag, List, Typography } from 'antd';
import { UserWithRecommendations, Recommendation } from '../types';
import './Dashboard.scss';

const { Title, Text } = Typography;

interface DashboardProps {
  usersWithRecommendations: UserWithRecommendations[];
  loading: boolean;
  onUserSelect: (user: UserWithRecommendations) => void;
}

const Dashboard: React.FC<DashboardProps> = ({
  usersWithRecommendations,
  loading,
  onUserSelect,
}) => {
  useEffect(() => {
    console.log('usersWithRecommendations:', usersWithRecommendations);
  }, [usersWithRecommendations]);

  // Define professional and social categories
  const professionalInterests = [
    'technology',
    'finance',
    'startups',
    'business',
    'coding',
    'engineering',
  ];
  const socialFunInterests = [
    'yoga',
    'hiking',
    'surfing',
    'photography',
    'cooking',
    'dancing',
    'running',
  ];

  // Function to determine the interest category
  const getInterestColor = (interest: string) => {
    if (professionalInterests.includes(interest.toLowerCase())) {
      return 'magenta'; // Professional
    } else if (socialFunInterests.includes(interest.toLowerCase())) {
      return 'green'; // Social/Fun
    }
    return 'blue'; // Default color
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      render: (name: string) => <Text strong>{name}</Text>,
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
      render: (age: number) => <Text>{age} years</Text>,
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
      render: (location: string) => <Tag color="purple">{location}</Tag>,
    },
    {
      title: 'Interests',
      dataIndex: 'interests',
      key: 'interests',
      render: (interests: string[]) => (
        <>
          {interests?.map((interest) => (
            <Tag color={getInterestColor(interest)} key={interest}>
              {interest}
            </Tag>
          )) || 'No interests'}
        </>
      ),
    },
    {
      title: 'Recommendations',
      dataIndex: 'recommendations',
      key: 'recommendations',
      render: (recommendations: Recommendation[]) => (
        <List
          size="small"
          dataSource={recommendations || []}
          renderItem={(item) => (
            <List.Item>
              <Text strong>{item.title}</Text>: {item.description}
            </List.Item>
          )}
        />
      ),
    },
  ];

  return (
    <>
      {/* Move the welcome section outside the card as the main header */}
      <div className="welcome-section">
        <Title level={2} className="welcome-title">
          Welcome to the User Dashboard
        </Title>
        <Text className="welcome-text">
          Manage your users and their recommendations with ease.
        </Text>
      </div>

      <Card className="dashboard-card">
        <Table
          dataSource={usersWithRecommendations}
          columns={columns}
          rowKey={(record) => record.id.toString()}
          loading={loading}
          onRow={(record) => ({
            onClick: () => onUserSelect(record),
          })}
          pagination={{ pageSize: 5 }}
          bordered
          rowClassName="table-row"
        />
      </Card>
    </>
  );
};

export default Dashboard;
