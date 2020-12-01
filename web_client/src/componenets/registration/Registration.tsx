import React from "react";
import Login from './Login';
import { SignUp } from './SignUp';
import { Route, Link, BrowserRouter as Router } from 'react-router-dom';

export class Registration extends React.Component{

    render()
    {
        return(
            <Router>
                <div>
                    <Route exact path="/" component={Login} />
                    <Route path="/Login" component={Login} />
                    <Route path="/SignUp" component={SignUp} />
                </div>
            </Router>
        );
    }
}