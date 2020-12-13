import React from 'react';
import {Registration} from './componenets/registration/Registration';
import { Provider } from "redux-zero/react";
import store from "./store/store";

const App: React.FC = () => {
  return (
    <div>
      <Provider store={store}>
        <Registration></Registration>
      </Provider>
    </div>
  );
}

export default App;
