import { useState } from 'react'
import SubjectSelection from './pages/SubjectSelection'
import Assessment from './pages/Assessment'
import Results from './pages/Results'

function App() {
  const [currentPage, setCurrentPage] = useState('subjects')
  const [selectedSubject, setSelectedSubject] = useState(null)
  const [sessionId, setSessionId] = useState(null)

  const handleSubjectSelect = (subject, session) => {
    setSelectedSubject(subject)
    setSessionId(session.session_id)
    setCurrentPage('assessment')
  }

  const handleAssessmentComplete = () => {
    setCurrentPage('results')
  }

  const handleRestart = () => {
    setCurrentPage('subjects')
    setSelectedSubject(null)
    setSessionId(null)
  }

  return (
    <div className="container">
      {currentPage === 'subjects' && (
        <SubjectSelection onSubjectSelect={handleSubjectSelect} />
      )}
      {currentPage === 'assessment' && (
        <Assessment
          subject={selectedSubject}
          sessionId={sessionId}
          onComplete={handleAssessmentComplete}
        />
      )}
      {currentPage === 'results' && (
        <Results sessionId={sessionId} onRestart={handleRestart} />
      )}
    </div>
  )
}

export default App
