import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './LandingPage';
import Dashboard from './Dashboard';
import PeerReviewForm from './PeerReviewForm';
import EvaluationSummary from './EvaluationSummary';
import AiRecordGenerator from './AiRecordGenerator';
import GuardianPortal from './GuardianPortal';
import './responsive.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/progress" element={<Dashboard />} />
        <Route path="/ai-analysis" element={<AiRecordGenerator />} />
        <Route path="/billing" element={<EvaluationSummary />} />
        <Route path="/guardian" element={<GuardianPortal />} />
        <Route path="/peer-review" element={<PeerReviewForm />} />
      </Routes>
    </Router>
  );
}

export default App;
