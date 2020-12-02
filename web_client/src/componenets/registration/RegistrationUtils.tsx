export enum RegistrationEnum {
    email = "Email",
    password = "Password"
}

export default class Utils {

    static checkEmail(email: String)
    {
        //Check also for existance in DB
        return email.length < 1 ? 'email must not be empty!': '';
    }

    static checkPassword(password: String)
    {
        return password.length < 6 ? 'Password must be 6 characters long!': '';
    }

}