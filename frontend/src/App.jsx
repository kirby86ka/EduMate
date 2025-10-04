import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { lazy, Suspense } from 'react'
import Navbar from './components/Navbar'

const Home = lazy(() => import('./pages/Home'))
const Subjects = lazy(() => import('./pages/Subjects'))
const Quiz = lazy(() => import('./pages/Quiz'))
const Dashboard = lazy(() => import('./pages/Dashboard'))
const PersonalizedPath = lazy(() => import('./pages/PersonalizedPath'))

const LoadingFallback = () => (
  <div className="min-h-screen bg-background flex items-center justify-center">
    <div className="text-center">
      <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      <p className="mt-4 text-muted-foreground">Loading...</p>
    </div>
  </div>
)

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Navbar />
        <Suspense fallback={<LoadingFallback />}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/subjects" element={<Subjects />} />
            <Route path="/quiz/:subject" element={<Quiz />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/personalized-path" element={<PersonalizedPath />} />
          </Routes>
        </Suspense>
      </div>
    </Router>
  )
}

export default App
