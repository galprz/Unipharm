import React from "react";
import Login from './Login';
import { SignUp } from './SignUp';
import WarehouseScene from '../home/Home';
import { Route, BrowserRouter as Router } from 'react-router-dom';

export class Registration extends React.Component{

    render()
    {
        return(
            <Router>
                <div>
                    <Route exact path="/" component={Login} />
                    <Route path="/Login" component={Login} />
                    <Route path="/SignUp" component={SignUp} />
                    <Route path="/Home" component={WarehouseScene} />
                </div>
            </Router>
        );
    }
}