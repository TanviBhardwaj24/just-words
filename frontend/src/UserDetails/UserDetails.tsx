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
  Select,
} from 'antd';
import {
  UserOutlined,
  MailOutlined,
  DashboardOutlined,
  ArrowLeftOutlined,
} from '@ant-design/icons';
import { allUsers, EmailContent } from '../types';
import './UserDetails.scss';

const { Text, Paragraph, Title } = Typography;
const { Option } = Select;

interface UserDetailsProps {
  allUsers: allUsers | null;
  onBack: () => void;
}

const UserDetails: React.FC<UserDetailsProps> = ({ allUsers, onBack }) => {
  const [emailContent, setEmailContent] = useState<EmailContent | null>(null);
  const [loading, setLoading] = useState(false);
  const [emailType, setEmailType] = useState('');

  useEffect(() => {
    if (allUsers?.id && emailType) {
      fetchEmailContent(allUsers.id.toString(), emailType);
    }
  }, [allUsers, emailType]);

  const fetchEmailContent = async (userId: string, type: string) => {
    setLoading(true);
    try {
      const emailResponse = await axios.post(
        `http://localhost:8000/api/generate-email/${userId}`,
        { type }
      );
      setEmailContent(emailResponse.data);
    } catch (error) {
      console.error('Error fetching email content:', error);
      message.error('Failed to fetch email content. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  if (!allUsers) return null;

  return (
    <>
      <Button
        icon={<ArrowLeftOutlined />}
        onClick={onBack}
        className="back-button"
        style={{ marginBottom: '16px' }}
      >
        Back to Dashboard
      </Button>

      <Row gutter={24}>
        <Col span={12}>
          <div style={{ marginBottom: 16 }}>
            <Title level={5}>
              Please select the email type to be generated
            </Title>
            <Select
              placeholder="Please select the email type to be generated"
              style={{ width: '100%' }}
              onChange={(value) => setEmailType(value)}
            >
              <Option value="winback">Winback Campaign</Option>
              <Option value="weekly-digest">Weekly Digest</Option>
              <Option value="signup-thankyou">Thanks for Signing Up</Option>
            </Select>
          </div>

          <Card
            title={
              <span>
                <UserOutlined /> User Profile
              </span>
            }
            className="user-profile-card"
          >
            <Paragraph>
              <Text strong>Name:</Text> {allUsers.name || 'N/A'}
            </Paragraph>
            <Paragraph>
              <Text strong>Age:</Text> {allUsers.age || 'N/A'}
            </Paragraph>
            <Paragraph>
              <Text strong>Location:</Text> {allUsers.location || 'N/A'}
            </Paragraph>
            <Paragraph>
              <Text strong>Interests:</Text>{' '}
              {allUsers.interests?.join(', ') || 'None'}
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
              dataSource={allUsers.recommendations || []}
              renderItem={(item) => (
                <List.Item>
                  <List.Item.Meta
                    title={item.title}
                    description={
                      <>
                        <Text type="secondary">{item.type}</Text> <br />
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
                    Generated Email Preview
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
