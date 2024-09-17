import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AutocompleteForm from './components/AutocompleteForm';
import AutocompleteFormTrie from './components/AutocompleteFormTrie';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route exat path="/" element={<AutocompleteForm/>} />
          <Route path="/trie" element={<AutocompleteFormTrie/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
