export default class Utils {

    static checkSignUpUserName(username: String)
    {
        //Check also for existance in DB
        return username.length < 5 ? 'Username must be 5 characters long!': '';
    }

    static checkSignUpPassword(password: String)
    {
        return password.length < 8 ? 'Password must be eight characters long!': '';
    }

    static validateLogin(username: String, password: String){
        return true;
    }

}