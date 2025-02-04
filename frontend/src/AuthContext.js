import {useContext,createContext,useEffect,useState} from "react";
import { createUserWithEmailAndPassword,signInWithEmailAndPassword,signOut,onAuthStateChanged } from "firebase/auth";
import {auth,db} from "./firebase";
import { setDoc, doc, getDoc } from "firebase/firestore";
import axios from "axios";


const AuthContext = createContext();

export function AuthProvider({children}){

const [user,setUser] = useState(null);
const [loading, setLoading] = useState(true);
const [userId, setUserId] = useState(null);


function signUp(email,password){
    return createUserWithEmailAndPassword(auth,email,password)
}

function logIn(email,password){
    return signInWithEmailAndPassword(auth,email,password)
}   

function logOut(){
    return signOut(auth);
}

// Kullanıcı profil bilgilerini kaydetme
// async function saveUserProfile(userId, profileData) {

//     try{
//         await setDoc(doc(db, 'users', userId), profileData);
//     } catch(error){
//         console.error("Account creation error:", error);
//     }

    
// }
  
  // Kullanıcı profil bilgilerini getirme
async function getUserProfile(userId) {

    try{
        const docRef = doc(db, 'users', userId);
        const docSnap = await getDoc(docRef);
        return docSnap.exists() ? docSnap.data() : null;
    } catch(error){
        console.error("Account creation error:", error);
    }

}

// User ID'yi almak için yeni fonksiyon
async function fetchUserId(email) {
    try {
        const response = await axios.get(`url`);
        setUserId(response.data.user_id);
        return response.data.user_id;
    } catch (error) {
        console.error("Error fetching User ID:", error);
        return null;
    }
}

useEffect(() => {
    const unsubscribe = onAuthStateChanged(auth, async (currentuser) => {
        console.log("Auth", currentuser);
        setUser(currentuser);
        if (currentuser?.email) {
            await fetchUserId(currentuser.email);
        }
        setLoading(false);
    });

    return () => {
        unsubscribe();
    };
}, []);


return <AuthContext.Provider value={{signUp,logIn,logOut,user,userId,getUserProfile,loading,fetchUserId}}>
    {!loading ? children : <div>Yükleniyor...</div>}
    </AuthContext.Provider>
}

export default AuthContext;
