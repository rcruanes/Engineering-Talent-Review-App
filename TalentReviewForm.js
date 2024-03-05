import React, { useState } from 'react';
import SignInPage from './SignInPage'; // Import the SignInPage component
import './TalentReviewForm.css'; // Import CSS file for styling

const TalentReviewForm = () => {
  const initialFormData = {
    name: '',
    department: '',
    roles: [],
    performanceComparison: {},
    contributions: ''
  };

  const [reviewData, setReviewData] = useState({ ...initialFormData });
  const [submitted, setSubmitted] = useState(false);
  const [user, setUser] = useState(null); // State to track signed-in user

  const questions = {
    'Individual contributor': 'What notable achievements has this individual made as an individual contributor?',
    'People manager': 'How effectively does this individual manage their team and handle interpersonal dynamics?',
    'Project Manager': 'How well does this individual lead and coordinate their team to achieve goals?'
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    // Check word count
    const wordCount = value.split(/\s+/).length;
    if (wordCount > 250) {
      return; // Prevent further input
    }

    // Update state if within limit
    setReviewData(prevState => ({
      ...prevState,
      [name]: value
    }));
  }

  const handleRoleChange = (e) => {
    const { name, checked } = e.target;
    setReviewData(prevState => ({
      ...prevState,
      roles: checked ? [...prevState.roles, name] : prevState.roles.filter(role => role !== name)
    }));
  }

  const handlePerformanceComparisonChange = (role, value) => {
    setReviewData(prevState => ({
      ...prevState,
      performanceComparison: {
        ...prevState.performanceComparison,
        [role]: value
      }
    }));
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission, e.g., send data to backend
    console.log('Form submitted:', reviewData);
    // Show thank you message
    setSubmitted(true);
  }

  const handleResubmit = () => {
    setReviewData({ ...initialFormData });
    setSubmitted(false);
  }

  const handleSignIn = (username) => {
    setUser(username);
  };

  if (!user) {
    return <SignInPage onSignIn={handleSignIn} />;
  }

  if (submitted) {
    return (
      <div className="form-container">
        <h2>Thank You!</h2>
        <p>Your review has been submitted successfully.</p>
        <button className="resubmit-button" onClick={handleResubmit}>Resubmit</button>
      </div>
    );
  }

  return (
    <div>
      <div className="background"></div>
      <div className="form-container">
        <h2>Talent Review Form</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Name:        
            <input 
              type="text" 
              name="name" 
              value={reviewData.name} 
              onChange={handleChange} 
              required 
            />
          </label>
          <br />
          <label>
            Department:
            <input 
              type="text" 
              name="department" 
              value={reviewData.department} 
              onChange={handleChange} 
              required 
            />
          </label>
          <div className="label-container">
            <label>
              Individual contributor:
              <input 
                type="checkbox" 
                name="Individual contributor" 
                checked={reviewData.roles.includes("Individual contributor")} 
                onChange={handleRoleChange} 
              />
            </label>
            <br />
            <label>
              People manager:
              <input 
                type="checkbox" 
                name="People manager" 
                checked={reviewData.roles.includes("People manager")} 
                onChange={handleRoleChange} 
              />
            </label>
            <br />
            <label>
              Project Manager:
              <input 
                type="checkbox" 
                name="Project Manager" 
                checked={reviewData.roles.includes("Project Manager")} 
                onChange={handleRoleChange} 
              />
            </label>
          </div>
          {reviewData.roles.map(role => (
            <label key={role}>
              {questions[role]}
              <textarea 
                name={`performanceComparison_${role}`} 
                value={reviewData.performanceComparison[role]} 
                onChange={e => handlePerformanceComparisonChange(role, e.target.value)} 
                required 
              />
            </label>
          ))}
          <label>
            List technical patents; technical reports and presentations; development of products, applications and systems; and, application of facilities and services along with the evidence to verify the contribution:
            <textarea 
              name="contributions" 
              value={reviewData.contributions} 
              onChange={handleChange} 
              required 
            />
          </label>
          <button type="submit">Submit</button>
        </form>
      </div>
    </div>
  );
}

export default TalentReviewForm;
