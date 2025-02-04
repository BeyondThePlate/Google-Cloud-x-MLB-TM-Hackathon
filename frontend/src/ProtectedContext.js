import { useContext } from "react";
import { Navigate } from "react-router-dom";
import AuthContext from "./AuthContext";

export function ProtectedContext({children}){
    const {user} = useContext(AuthContext)
    if(!user){
        return <Navigate to="/signup" />
    }
    return children;
}

export default ProtectedContext;
