import React from 'react';
import '../../../src/Style.css';
import './RegistrationStyle.css';
import { TextField } from "../common/TextField";
import Utils, { RegistrationEnum } from './RegistrationUtils';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';
import {authClient} from '../../api/init-firebase';
interface LoginState {
  email : string,
  password : string,
  email_error : string,
  password_error : string
};

export class Login extends React.Component<any, LoginState>{

  constructor(props: {}){
    super(props);
    const initialState = {
      email : '',
      password : '',
      email_error : '',
      password_error : ''
    }
    this.state = initialState;
    this.handleEmailChange = this.handleEmailChange.bind(this);
    this.handlePasswordChange = this.handlePasswordChange.bind(this);
    this.handleLogin = this.handleLogin.bind(this);
  }

  handleEmailChange(event : any){
    const email = event.target.value;
    const email_error = Utils.checkEmail(email);
    this.setState({email, email_error});
  }

  handlePasswordChange(event : any){
    const password = event.target.value;
    const password_error = Utils.checkPassword(password);
    this.setState({password, password_error});
  }

  async handleLogin(event : any){
    event.preventDefault();
    try {
      await authClient.signInWithEmailAndPassword(this.state.email, this.state.password)
      alert("Successfully signed in")
    }
    catch(result) {
      this.setState({email_error : "Couldn't sign in"})
    }
    // TODO: If the sign in was successful open the home screen once we have one
  }

  render()
  {  
    return (
      <div className='wrapper'>
        <div className='form-wrapper'>
          <h2>Login</h2>
          <form onSubmit={this.handleLogin}>
          <TextField value = {RegistrationEnum.email} 
                     error = {this.state.email_error} 
                     type = 'text' 
                     onChange = {this.handleEmailChange} 
                     class_name = "email"></TextField>
          <TextField value = {RegistrationEnum.password} 
                     error = {this.state.password_error} 
                     type = 'password' 
                     onChange = {this.handlePasswordChange} 
                     class_name = "password"></TextField>            
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

