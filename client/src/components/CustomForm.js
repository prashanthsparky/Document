import React, { useState } from 'react';
import '../customForm.css';

function CustomForm() {
  const [file, setFile] = useState(null);
  const [documentType, setDocumentType] = useState('');
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    dob: '',
    contact: '',
    gender: '',
    documentNumber: '',
    url: '',
    aboutMe: '',
  });
  const [isChecked, setIsChecked] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setIsChecked(false);
    setDocumentType('');
    setFormData({ ...formData, documentNumber: '' });
    setError('');
  };

  const handleCheck = async () => {
    if (!file) {
      alert('Please upload a document first.');
      return;
    }

    const token = localStorage.getItem('token');

    if (!token) {
      alert('Authentication token not found. Please log in again.');
      return;
    }

    const uploadData = new FormData();
    uploadData.append('file', file);

    setIsLoading(true);
    setError('');
    try {
      const response = await fetch('http://localhost:5001/predict', {
        method: 'POST',
        body: uploadData,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const result = await response.json();

      if (response.ok) {
        setDocumentType(result.document_type);
        setIsChecked(true);
        setFormData({
          ...formData,
          documentNumber: result.details.document_number || '',
        });
      } else {
        setError(result.error || 'An error occurred while processing the document.');
      }
    } catch (err) {
      setError('An unexpected error occurred. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!isChecked) {
      alert('Please check the document before submitting.');
      return;
    }

    alert('Form submitted successfully!');
    setFile(null);
    setDocumentType('');
    setFormData({
      name: '',
      email: '',
      dob: '',
      contact: '',
      gender: '',
      documentNumber: '',
      url: '',
      aboutMe: '',
    });
    setIsChecked(false);
    setError('');
  };

  return (
    <div className="container">
      <h1>Custom Form</h1>
      <form onSubmit={handleSubmit} className="custom-form">
        <label>Name:</label>
        <input
          type="text"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          placeholder="Enter your name"
          required
        />

        <label>Email ID:</label>
        <input
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          placeholder="Enter your email"
          required
        />

        <label>Date of Birth:</label>
        <input
          type="date"
          value={formData.dob}
          onChange={(e) => setFormData({ ...formData, dob: e.target.value })}
          required
        />

        <label>Contact No:</label>
        <input
          type="tel"
          value={formData.contact}
          onChange={(e) => setFormData({ ...formData, contact: e.target.value })}
          placeholder="Enter your contact number"
          required
        />

        <label>Gender:</label>
        <select
          value={formData.gender}
          onChange={(e) => setFormData({ ...formData, gender: e.target.value })}
          required
        >
          <option value="">Select Gender</option>
          <option value="male">Male</option>
          <option value="female">Female</option>
          <option value="other">Other</option>
        </select>

        <label>Document Upload:</label>
        <div className="file-input-section">
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <button type="button" onClick={handleCheck} className="check-button" disabled={!file || isLoading}>
            {isLoading ? 'Checking...' : 'Check'}
          </button>
        </div>

        {error && <p className="error-message">{error}</p>}

        {documentType && (
          <div className="document-type">
            <p>
              <strong>Detected Document Type: </strong>
              {documentType}
            </p>
          </div>
        )}

        <label>Document Number:</label>
        <input
          type="text"
          value={formData.documentNumber}
          onChange={(e) => setFormData({ ...formData, documentNumber: e.target.value })}
          placeholder="Enter your document number"
          required
        />

        <label>URL Link:</label>
        <input
          type="url"
          value={formData.url}
          onChange={(e) => setFormData({ ...formData, url: e.target.value })}
          placeholder="Enter a URL"
        />

        <label>About Me:</label>
        <textarea
          value={formData.aboutMe}
          onChange={(e) => setFormData({ ...formData, aboutMe: e.target.value })}
          placeholder="Tell us about yourself"
          rows="4"
        ></textarea>

        <button type="submit" disabled={!isChecked}>
          Submit
        </button>
      </form>
    </div>
  );
}

export default CustomForm;


