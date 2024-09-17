import React, { useState, useEffect } from 'react';
import axios from 'axios';

const apiUrl = "http://127.0.0.1:8000";

const AutocompleteForm = () => {
  const [bandName, setBandName] = useState('');
  const [albumTitle, setAlbumTitle] = useState('');
  const [songTitle, setSongTitle] = useState('');
  const [activeField, setActiveField] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  const handleInputChange = async (field, value) => {
    if (field === 'bandName') setBandName(value);
    if (field === 'albumTitle') setAlbumTitle(value);
    if (field === 'songTitle') setSongTitle(value);

    setActiveField(field);

    const params = {};

    if (field === 'albumTitle' && bandName) {
      params.bandName = bandName;
    }

    if (field === 'songTitle' && bandName && albumTitle) {
      params.bandName = bandName;
      params.albumTitle = albumTitle;
    }

    if (value.length > 0) {
      try {
        const response = await axios.get(`${apiUrl}/autocomplete/?prefix=${value}`, {params});
        setSuggestions(response.data);
      } catch (error) {
        console.error('Error fetching autocomplete suggestions:', error);
      }
    } else {
      setSuggestions([]);
    }
  };

  const handleSuggestionClick = (suggestion) => {
    if (activeField === 'bandName') {
      setBandName(suggestion);
    } else if (activeField === 'albumTitle') {
      setAlbumTitle(suggestion);
    } else if (activeField === 'songTitle') {
      setSongTitle(suggestion);
    }

    // Clear suggestions after selection
    setSuggestions([]);
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log('Submitted:', {
      bandName,
      albumTitle,
      songTitle,
    });
  };

  return (
    <div>
      <h2>Autocomplete Band, Album, and Song Search</h2>
      <form onSubmit={handleSubmit}>
        <label>
          Band Name:
          <input
            type="text"
            value={bandName}
            onChange={(e) => handleInputChange('bandName', e.target.value)}
            placeholder="Type band name"
          />
        </label>

        <label>
          Album Title:
          <input
            type="text"
            value={albumTitle}
            onChange={(e) => handleInputChange('albumTitle', e.target.value)}
            placeholder="Type album title"
            disabled={!bandName}
          />
        </label>

        <label>
          Song Title:
          <input
            type="text"
            value={songTitle}
            onChange={(e) => handleInputChange('songTitle', e.target.value)}
            placeholder="Type song title"
            disabled={!albumTitle}
          />
        </label>

        <button type="submit">View</button>
      </form>

      <div>
        {suggestions.length > 0 && (
          <ul>
            {suggestions.map((suggestion, index) => (
              <li key={index} onClick={() => handleSuggestionClick(suggestion)}>
                {suggestion}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
};

export default AutocompleteForm;
