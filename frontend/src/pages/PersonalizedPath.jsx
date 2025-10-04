import { useState } from 'react'
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { ExternalLink, Sparkles } from 'lucide-react'

export default function PersonalizedPath() {
  const [recommendation, setRecommendation] = useState(null)
  
  const resources = [
    {
      title: 'Khan Academy',
      description: 'Free educational videos and exercises',
      url: 'https://www.khanacademy.org/',
    },
    {
      title: 'Coursera',
      description: 'Online courses from top universities',
      url: 'https://www.coursera.org/',
    },
    {
      title: 'edX',
      description: 'University-level online courses',
      url: 'https://www.edx.org/',
    },
    {
      title: 'freeCodeCamp',
      description: 'Learn to code for free',
      url: 'https://www.freecodecamp.org/',
    },
  ]
  
  const getGeminiRecommendation = async () => {
    setRecommendation("Gemini integration will provide personalized learning path recommendations based on your performance and skill gaps.")
  }
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Personalized Learning Path</h1>
          <p className="text-muted-foreground">
            AI-powered recommendations tailored to your learning journey
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Sparkles className="w-5 h-5 text-primary" />
                AI Recommendations
              </CardTitle>
              <CardDescription>
                Get personalized study recommendations from Gemini AI
              </CardDescription>
            </CardHeader>
            <CardContent>
              {!recommendation ? (
                <Button onClick={getGeminiRecommendation} className="w-full">
                  Get AI Recommendation
                </Button>
              ) : (
                <div className="p-4 bg-muted rounded-lg">
                  <p className="text-sm">{recommendation}</p>
                </div>
              )}
              <p className="text-xs text-muted-foreground mt-4">
                Note: Gemini CLI integration coming soon
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Learning Resources</CardTitle>
              <CardDescription>
                Curated resources to enhance your learning
              </CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                {resources.map((resource, index) => (
                  <a
                    key={index}
                    href={resource.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex items-center justify-between p-3 rounded-lg border hover:bg-accent transition-colors"
                  >
                    <div>
                      <h4 className="font-medium">{resource.title}</h4>
                      <p className="text-xs text-muted-foreground">
                        {resource.description}
                      </p>
                    </div>
                    <ExternalLink className="w-4 h-4 text-muted-foreground" />
                  </a>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}
