import React, { useState, useEffect } from 'react';
import axios from 'axios';

const apiUrl = "http://127.0.0.1:8000"

const AutocompleteForm = () => {
  const [bandName, setBandName] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const handleChange = async (e) => {
    const input = e.target.value;
    setBandName(input);

    if (input.length > 0) {
      try {
        const response = await axios.get(`${apiUrl}/autocomplete/?prefix=${input}`);
        setSuggestions(response.data);
      } catch (error) {
        console.error('Error fetching autocomplete suggestions:', error);
      }
    } else {
      setSuggestions([]);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', bandName);
  };

  return (
    <div>
      <h2>Autocomplete Band Name Search</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Band Name:
          <input 
            type="text" 
            value={bandName} 
            onChange={handleChange} 
            placeholder="Type band name" 
          />
        </label>
        <button type="submit">View</button>
      </form>
      <div>
        {suggestions.length > 0 && (
          <ul>
            {suggestions.map((suggestion, index) => (
              <li key={index}>{suggestion}</li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default AutocompleteForm;
