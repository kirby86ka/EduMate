import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card'

export default function Dashboard() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-50 via-white to-blue-50 py-8">
      <div className="container mx-auto px-4">
        <div className="mb-8">
          <h1 className="text-4xl font-bold mb-2">Analytics Dashboard</h1>
          <p className="text-muted-foreground">
            Track your learning progress and skill mastery
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Power BI Analytics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="aspect-video bg-muted rounded-lg flex items-center justify-center">
              <p className="text-muted-foreground">
                Power BI Dashboard will be embedded here
              </p>
            </div>
            <p className="text-sm text-muted-foreground mt-4">
              Connect your Power BI dashboard using the analytics endpoint at{' '}
              <code className="bg-muted px-2 py-1 rounded">
                /api/powerbi/analytics
              </code>
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
