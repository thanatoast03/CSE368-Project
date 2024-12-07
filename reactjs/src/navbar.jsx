import React from 'react';
import {useNavigate} from 'react-router-dom';
import "./App.css";

const Navbar = () => {

    const navigate = useNavigate();

    const handleHome = () => {
        navigate('/')
    }

  return (
    <div className="navbarContainer">
        <button onClick={handleHome}>Home</button>
    </div>
  );
};

export default Navbar;

