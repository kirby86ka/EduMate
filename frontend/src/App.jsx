import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import Subjects from './pages/Subjects'
import Quiz from './pages/Quiz'
import Dashboard from './pages/Dashboard'
import PersonalizedPath from './pages/PersonalizedPath'

function App() {
  return (
    <Router>
      <div className="min-h-screen">
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/subjects" element={<Subjects />} />
          <Route path="/quiz/:subject" element={<Quiz />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/personalized-path" element={<PersonalizedPath />} />
        </Routes>
      </div>
    </Router>
  )
}

export default App
