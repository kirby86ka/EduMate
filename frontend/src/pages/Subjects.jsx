import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'
import { Button } from '../components/ui/button'
import { Calculator, Flask, Code } from 'lucide-react'

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
      icon: <Flask className="w-12 h-12" />,
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
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">Choose Your Subject</h1>
          <p className="text-muted-foreground">
            Select a subject to begin your adaptive assessment
          </p>
        </div>
        
        <div className="grid md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {subjects.map((subject) => (
            <Card key={subject.id} className="hover:shadow-xl transition-all">
              <CardHeader>
                <div className={`w-20 h-20 mx-auto mb-4 rounded-full bg-gradient-to-br ${subject.color} flex items-center justify-center text-white`}>
                  {subject.icon}
                </div>
                <CardTitle className="text-center text-2xl">{subject.name}</CardTitle>
              </CardHeader>
              <CardContent className="text-center">
                <p className="text-muted-foreground mb-6">{subject.description}</p>
                <Button 
                  className="w-full" 
                  onClick={() => handleStartQuiz(subject.id)}
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
