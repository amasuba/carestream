import React, { useEffect, useState } from 'react'
import axios from 'axios'

function App() {
  const [scenario, setScenario] = useState(null)
  const [running, setRunning] = useState(false)

  useEffect(() => {
    // poll session state while running
    let t
    if (running) {
      t = setInterval(() => {
        axios.get('http://localhost:8000/api/scenario/state').then(res => setScenario(res.data))
      }, 800)
    } else {
      axios.get('http://localhost:8000/api/sessions/').then(res => setScenario({ session: res.data[0] }))
    }
    return () => clearInterval(t)
  }, [running])

  const start = async () => {
    await axios.post('http://localhost:8000/api/scenario/start')
    setRunning(true)
  }

  return (
    <div style={{ maxWidth: 900, margin: '0 auto', padding: 16 }}>
      import React, { useEffect, useState, useRef } from 'react'
      import axios from 'axios'
      import { Layout, Row, Col, Card, Button, Descriptions, List, Tag, Typography } from 'antd'
      import {
        LineChart,
        Line,
        XAxis,
        YAxis,
        Tooltip,
        CartesianGrid,
        ResponsiveContainer,
      } from 'recharts'
      import 'antd/dist/reset.css'
      import './styles/index.css'

      const { Title, Text } = Typography

      function App() {
        const [scenario, setScenario] = useState(null)
        const [running, setRunning] = useState(false)
        const [history, setHistory] = useState([])
        const lastQoeRef = useRef(null)

        useEffect(() => {
          let t
          const poll = async () => {
            try {
              const res = await axios.get('http://localhost:8000/api/scenario/state')
              const s = res.data
              setScenario(s)

              // append to history when qoe changes
              const q = s.session?.qoe_score
              const ts = new Date().toLocaleTimeString()
              if (q !== undefined && q !== null) {
                if (lastQoeRef.current !== q) {
                  setHistory(h => [...h.slice(-49), { time: ts, qoe: Number(q) }])
                  lastQoeRef.current = q
                }
              }
            } catch (err) {
              // fallback: try sessions endpoint
              try {
                const r2 = await axios.get('http://localhost:8000/api/sessions/')
                setScenario({ session: r2.data[0] })
              } catch (_) {}
            }
          }

          // start polling immediately and every 1s while running or always poll to update history
          poll()
          t = setInterval(poll, 1000)
          return () => clearInterval(t)
        }, [running])

        const start = async () => {
          await axios.post('http://localhost:8000/api/scenario/start')
          setRunning(true)
        }

        const chartData = history.length ? history : scenario?.session ? [{ time: new Date().toLocaleTimeString(), qoe: scenario.session.qoe_score }] : []

        return (
          <Layout style={{ minHeight: '100vh', padding: 24, background: '#f0f2f5' }}>
            <Row justify="space-between" align="middle" style={{ marginBottom: 16 }}>
              <Col>
                <Title level={3}>CareStream360 — Johannesburg Peak Demo</Title>
              </Col>
              <Col>
                <Button type="primary" onClick={start} disabled={running}>
                  Start Demo Scenario
                </Button>
              </Col>
            </Row>

            <Row gutter={[16, 16]}>
              <Col xs={24} md={8}>
                <Card>
                  <Title level={5}>Session</Title>
                  <Descriptions column={1} size="small">
                    <Descriptions.Item label="Customer">{scenario?.session?.customer ?? '-'}</Descriptions.Item>
                    <Descriptions.Item label="QoE Score">{scenario?.session?.qoe_score ?? '-'}</Descriptions.Item>
                    <Descriptions.Item label="Status">{scenario?.session?.status ?? '-'}</Descriptions.Item>
                  </Descriptions>
                </Card>

                <Card style={{ marginTop: 12 }}>
                  <Title level={5}>Tickets</Title>
                  <List
                    dataSource={scenario?.tickets ?? []}
                    locale={{ emptyText: 'No tickets' }}
                    renderItem={t => (
                      <List.Item>
                        <List.Item.Meta
                          title={<Text strong>{t.title}</Text>}
                          description={`Priority: ${t.priority} — Assigned: ${t.assigned_to}`}
                        />
                      </List.Item>
                    )}
                  />
                </Card>

                <Card style={{ marginTop: 12 }}>
                  <Title level={5}>Notifications</Title>
                  <List
                    dataSource={scenario?.notifications ?? []}
                    locale={{ emptyText: 'No notifications' }}
                    renderItem={n => (
                      <List.Item>
                        <div>
                          <div>{n.message}</div>
                          <Text type="secondary">{new Date(n.sent_at).toLocaleString()}</Text>
                        </div>
                      </List.Item>
                    )}
                  />
                </Card>
              </Col>

              <Col xs={24} md={16}>
                <Card>
                  <Title level={5}>QoE Over Time</Title>
                  <div style={{ height: 320 }}>
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={chartData} margin={{ top: 8, right: 16, left: 0, bottom: 8 }}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="time" />
                        <YAxis domain={[0, 5]} />
                        <Tooltip />
                        <Line type="monotone" dataKey="qoe" stroke="#1890ff" strokeWidth={2} dot={{ r: 3 }} />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                </Card>

                <Card style={{ marginTop: 12 }}>
                  <Title level={5}>Progress</Title>
                  <div>
                    <Text strong>Current Step:</Text> <Tag color="blue">{scenario?.current_step ?? '-'}</Tag>
                  </div>
                </Card>
              </Col>
            </Row>
          </Layout>
        )
      }

      export default App
