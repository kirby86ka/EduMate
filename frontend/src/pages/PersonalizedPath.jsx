import { useState, useEffect } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '../components/ui/tabs'
import { ExternalLink, Sparkles, AlertCircle, Youtube, Search, BookOpen } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import remarkMath from 'remark-math'
import remarkGfm from 'remark-gfm'
import rehypeKatex from 'rehype-katex'
import 'katex/dist/katex.min.css'
import api from '../services/api'

export default function PersonalizedPath() {
  const [activeTab, setActiveTab] = useState('Maths')
  const [data, setData] = useState({})
  const [loading, setLoading] = useState({})
  const [error, setError] = useState({})
  
  const subjects = ['Maths', 'Science', 'Python']
  
  const getRecommendations = async (subject) => {
    setLoading(prev => ({ ...prev, [subject]: true }))
    setError(prev => ({ ...prev, [subject]: null }))
    try {
      const recommendations = await api.getLearningRecommendations(null, subject)
      setData(prev => ({ ...prev, [subject]: recommendations }))
    } catch (err) {
      setError(prev => ({ ...prev, [subject]: err.message }))
    } finally {
      setLoading(prev => ({ ...prev, [subject]: false }))
    }
  }

  useEffect(() => {
    getRecommendations(activeTab)
  }, [activeTab])
  
  const renderSubjectContent = (subject) => {
    const isLoading = loading[subject]
    const subjectError = error[subject]
    const subjectData = data[subject]

    if (isLoading) {
      return (
        <div className="text-center py-12">
          <p className="text-muted-foreground">Analyzing your {subject} quiz data...</p>
        </div>
      )
    }

    if (subjectError) {
      return (
        <Card className="bg-card border-border">
          <CardContent className="p-8 text-center">
            <p className="text-red-500">{subjectError}</p>
            <Button onClick={() => getRecommendations(subject)} className="mt-4">
              Try Again
            </Button>
          </CardContent>
        </Card>
      )
    }

    if (!subjectData || !subjectData.has_data) {
      return (
        <Card className="bg-card border-border">
          <CardContent className="p-8 text-center">
            <AlertCircle className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
            <p className="text-lg font-medium mb-2">No {subject} Quiz Data Available</p>
            <p className="text-muted-foreground mb-4">
              Complete a {subject} quiz to get personalized learning recommendations!
            </p>
            <Button onClick={() => window.location.href = '/subjects'}>
              Take a Quiz
            </Button>
          </CardContent>
        </Card>
      )
    }
    
    return (
      <div className="space-y-6">
        <div className="text-muted-foreground text-sm">
          Based on {subjectData.total_quizzes} quiz{subjectData.total_quizzes !== 1 ? 'zes' : ''} and {subjectData.total_questions} question{subjectData.total_questions !== 1 ? 's' : ''}
        </div>

        <Card className="bg-card border-border">
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Sparkles className="w-5 h-5 text-primary" />
              AI Recommendations for {subject}
            </CardTitle>
            <CardDescription className="text-muted-foreground">
              Personalized insights from Gemini AI based on your {subject} quiz performance
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="p-4 bg-secondary/50 rounded-lg border border-border">
              <div className="markdown-content text-foreground">
                <ReactMarkdown
                  remarkPlugins={[remarkMath, remarkGfm]}
                  rehypePlugins={[rehypeKatex]}
                >
                  {subjectData.ai_recommendations}
                </ReactMarkdown>
              </div>
            </div>
          </CardContent>
        </Card>

        {subjectData.weak_areas && subjectData.weak_areas.length > 0 && (
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle>Areas to Focus On</CardTitle>
              <CardDescription className="text-muted-foreground">
                Topics where you can improve your performance
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {subjectData.weak_areas.map((area, index) => (
                  <div 
                    key={index}
                    className="p-4 rounded-lg border border-border bg-secondary/30"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <div>
                        <span className="font-semibold text-foreground">{area.subject}</span>
                        <span className="text-muted-foreground"> • </span>
                        <span className="text-foreground">{area.topic}</span>
                      </div>
                      <span className={`font-semibold ${
                        area.accuracy < 30 ? 'text-red-500' :
                        area.accuracy < 50 ? 'text-orange-500' :
                        'text-yellow-500'
                      }`}>
                        {area.accuracy}%
                      </span>
                    </div>
                    <p className="text-xs text-muted-foreground">
                      {area.questions_attempted} question{area.questions_attempted !== 1 ? 's' : ''} attempted
                    </p>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        {subjectData.learning_resources && subjectData.learning_resources.length > 0 && (
          <Card className="bg-card border-border">
            <CardHeader>
              <CardTitle>Learning Resources</CardTitle>
              <CardDescription className="text-muted-foreground">
                Curated resources to help you improve in your weak areas
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-6">
                {subjectData.learning_resources.map((resource, index) => (
                  <div key={index} className="p-4 border border-border rounded-lg bg-secondary/30">
                    <div className="mb-3">
                      <h4 className="font-semibold text-lg mb-1 text-foreground">{resource.title}</h4>
                      <p className="text-sm text-muted-foreground">{resource.description}</p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                      <a
                        href={resource.search_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-2 px-3 py-2 rounded-md border border-border hover:bg-accent transition-colors text-sm text-foreground"
                      >
                        <Search className="w-4 h-4" />
                        Google Search
                        <ExternalLink className="w-3 h-3" />
                      </a>
                      <a
                        href={resource.khan_academy_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-2 px-3 py-2 rounded-md border border-border hover:bg-accent transition-colors text-sm text-foreground"
                      >
                        <BookOpen className="w-4 h-4" />
                        Khan Academy
                        <ExternalLink className="w-3 h-3" />
                      </a>
                      <a
                        href={resource.youtube_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="inline-flex items-center gap-2 px-3 py-2 rounded-md border border-border hover:bg-accent transition-colors text-sm text-foreground"
                      >
                        <Youtube className="w-4 h-4" />
                        YouTube
                        <ExternalLink className="w-3 h-3" />
                      </a>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        )}

        <div className="text-center">
          <Button onClick={() => getRecommendations(subject)} variant="outline">
            <Sparkles className="w-4 h-4 mr-2" />
            Refresh Recommendations
          </Button>
        </div>
      </div>
    )
  }
  
  return (
    <div className="min-h-screen bg-background py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2 text-foreground">Learning Recommendations</h1>
          <p className="text-muted-foreground">
            AI-powered recommendations tailored to your learning journey
          </p>
        </div>

        <Tabs value={activeTab} onValueChange={setActiveTab} className="w-full">
          <TabsList className="grid w-full grid-cols-3 mb-6 bg-secondary">
            {subjects.map((subject) => (
              <TabsTrigger 
                key={subject} 
                value={subject}
                className="data-[state=active]:bg-primary data-[state=active]:text-primary-foreground"
              >
                {subject}
              </TabsTrigger>
            ))}
          </TabsList>
          
          {subjects.map((subject) => (
            <TabsContent key={subject} value={subject}>
              {renderSubjectContent(subject)}
            </TabsContent>
          ))}
        </Tabs>
      </div>
    </div>
  )
}
