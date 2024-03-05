import React, { useState, useEffect } from 'react';
import './App.css';
import Header from './components/Header';
//import Footer from './components/Footer';
import TalentReviewForm from './components/TalentReviewForm';
import Loading from './components/Loading'; // Import the Loading component

function App() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Simulate loading delay with setTimeout
    const timer = setTimeout(() => {
      setLoading(false);
    }, 3000); // Adjust the time as needed

    // Clean up the timer on component unmount
    return () => clearTimeout(timer);
  }, []);

  return (
    <div className="App">
      <Loading /> {/* Render the Loading component */}
      <Header />
      {!loading && <TalentReviewForm />} {/* Render the TalentReviewForm only when loading is false */}
    </div>
  );
}

export default App;
