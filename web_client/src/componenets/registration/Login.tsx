import React from 'react';
import '../../../src/Style.css';
import './RegistrationStyle.css';
import { TextField } from "../common/TextField";
import Utils, { RegistrationEnum } from './RegistrationUtils';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';

interface LoginState {
  email : string,
  password : string
};

export class Login extends React.Component<any, LoginState>{

  constructor(props: any){
    super(props);
    const initialState = {
      email : '',
      password : '',
    }
    this.state = initialState;
    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleSubmit = this.handleSubmit.bind(this);
  }

  handleEmailChange(event: any){
    this.setState({
      email: event.target.value
    });    
  };

  handlePasswordChange(event: any){
    this.setState({
      password: event.target.value
    });    
  };

  handleSubmit(event : any){
    event.preventDefault();
    if(Utils.validateLogin(this.state.email, this.state.password)){
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
            <TextField value = {RegistrationEnum.email} error = '' type = 'text' onChange = {this.handleEmailChange}></TextField>
            <TextField value = {RegistrationEnum.password} error = '' type = 'password' onChange = {this.handlePasswordChange}></TextField>            
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