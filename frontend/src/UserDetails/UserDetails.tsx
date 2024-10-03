import React, { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Card,
  List,
  Typography,
  Divider,
  Row,
  Col,
  message,
  Button,
  Spin,
} from 'antd';
import {
  UserOutlined,
  MailOutlined,
  DashboardOutlined,
  ArrowLeftOutlined,
} from '@ant-design/icons';
import { UserWithRecommendations, EmailContent } from '../types';
import './UserDetails.scss';

const { Text, Paragraph } = Typography;

interface UserDetailsProps {
  userWithRecommendations: UserWithRecommendations | null;
  onBack: () => void;
}

const UserDetails: React.FC<UserDetailsProps> = ({
  userWithRecommendations,
  onBack,
}) => {
  const [emailContent, setEmailContent] = useState<EmailContent | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (userWithRecommendations?.id) {
      fetchEmailContent(userWithRecommendations.id.toString());
    }
  }, [userWithRecommendations]);

  const fetchEmailContent = async (userId: string) => {
    setLoading(true);
    try {
      const emailResponse = await axios.post(
        `http://localhost:8000/api/generate-email/${userId}`
      );
      setEmailContent(emailResponse.data);
    } catch (error) {
      console.error('Error fetching email content:', error);
      message.error('Failed to fetch email content. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (!userWithRecommendations) return null;

  return (
    <>
      <Button
        icon={<ArrowLeftOutlined />}
        onClick={onBack}
        className="back-button"
      >
        Back to Dashboard
      </Button>
      <Row gutter={24}>
        <Col span={12}>
          <Card
            title={
              <span>
                <UserOutlined /> User Profile
              </span>
            }
            className="user-profile-card"
          >
            <Paragraph>
              <Text strong>Name:</Text> {userWithRecommendations.name || 'N/A'}
            </Paragraph>
            <Paragraph>
              <Text strong>Age:</Text> {userWithRecommendations.age || 'N/A'}
            </Paragraph>
            <Paragraph>
              <Text strong>Location:</Text>{' '}
              {userWithRecommendations.location || 'N/A'}
            </Paragraph>
            <Paragraph>
              <Text strong>Interests:</Text>{' '}
              {userWithRecommendations.interests?.join(', ') || 'None'}
            </Paragraph>
          </Card>
          <Card
            title={
              <span>
                <DashboardOutlined /> Recommendations
              </span>
            }
            className="recommendations-card"
          >
            <List
              itemLayout="horizontal"
              dataSource={userWithRecommendations.recommendations || []}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={item.title}
                    description={
                      <>
                        <Text type="secondary">{item.type}</Text>
                        <br />
                        {item.description}
                      </>
                    }
                  />
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Spin spinning={loading} tip="Generating the email...">
            {emailContent && (
              <Card
                title={
                  <span>
                    <MailOutlined style={{ marginRight: '8px' }} />
                    Generated Email
                  </span>
                }
                className="email-content-card"
              >
                <Paragraph className="email-subject">
                  <Text strong>Subject:</Text> {emailContent.subject}
                </Paragraph>
                <Divider />
                <Paragraph className="email-body">
                  {emailContent.body}
                </Paragraph>
              </Card>
            )}
          </Spin>
        </Col>
      </Row>
    </>
  );
};

export default UserDetails;
