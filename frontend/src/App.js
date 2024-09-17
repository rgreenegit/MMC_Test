import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import AutocompleteForm from './components/AutocompleteForm';
import AutocompleteFormTrie from './components/AutocompleteFormTrie';
import AutocompleteFormDB from './components/AutocompleteFormDB';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route exat path="/" element={<AutocompleteForm/>} />
          <Route path="/trie" element={<AutocompleteFormTrie/>} />
          <Route path="/db" element={<AutocompleteFormDB/>} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
