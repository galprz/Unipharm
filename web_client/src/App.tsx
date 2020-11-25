import React, { Fragment } from 'react';
import Login from './componenets/registration/Login';
import { SignUp } from './componenets/registration/SignUp';

const App: React.FC = () => {
  return (
    <div>
      <SignUp></SignUp>
      <Login></Login>
    </div>
  );
}

export default App;
