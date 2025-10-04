import { useNavigate } from 'react-router-dom'
import { Button } from '../components/ui/button'
import { Card, CardContent } from '../components/ui/card'
import { BookOpen, Target, TrendingUp, Sparkles, BarChart } from 'lucide-react'

export default function Home() {
  const navigate = useNavigate()
  
  const features = [
    {
      icon: <BookOpen className="w-6 h-6" />,
      title: "Adaptive Learning",
      description: "Dynamic difficulty adjustment based on your performance",
    },
    {
      icon: <Target className="w-6 h-6" />,
      title: "Skill Mastery",
      description: "Track your progress with detailed analytics",
    },
    {
      icon: <TrendingUp className="w-6 h-6" />,
      title: "Personalized Path",
      description: "AI-powered learning recommendations",
    },
  ]
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div 
        className="relative h-80 bg-cover bg-center flex items-center justify-center"
        style={{
          backgroundImage: 'linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url(/hero-bg.jpg)',
        }}
      >
        <div className="text-center z-10">
          <h1 className="text-5xl md:text-6xl font-bold mb-6 text-white drop-shadow-lg">
            Welcome to AdaptLearn
          </h1>
          <div className="flex gap-4 justify-center">
            <Button 
              size="lg" 
              onClick={() => navigate('/subjects')}
              className="bg-white text-purple-600 hover:bg-gray-100"
            >
              Try a Quick Quiz
            </Button>
            <Button 
              size="lg" 
              variant="outline"
              onClick={() => navigate('/dashboard')}
              className="bg-transparent text-white border-white hover:bg-white/20"
            >
              Check Recent Quizzes
            </Button>
          </div>
        </div>
      </div>

      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            Personalized learning powered by Bayesian Knowledge Tracing. Our adaptive platform adjusts to your skill level in real-time.
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto mb-12">
          {features.map((feature, index) => (
            <Card 
              key={index} 
              className="border-2"
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
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="flex gap-6 justify-center max-w-2xl mx-auto">
          <Button 
            size="lg" 
            className="flex-1 max-w-xs"
            onClick={() => navigate('/subjects')}
          >
            <Sparkles className="w-5 h-5 mr-2" />
            Take a Quiz
          </Button>
          <Button 
            size="lg" 
            variant="outline"
            className="flex-1 max-w-xs"
            onClick={() => navigate('/personalized-path')}
          >
            <BarChart className="w-5 h-5 mr-2" />
            Learning Recommendations
          </Button>
        </div>
      </div>
    </div>
  )
}
