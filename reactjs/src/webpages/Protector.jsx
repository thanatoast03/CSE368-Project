import React from 'react';
import { Navigate } from 'react-router-dom';
import { isAuthenticated } from '../auth';

const Protector = ({ element: Component }) => {
  return isAuthenticated() ? Component : <Navigate to="/loggedIn" />;
};

export default Protector;