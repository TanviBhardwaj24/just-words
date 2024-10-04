import React, { useEffect } from 'react';
import { Card, Table, Tag, List, Typography } from 'antd';
import { allUsers, Recommendation } from '../types';
import { FaFacebook, FaInstagram, FaLinkedin, FaGithub } from 'react-icons/fa';
import './Dashboard.scss';

const { Title, Text } = Typography;

interface DashboardProps {
  usersWithRecommendations: allUsers[];
  loading: boolean;
  onUserSelect: (user: allUsers) => void;
}

const Dashboard: React.FC<DashboardProps> = ({
  usersWithRecommendations,
  loading,
  onUserSelect,
}) => {
  useEffect(() => {}, [usersWithRecommendations]);

  const professionalInterests = [
    'technology',
    'finance',
    'startups',
    'business',
    'coding',
    'engineering',
    'acting',
    'tech startups',
  ];

  const socialFunInterests = [
    'yoga',
    'hiking',
    'surfing',
    'photography',
    'cooking',
    'dancing',
    'running',
    'ballet',
    'literature',
    'cycling',
  ];

  const getInterestColor = (interest: string) => {
    if (professionalInterests.includes(interest.toLowerCase())) {
      return 'magenta';
    } else if (socialFunInterests.includes(interest.toLowerCase())) {
      return 'green';
    }
    return 'blue';
  };

  const renderSocialMediaIcons = (record: allUsers) => {
    return (
      <div style={{ display: 'flex', gap: '10px' }}>
        {record.facebook && (
          <a href={record.facebook} target="_blank" rel="noopener noreferrer">
            <FaFacebook size={20} color="#3b5998" />
          </a>
        )}
        {record.instagram && (
          <a href={record.instagram} target="_blank" rel="noopener noreferrer">
            <FaInstagram size={20} color="#E1306C" />
          </a>
        )}
        {record.linkedin && (
          <a href={record.linkedin} target="_blank" rel="noopener noreferrer">
            <FaLinkedin size={20} color="#0e76a8" />
          </a>
        )}
        {record.github && (
          <a href={record.github} target="_blank" rel="noopener noreferrer">
            <FaGithub size={20} color="#333" />
          </a>
        )}
      </div>
    );
  };

  const columns = [
    {
      title: 'Name',
      dataIndex: 'name',
      key: 'name',
      width: '10%',
      render: (name: string) => <Text strong>{name}</Text>,
    },
    {
      title: 'Age',
      dataIndex: 'age',
      key: 'age',
      width: '7%',
      render: (age: number) => <Text>{age} years</Text>,
    },
    {
      title: 'Location',
      dataIndex: 'location',
      key: 'location',
      width: '10%',
      render: (location: string) => <Tag color="purple">{location}</Tag>,
    },
    {
      title: 'Description',
      dataIndex: 'description',
      key: 'description',
      width: '12%',
      render: (description: string) => (
        <Text>{description || 'No description'}</Text>
      ),
    },
    {
      title: 'Interests',
      dataIndex: 'interests',
      key: 'interests',
      width: '20%',
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
      title: 'Social Media',
      dataIndex: '',
      key: 'social_media',
      render: (record: allUsers) => renderSocialMediaIcons(record),
      width: '10%',
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
    {
      title: 'Follows',
      dataIndex: 'follows',
      key: 'follows',
      render: (follows: string[]) => (
        <List
          size="small"
          dataSource={follows || []}
          renderItem={(followedUser) => (
            <List.Item>
              <Text>{followedUser}</Text>
            </List.Item>
          )}
        />
      ),
    },
  ];

  return (
    <>
      <div className="welcome-section">
        <Title level={2} className="welcome-title">
          Welcome to the User Dashboard
        </Title>
        <Text className="welcome-text">
          Manage your users and their recommendations with ease
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
          pagination={{ pageSize: 3 }}
          bordered
          rowClassName="table-row"
          scroll={{ y: 450 }}
        />
      </Card>
    </>
  );
};

export default Dashboard;
