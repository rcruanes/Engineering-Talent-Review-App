import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import NominatorDashboard from './components/NominatorDashboard';
import RecommenderDashboard from './components/RecommenderDashboard';
import ReviewCommitteeDashboard from './components/ReviewCommitteeDashboard';
import NewNomineeForm from './components/NewNomineeForm';
import ViewNominee from './components/ViewNominee';
import EditNominee from './components/EditNominee';
import RecommendNominee from './components/RecommendNominee';
import NomineeDetails from './components/NomineeDetails';
import NomineeEducationForm from './components/NomineeEducationForm';
import EditEducationForm from './components/EditEducationForm'; 
import ProtectedRoute from './components/ProtectedRoute';  

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Register />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/recommender/dashboard" element={
          <ProtectedRoute allowedRoles={['Recommender', 'Nominator']}>
            <RecommenderDashboard />
          </ProtectedRoute>
        } />
        <Route path="/review/dashboard" element={
          <ProtectedRoute allowedRoles={['Review Committee']}>
            <ReviewCommitteeDashboard />
          </ProtectedRoute>
        } />
        <Route path="/nominee/dashboard" element={
          <ProtectedRoute allowedRoles={['Nominator']}>
            <NominatorDashboard />
          </ProtectedRoute>
        } />
        <Route path="/nominee/new" element={<NewNomineeForm />} />
        <Route path="/nominee/:id/edit" element={<EditNominee />} />
        <Route path="/nominee/:id/info" element={<ViewNominee />} />
        <Route path="/recommend/new" element={<RecommendNominee />} />
        <Route path="/review/nominee/:nomineeId/details" element={<NomineeDetails />} />
        <Route path="/nominee/:id/education" element={<NomineeEducationForm />} />
        <Route path="/nominee/:id/education/edit" element={<EditEducationForm />} />
      </Routes>
    </Router>
  );
}

export default App;
