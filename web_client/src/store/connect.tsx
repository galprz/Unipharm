import React from "react";
import { Connect } from "redux-zero/react";

export default function mapActionsAndProps(actions = {}, state = {}): any {
    return (Child: React.ElementType) => (props: {}) => (
      <Connect mapToProps={() => ({ state })} actions={actions}>
        {(mappedProps: {}) => <Child {...mappedProps} {...props} />}
      </Connect>
    )
}