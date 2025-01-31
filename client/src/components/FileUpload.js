import React, { useState } from 'react';
import '../styles.css';

function FileUpload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);
    setResult(null);

    if (!file) {
      setError('Please select a file to upload');
      return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
      const token = localStorage.getItem('token');  // Retrieve token from localStorage

      const response = await fetch('http://localhost:5001/predict', {
        method: 'POST',
        body: formData,
        headers: {
          'Authorization': `Bearer ${token}`, // Use 'Authorization' header with Bearer scheme
        },
      });

      if (!response.ok) {
        throw new Error('Failed to upload file');
      }

      const data = await response.json();
      if (data.error) {
        setError(data.error);
      } else {
        setResult(data);
      }
    } catch (err) {
      setError(err.message);
    }
  };

  const renderDetails = (details) => {
    switch (result.document_type) {
      case 'adhar':
        return (
          <>
            <p><strong>Name:</strong> {details.name}</p>
            <p><strong>Date of Birth:</strong> {details.date_of_birth}</p>
            <p><strong>Gender:</strong> {details.gender}</p>
            <p><strong>Aadhaar Number:</strong> {details.aadhaar_number}</p>
          </>
        );
      case 'pan':
        return (
          <>
            <p><strong>Name:</strong> {details.name}</p>
            <p><strong>Father's Name:</strong> {details.father_name}</p>
            <p><strong>Date of Birth:</strong> {details.date_of_birth}</p>
            <p><strong>PAN Number:</strong> {details.pan_number}</p>
          </>
        );
      case 'driving_license':
        return (
          <>
            <p><strong>Name:</strong> {details.name}</p>
            <p><strong>Date of Birth:</strong> {details.date_of_birth}</p>
            <p><strong>License Number:</strong> {details.license_number}</p>
          </>
        );
      case 'voter_id':
        return (
          <>
            <p><strong>Name:</strong> {details.name}</p>
            <p><strong>Father's Name:</strong> {details.father_name}</p>
            <p><strong>Voter ID Number:</strong> {details.voter_id_number}</p>
          </>
        );
      case 'passport':
        return (
          <>
            <p><strong>Name:</strong> {details.name}</p>
            <p><strong>Passport Number:</strong> {details.passport_number}</p>
            <p><strong>Date of Birth:</strong> {details.date_of_birth}</p>
            <p><strong>Nationality:</strong> {details.nationality}</p>
          </>
        );
      case 'utility':
        return (
          <>
            <p><strong>Account Holder Name:</strong> {details.account_holder_name}</p>
            <p><strong>Bill Number:</strong> {details.bill_number}</p>
            <p><strong>Address:</strong> {details.address}</p>
            <p><strong>Amount Due:</strong> {details.amount_due}</p>
          </>
        );
      default:
        return <p>No details available</p>;
    }
  };

  return (
    <div className="container">
      <h1>Document Verification</h1>
      <form onSubmit={handleSubmit} className="upload-form">
        <label htmlFor="file">Upload your document:</label>
        <input type="file" id="file" onChange={handleFileChange} accept="image/*" required />
        <button type="submit">Upload</button>
      </form>
      <div className="result-container">
        {error && <p className="error-message">Error: {error}</p>}
        {result && (
          <div className="result">
            <p><strong>Document Type:</strong> {result.document_type}</p>
            <p><strong>Confidence:</strong> {result.confidence.toFixed(2)}</p>
            <p><strong>Extracted Text:</strong></p>
            <pre>{result.extracted_text}</pre>
            <div>
              <h3>Details:</h3>
              {renderDetails(result.details)}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default FileUpload;
