import './App.css';
import React from 'react';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Voted from '../components/Voted';
import ContenderForm from '../components/ContenderForm';
import Register from '../components/Register';


function App() {

  return (
    <div className="App">
      <BrowserRouter>
        <Routes>
          <Route element={<Register/>} path="/api/register" default/>
          <Route element={<ContenderForm/>} path="/api/contender" />
          <Route element={<Voted/>} path="/api/selected/contender/:id" />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
