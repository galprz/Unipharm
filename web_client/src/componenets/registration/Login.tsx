import React from 'react';
import './RegistrationStyle.css';

interface LoginProps {
  name?: any;
  value?: any;
};

interface LoginState {
  username : string,
  password : string,
  errors : {
    username :  string,
    password : string
  }
};

class Login extends React.Component<LoginProps, LoginState>{

  handleSubmit(event : any){
    event.preventDefault();
    if(this.state.username === 'admin' && this.state.password === 'password'){
       console.log("Registering can be done");
    }else{
       console.log("You cannot be registered!!!")
    }
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

    constructor(props: LoginProps){
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
      this.handleSubmit = this.handleSubmit.bind(this);
    }

    render()
    {
      const {errors} = this.state   
      return (
      <div className='wrapper'>
          <div className='form-wrapper'>
          <h2>Login</h2>
          <form onSubmit={this.handleSubmit} noValidate >
              <div className='fullName'>
                  <label htmlFor="fullName">Full Name</label>
                  <input type='text' name='fullName' onChange={this.handleUsernameChange}/>
                  {errors.username.length > 0 &&  <span style={{color: "red"}}>{errors.username}</span>}
  </div>
              <div className='password'>
                  <label htmlFor="password">Password</label>
                  <input type='password' name='password' onChange={this.handlePasswordChange}/>
                  {errors.password.length > 0 &&  <span style={{color: "red"}}>{errors.password}</span>}
  </div>              
              <div className='submit'>
                  <button>Enter The System</button>
              </div>
          </form>
      </div>
  </div>
  ); 
    }
  
}

export default Login;