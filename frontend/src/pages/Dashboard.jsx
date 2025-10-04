import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Tabs, TabsList, TabsTrigger, TabsContent } from '../components/ui/tabs'
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import { CheckCircle2, XCircle, TrendingUp } from 'lucide-react'
import api from '../services/api'

export default function Dashboard() {
  const [selectedSubject, setSelectedSubject] = useState('Maths')
  const [analyticsData, setAnalyticsData] = useState({
    Maths: null,
    Science: null,
    Python: null
  })
  const [loading, setLoading] = useState(false)

  const loadSubjectData = async (subject) => {
    if (analyticsData[subject]) return
    
    setLoading(true)
    try {
      const data = await api.getSubjectAnalytics(subject.toLowerCase())
      setAnalyticsData(prev => ({ ...prev, [subject]: data }))
    } catch (error) {
      console.error('Failed to load analytics:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadSubjectData(selectedSubject)
  }, [selectedSubject])

  const renderSubjectAnalytics = (subject) => {
    const data = analyticsData[subject]

    if (loading && !data) {
      return (
        <div className="flex items-center justify-center py-12">
          <p className="text-muted-foreground">Loading analytics...</p>
        </div>
      )
    }

    if (!data || data.total_questions === 0) {
      return (
        <div className="flex items-center justify-center py-12">
          <div className="text-center">
            <p className="text-muted-foreground mb-2">No quiz data yet for {subject}</p>
            <p className="text-sm text-muted-foreground">Complete a quiz to see your analytics</p>
          </div>
        </div>
      )
    }

    const masteryPercent = (data.mastery_estimate * 100).toFixed(1)
    const masteryColor = 
      data.mastery_estimate >= 0.7 ? 'text-green-600' :
      data.mastery_estimate >= 0.4 ? 'text-yellow-600' :
      'text-red-600'

    return (
      <div className="space-y-6">
        <div className="grid md:grid-cols-3 gap-6">
          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Questions</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{data.total_questions}</div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">Accuracy</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">{data.accuracy}%</div>
              <p className="text-xs text-muted-foreground mt-1">
                {data.correct_answers}/{data.total_questions} correct
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader className="pb-3">
              <CardTitle className="text-sm font-medium text-muted-foreground">Bayesian Mastery Estimate</CardTitle>
            </CardHeader>
            <CardContent>
              <div className={`text-3xl font-bold ${masteryColor}`}>
                {masteryPercent}%
              </div>
              <p className="text-xs text-muted-foreground mt-1">
                {data.mastery_estimate >= 0.7 ? 'Proficient' : 
                 data.mastery_estimate >= 0.4 ? 'Developing' : 'Beginner'}
              </p>
            </CardContent>
          </Card>
        </div>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <TrendingUp className="w-5 h-5" />
              Growth Chart
            </CardTitle>
          </CardHeader>
          <CardContent>
            {data.growth_data && data.growth_data.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={data.growth_data}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis 
                    dataKey="question_number" 
                    label={{ value: 'Question Number', position: 'insideBottom', offset: -5 }}
                  />
                  <YAxis 
                    label={{ value: 'Accuracy (%)', angle: -90, position: 'insideLeft' }}
                  />
                  <Tooltip 
                    content={({ active, payload }) => {
                      if (active && payload && payload.length) {
                        return (
                          <div className="bg-white p-3 border rounded-lg shadow-lg">
                            <p className="font-semibold">Question {payload[0].payload.question_number}</p>
                            <p className="text-sm">
                              Correct: {payload[0].payload.correct}/{payload[0].payload.question_number}
                            </p>
                            <p className="text-sm text-primary font-semibold">
                              Accuracy: {payload[0].value}%
                            </p>
                          </div>
                        )
                      }
                      return null
                    }}
                  />
                  <Line 
                    type="monotone" 
                    dataKey="accuracy" 
                    stroke="hsl(var(--primary))" 
                    strokeWidth={2}
                    dot={{ fill: 'hsl(var(--primary))', r: 4 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            ) : (
              <p className="text-center text-muted-foreground py-8">No growth data available</p>
            )}
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Question History</CardTitle>
          </CardHeader>
          <CardContent>
            {data.question_history && data.question_history.length > 0 ? (
              <div className="space-y-3">
                {data.question_history.slice().reverse().map((item, index) => (
                  <div 
                    key={index}
                    className={`p-4 rounded-lg border ${
                      item.is_correct 
                        ? 'border-green-200 bg-green-50' 
                        : 'border-red-200 bg-red-50'
                    }`}
                  >
                    <div className="flex items-start gap-3">
                      {item.is_correct ? (
                        <CheckCircle2 className="w-5 h-5 text-green-600 mt-1 flex-shrink-0" />
                      ) : (
                        <XCircle className="w-5 h-5 text-red-600 mt-1 flex-shrink-0" />
                      )}
                      <div className="flex-1 min-w-0">
                        <div className="flex flex-wrap items-center gap-2 mb-2">
                          <span className="px-2 py-1 bg-white rounded text-xs font-medium">
                            {item.topic}
                          </span>
                          <span className="px-2 py-1 bg-white rounded text-xs">
                            {item.difficulty}
                          </span>
                        </div>
                        <p className="text-sm break-words">{item.question}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-center text-muted-foreground py-8">No questions answered yet</p>
            )}
          </CardContent>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-8">
      <div className="container mx-auto px-4">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold mb-8 text-center">Analytics Dashboard</h1>

          <Tabs value={selectedSubject} onValueChange={setSelectedSubject} className="w-full">
            <TabsList className="grid w-full max-w-md mx-auto grid-cols-3 mb-8">
              <TabsTrigger value="Maths">Maths</TabsTrigger>
              <TabsTrigger value="Science">Science</TabsTrigger>
              <TabsTrigger value="Python">Python</TabsTrigger>
            </TabsList>

            <TabsContent value="Maths">
              {renderSubjectAnalytics('Maths')}
            </TabsContent>

            <TabsContent value="Science">
              {renderSubjectAnalytics('Science')}
            </TabsContent>

            <TabsContent value="Python">
              {renderSubjectAnalytics('Python')}
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  )
}
