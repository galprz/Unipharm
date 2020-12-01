import React from "react";
import '../../../src/Style.css';
import './RegistrationStyle.css';
import { TextField } from "../common/TextField";
import Utils from './RegistrationUtils';
import { Link } from 'react-router-dom';
import Button from '@material-ui/core/Button';

enum SignUpEnum {
   username = "Username",
   password = "Password"
}

interface SignUpState {
    username : string,
    password : string,
    errors : {
       username :  string,
       password : string
    }
 }

export class SignUp extends React.Component<any, SignUpState>{
   constructor(props: any) {
      super(props);
      const initialState = {
         username : '',
         password : '',
         errors : {
           username : '',
           password : ''
         } 
       }
       this.state = initialState;
       this.handleChange = this.handleChange.bind(this);
       this.handleSubmit = this.handleSubmit.bind(this);
   }

   handleChange(event : any){
      event.preventDefault();
      const { name, value } = event.target;
      let error;
      switch (name) {
        case SignUpEnum.username:
           error = Utils.checkSignUpUserName(value);
           console.log("Username Error: " + error);
           this.setState({ 
            errors: 
            {
               username: error,
               password: this.state.errors.password
            }
            });
           break;
        case SignUpEnum.password:
           error = Utils.checkSignUpPassword(value);
           console.log("Password Error: " + error);
           this.setState({ 
            errors: 
            {
               username: this.state.errors.username,
               password: error
            }
            });
           break;
        default:
          break;
      }
    }

   handleSubmit(event : any){
      event.preventDefault();
      let validity = true;
      Object.values(this.state.errors).forEach(
         (val) => val.length > 0 && (validity = false)
      );
      if(validity === true){
         console.log("Registering can be done");
      }else{
         console.log("You cannot be registered!!!")
      }
   }

    render() { 
      const {errors} = this.state 
      return (
      <div className='wrapper'>
         <div className='form-wrapper'>
            <h2>Sign Up</h2>
            <form onSubmit={this.handleSubmit} noValidate >
               <TextField value = {SignUpEnum.username} error = {errors.username} type = 'text' onChange = {this.handleChange}></TextField>
               <TextField value = {SignUpEnum.password} error = {errors.password} type = 'password' onChange = {this.handleChange}></TextField>            
               <div className='submit'>
                  <button>Register</button>
               </div>
               <Button component={Link} to="/Login">Go back to login</Button>
            </form>
         </div>
      </div>
  );
    }
}