import React from "react";
import { useNavigate, useParams, useLocation } from "react-router-dom";

// Mimic `withRouter` functionality for class components
export function withRouter(Component) {
  return (props) => {
    const params = useParams();
    const navigate = useNavigate();
    const location = useLocation();
    return <Component {...props} params={params} navigate={navigate} location={location} />;
  };
}
