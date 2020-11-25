import React from "react";
import './RegistrationStyle.css';

enum SignUpEnum {
   username = "username",
   password = "password"
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
    handleChange = (event : any) => {
        event.preventDefault();
        const { name, value } = event.target;
        let errors = this.state.errors;
        switch (name) {
          case SignUpEnum.username:
             errors.username = value.length < 5 ? 'Username must be 5 characters long!': '';
             break;
          case SignUpEnum.password:
             errors.password = value.length < 8 ? 'Password must be eight characters long!': '';
             break;
          default:
            break;
        }
      this.setState({ 
         errors: errors,
         //[name]: value
      });
      console.log(this.state.errors);
      }

      handleSubmit(event : any){
        event.preventDefault();
        let validity = true;
        Object.values(this.state.errors).forEach(
          (val) => val.length > 0 && (validity = false)
        );
        if(validity == true){
           console.log("Registering can be done");
        }else{
           console.log("You cannot be registered!!!")
        }
     }

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
   }

    render() {
      const {errors} = this.state   
      return (
      <div className='wrapper'>
          <div className='form-wrapper'>
          <h2>Sign Up</h2>
          <form onSubmit={this.handleSubmit} noValidate >
              <div className='fullName'>
                  <label htmlFor="fullName">Full Name</label>
                  <input type='text' name='fullName' onChange=            {this.handleChange}/>
                  {errors.username.length > 0 &&  <span style={{color: "red"}}>{errors.username}</span>}
  </div>
              <div className='password'>
                  <label htmlFor="password">Password</label>
                  <input type='password' name='password' onChange={this.handleChange}/>
                  {errors.password.length > 0 &&  <span style={{color: "red"}}>{errors.password}</span>}
  </div>              
              <div className='submit'>
                  <button>Register Me</button>
              </div>
          </form>
      </div>
  </div>
  );
    }
}