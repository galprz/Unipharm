import React from 'react';
import { Provider } from "redux-zero/react";
import store from "./store/store";

const App: React.FC = () => {
  return (
    <div>
      <Provider store={store}>
      </Provider>
    </div>
  );
}

export default App;
