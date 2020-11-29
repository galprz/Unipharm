import React from 'react';
import '../../../src/Style.css';
import './RegistrationStyle.css';
import { TextField } from "../common/TextField";
import Utils from './RegistrationUtils';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';

interface LoginState {
  username : string,
  password : string
};

export class Login extends React.Component<any, LoginState>{

  constructor(props: any){
    super(props);
    const initialState = {
      username : '',
      password : '',
    }
    this.state = initialState;
    this.handleUsernameChange = this.handleUsernameChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleUsernameChange(event: any){
    this.setState({
      username: event.target.value
    });    
  };

  handlePasswordChange(event: any){
    this.setState({
      password: event.target.value
    });    
  };

  handleSubmit(event : any){
    event.preventDefault();
    if(Utils.validateLogin(this.state.username, this.state.password)){
       console.log("Registering can be done");
    }else{
       console.log("You cannot login!!!")
    }
  }

  render()
  {  
    return (
      <div className='wrapper'>
        <div className='form-wrapper'>
          <h2>Login</h2>
          <form onSubmit={this.handleSubmit} noValidate >
            <TextField value = 'Username' error = '' type = 'text' onChange = {this.handleUsernameChange}></TextField>
            <TextField value = 'Password' error = '' type = 'password' onChange = {this.handlePasswordChange}></TextField>            
            <div className='submit'>
              <button>Login</button>
            </div>
            <Button component={Link} to="/SignUp">Or click here to sign up</Button>
          </form>
        </div>
      </div>
    ); 
  }
  
}

export default Login;