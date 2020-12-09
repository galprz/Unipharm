import React from "react";

interface TextFieldProps {
    value: string;
    error: string;
    type: string
    class_name: string
    onChange: (event: any) => void;
}

export class TextField extends React.Component<TextFieldProps>{

    render()
    {
        return(
            <div className={this.props.class_name}>
                  <label htmlFor={this.props.value}>{this.props.value}</label>
                  <input type={this.props.type} name={this.props.value} onChange= {this.props.onChange}/>
                  {this.props.error.length > 0 &&  <span style={{color: "red"}}>{this.props.error}</span>}
            </div>
        );
    }
}