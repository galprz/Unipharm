import createStore from "redux-zero";

const initialAppState = { current_user_email: "" };
const store = createStore(initialAppState);

export default store;