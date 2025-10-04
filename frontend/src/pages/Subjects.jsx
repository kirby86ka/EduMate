import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Calculator, Beaker, Code } from 'lucide-react'

export default function Subjects() {
  const navigate = useNavigate()
  
  const subjects = [
    {
      id: 'maths',
      name: 'Maths',
      icon: <Calculator className="w-12 h-12" />,
      description: 'Master mathematical concepts',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      id: 'science',
      name: 'Science',
      icon: <Beaker className="w-12 h-12" />,
      description: 'Explore scientific principles',
      color: 'from-green-500 to-emerald-500',
    },
    {
      id: 'python',
      name: 'Python',
      icon: <Code className="w-12 h-12" />,
      description: 'Learn programming fundamentals',
      color: 'from-purple-500 to-pink-500',
    },
  ]
  
  const handleStartQuiz = (subjectId) => {
    navigate(`/quiz/${subjectId}`)
  }
  
  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto px-4 py-8 sm:py-16">
        <div className="text-center mb-8 sm:mb-12 animate-slide-up">
          <h1 className="text-3xl sm:text-4xl font-bold mb-4 text-foreground">Choose Your Subject</h1>
          <p className="text-sm sm:text-base text-muted-foreground">
            Select a subject to begin your adaptive assessment
          </p>
        </div>
        
        <div className="grid sm:grid-cols-2 md:grid-cols-3 gap-6 sm:gap-8 max-w-5xl mx-auto">
          {subjects.map((subject, index) => (
            <Card 
              key={subject.id} 
              className="hover-lift border-border bg-card animate-scale-in cursor-pointer group"
              style={{ animationDelay: `${index * 0.1}s` }}
              onClick={() => handleStartQuiz(subject.id)}
            >
              <CardHeader>
                <div className={`w-16 h-16 sm:w-20 sm:h-20 mx-auto mb-4 rounded-full bg-gradient-to-br ${subject.color} flex items-center justify-center text-white transition-smooth group-hover:scale-110 group-hover:rotate-6`}>
                  {subject.icon}
                </div>
                <CardTitle className="text-center text-xl sm:text-2xl text-foreground">{subject.name}</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-sm sm:text-base text-muted-foreground mb-6">{subject.description}</p>
                <Button 
                  className="w-full transition-smooth hover:scale-105" 
                  onClick={(e) => {
                    e.stopPropagation()
                    handleStartQuiz(subject.id)
                  }}
                >
                  Start Quiz
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}
