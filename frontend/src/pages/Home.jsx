import { useNavigate } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card, CardContent } from '../components/ui/card'
import { BookOpen, Target, TrendingUp } from 'lucide-react'

export default function Home() {
  const navigate = useNavigate()
  
  const features = [
    {
      icon: <BookOpen className="w-6 h-6" />,
      title: "Adaptive Learning",
      description: "Dynamic difficulty adjustment based on your performance",
      action: () => navigate('/subjects'),
    },
    {
      icon: <Target className="w-6 h-6" />,
      title: "Skill Mastery",
      description: "Track your progress with detailed analytics",
      action: () => navigate('/dashboard'),
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: "Personalized Path",
      description: "AI-powered learning recommendations",
      action: () => navigate('/personalized-path'),
    },
  ]
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-16">
          <h1 className="text-5xl font-bold mb-4 bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
            Welcome to AdaptLearn
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Personalized learning powered by Bayesian Knowledge Tracing. Our adaptive platform adjusts to your skill level in real-time.
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="hover:shadow-lg transition-shadow cursor-pointer border-2 hover:border-primary"
              onClick={feature.action}
            >
              <CardContent className="p-6">
                <div className="mb-4 flex justify-center">
                  <div className="p-3 bg-primary/10 rounded-full text-primary">
                    {feature.icon}
                  </div>
                </div>
                <h3 className="text-xl font-semibold mb-2 text-center">
                  {feature.title}
                </h3>
                <p className="text-muted-foreground text-center text-sm">
                  {feature.description}
                </p>
                <div className="mt-4 flex justify-center">
                  <Button variant="outline" size="sm">
                    Get Started
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
