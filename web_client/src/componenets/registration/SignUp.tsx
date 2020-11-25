import React from "react";
import '../../../src/Style.css';
import './RegistrationStyle.css';
import { TextField } from "./TextField";
import Utils from './RegistrationUtils';

enum SignUpEnum {
   username = "Username",
   password = "Password"
}

interface SignUpProps {
    name?: any;
    value?: any;
}

interface SignUpState {
    username : string,
    password : string,
    errors : {
       username :  string,
       password : string
    }
 }

export class SignUp extends React.Component<SignUpProps, SignUpState>{
   constructor(props: SignUpProps) {
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
                  <button>Register Me</button>
               </div>
            </form>
         </div>
      </div>
  );
    }
}