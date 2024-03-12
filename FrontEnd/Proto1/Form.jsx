import { useState } from 'react';
import './styles.css';

const questions = {
  'Individual contributor': 'What notable achievements has this individual made as an individual contributor?\n',
  'People manager': 'How effectively does this individual manage their team and handle interpersonal dynamics\n?',
  'Project Manager': 'How well does this individual lead and coordinate their team to achieve goals?\n'
};

export default function ControlledComponent() {
  const [lastname, setLastName] = useState('');
  const [firstname, setFirstName] = useState('');
  const [department, setDepartment] = useState('');
  const [jCategory, setJCategory] = useState('');
  const [email, setEmail] = useState('');
  
  const [educations, setEducations] = useState([
    { university: '', location: '', degree: '', program: '', graduationYear: '' }
  ]);

  const [selectedRoles, setSelectedRoles] = useState([]);
  const [responses, setResponses] = useState({});

  const handleChange = (event, setter) => {
    setter(event.target.value);
  };

  const handleEducationChange = (event, index, key) => {
    const newEducations = [...educations];
    newEducations[index][key] = event.target.value;
    setEducations(newEducations);
  };

  const addEducation = () => {
    setEducations([...educations, { university: '', location: '', degree: '', program: '', graduationYear: '' }]);
  };

  const removeEducation = (index) => {
    const newEducations = [...educations];
    newEducations.splice(index, 1);
    setEducations(newEducations);
  };

  const handleCheckboxChange = (event) => {
    const roleName = event.target.name;
    const isChecked = event.target.checked;
    
    if (isChecked) {
      setSelectedRoles([...selectedRoles, roleName]);
      setResponses({ ...responses, [roleName]: '' });
    } else {
      setSelectedRoles(selectedRoles.filter(role => role !== roleName));
      const updatedResponses = { ...responses };
      delete updatedResponses[roleName];
      setResponses(updatedResponses);
    }
  };

  const handleResponseChange = (event, roleName) => {
    setResponses({ ...responses, [roleName]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
  
    // Extracting educational history
    const educationalHistory = educations.map((education) => ({
      university: education.university,
      location: education.location,
      degree: education.degree,
      program: education.program,
      graduationYear: education.graduationYear
    }));
  
    // Logging all form data
    console.log("Last Name:", lastname);
    console.log("First Name:", firstname);
    console.log("Department Name:", department);
    console.log("Job Category:", jCategory);
    console.log("Email:", email);
    console.log("Educational History:", educationalHistory);
    console.log("Selected Roles:", selectedRoles);
    console.log("Responses:", responses);
  };

  return (
    <form className="container" onSubmit={handleSubmit}>
      <div className="header-container">
        <header>Talent Review</header><br/><br/>
      </div>
      <div className="form-row">
        <div className="form-column">
          <header>Nominee Information</header>
          <label>
            Last Name:<br/>
            <input type="text" value={lastname} onChange={(e) => handleChange(e, setLastName)} />
            <br/>
          </label>

          <label>
            First Name:<br/>
            <input type="text" value={firstname} onChange={(e) => handleChange(e, setFirstName)} />
            <br/>
          </label>

          <label>
            Department Name:<br/>
            <input type="text" value={department} onChange={(e) => handleChange(e, setDepartment)} />
            <br/>
          </label>

          <label>
            Job Category:<br/>
            <input type="text" value={jCategory} onChange={(e) => handleChange(e, setJCategory)} />
            <br/>
          </label>

          <label>
            Email:<br/>
            <input type="text" value={email} onChange={(e) => handleChange(e, setEmail)} />
            <br/><br/><br/>
          </label>
        </div>

        <div className="form-column">
          <header>Education</header>
          {educations.map((education, index) => (
            <div key={index}>
              <label>
                University/College name:<br/>
                <input type="text" value={education.university} onChange={(e) => handleEducationChange(e, index, 'university')} />
                <br/>
              </label>

              <label>
                Location:<br/>
                <input type="text" value={education.location} onChange={(e) => handleEducationChange(e, index, 'location')} />
                <br/>
              </label>

              <label>
                Degree:<br/>
                <input type="text" value={education.degree} onChange={(e) => handleEducationChange(e, index, 'degree')} />
                <br/>
              </label>

              <label>
                Program:<br/>
                <input type="text" value={education.program} onChange={(e) => handleEducationChange(e, index, 'program')} />
                <br/>
              </label>

              <label>
                Graduation Year:<br/>
                <input type="text" value={education.graduationYear} onChange={(e) => handleEducationChange(e, index, 'graduationYear')} />
                <br/><br/>
              </label>

              {index > 0 && (
                <button type="button" onClick={() => removeEducation(index)}>Remove</button>
              )}
            </div>
          ))}
          {educations.length < 3 && <button type="button" onClick={addEducation}>Add Education</button>}
        </div>
      </div>

      <div className="form-column">
        <header>Role Selection</header>
        <label>
          <input type="checkbox" name="People manager" checked={selectedRoles.includes("People manager")} onChange={handleCheckboxChange}/>
          People Manager:<br/>
        </label>

        <label>
          <input type="checkbox" name="Project Manager" checked={selectedRoles.includes("Project Manager")} onChange={handleCheckboxChange}/>
          Project Manager:<br/>
        </label>

        <label>
          <input type="checkbox" name="Individual contributor" checked={selectedRoles.includes("Individual contributor")} onChange={handleCheckboxChange}/>
          Individual Contributor:<br/>
        </label>

        {selectedRoles.map(role => (
          <div key={role}>
            <div>{questions[role]}</div>
            <textarea 
              value={responses[role] || ''} 
              onChange={(event) => handleResponseChange(event, role)}
              placeholder="Enter your response..."
            />
          </div>
        ))}
        <button type="submit">Submit</button>
      </div>
    </form>
  );
}
