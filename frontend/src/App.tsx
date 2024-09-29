import React, { useState } from 'react';
import axios from 'axios';
import { Layout, Input, Button, Card, List, Typography, Divider, Row, Col } from 'antd';

const { Header, Content } = Layout;
const { Title, Text, Paragraph } = Typography;

interface User {
  id: string;
  name: string;
  interests: string[];
}

interface Recommendation {
  type: string;
  title: string;
  description: string;
}

interface EmailContent {
  subject: string;
  body: string;
}

const App: React.FC = () => {
  const [userId, setUserId] = useState('');
  const [user, setUser] = useState<User | null>(null);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [emailContent, setEmailContent] = useState<EmailContent | null>(null);

  const fetchUserData = async () => {
    try {
      const userResponse = await axios.get(`http://localhost:8000/api/users/${userId}`);
      setUser(userResponse.data);

      const recommendationsResponse = await axios.get(`http://localhost:8000/api/recommendations/${userId}`);
      setRecommendations(recommendationsResponse.data);

      const emailResponse = await axios.post(`http://localhost:8000/api/generate-email/${userId}`);
      setEmailContent(emailResponse.data);
    } catch (error) {
      console.error('Error fetching data:', error);
      setUser(null);
      setRecommendations([]);
      setEmailContent(null);
    }
  };

  return (
    <Layout className="layout" style={{ minHeight: '100vh' }}>
      <Header>
        <Title level={3} style={{ color: 'white', margin: 0 }}>Email Marketing Dashboard</Title>
      </Header>
      <Content style={{ padding: '24px' }}>
        <Row gutter={24}>
          <Col span={12}>
            <Card>
              <Input
                placeholder="Enter User ID"
                value={userId}
                onChange={(e) => setUserId(e.target.value)}
                style={{ marginBottom: '16px' }}
              />
              <Button type="primary" onClick={fetchUserData} block>
                Fetch User Data
              </Button>

              {user && (
                <div style={{ marginTop: '24px' }}>
                  <Divider orientation="left">User Profile</Divider>
                  <Paragraph>
                    <Text strong>Name:</Text> {user.name}
                  </Paragraph>
                  <Paragraph>
                    <Text strong>Interests:</Text> {user.interests.join(', ')}
                  </Paragraph>
                </div>
              )}

              {recommendations.length > 0 && (
                <div style={{ marginTop: '24px' }}>
                  <Divider orientation="left">Recommendations</Divider>
                  <List
                    itemLayout="horizontal"
                    dataSource={recommendations}
                    renderItem={item => (
                      <List.Item>
                        <List.Item.Meta
                          title={item.title}
                          description={item.description}
                        />
                      </List.Item>
                    )}
                  />
                </div>
              )}
            </Card>
          </Col>

          <Col span={12}>
            {emailContent && (
              <Card title="Generated Email">
                <Paragraph>
                  <Text strong>Subject:</Text> {emailContent.subject}
                </Paragraph>
                <Divider />
                <Paragraph>
                  <pre style={{ whiteSpace: 'pre-wrap', fontFamily: 'inherit' }}>
                    {emailContent.body}
                  </pre>
                </Paragraph>
              </Card>
            )}
          </Col>
        </Row>
      </Content>
    </Layout>
  );
};

export default App;