import React, { useState, useContext } from 'react'
import Header from '../components/Header'
import AuthContext from '../AuthContext'
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

const SignupPage = () => {
  const { signUp } = useContext(AuthContext)
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    userName: '',
    email: '',
    password: '',
    country: ''
  })
  const [errors, setErrors] = useState({})

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required'
    }
    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required'
    }
    if (!formData.userName.trim()) {
      newErrors.userName = 'Username is required'
    }
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    }
    if (!formData.password.trim()) {
      newErrors.password = 'Password is required'
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters'
    }
    if (!formData.country.trim()) {
      newErrors.country = 'Country is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) {
      return
    }

    setLoading(true)
    console.log("Form gönderiliyor...")

    try {
      // Firebase kaydı
      console.log("Firebase kaydı başlıyor...");
      const userCredential = await signUp(formData.email, formData.password)
      const user = userCredential.user;
      console.log("Firebase kaydı başarılı:", user);
      
      // API'ye gönderilecek kullanıcı verilerini hazırla
      const userData = { 
        user_id: user.uid,
        first_name: formData.firstName,
        last_name: formData.lastName,
        username: formData.userName,
        email: formData.email,
        country: formData.country
      };
      console.log("Gönderilecek veriler:", userData);

      // Axios ile API'ye POST isteği gönder
      console.log("API isteği gönderiliyor...");
      const response = await axios.post('URL', userData, {
        headers: {
          'Content-Type': 'application/json' 
        }
      });
      console.log('API yanıtı:', response.data);

      // Profil kaydetme
      console.log("Profil kaydediliyor...");
      // await saveUserProfile(user.uid, userData)
      console.log("İşlem tamamlandı, anasayfaya yönlendiriliyor...");
      
      navigate("/")
    } catch (error) {
      let errorMessage = "An error occurred. Please try again."
      
      if (error.response) {
        // Server error response
        console.error("Server error:", error.response.data);
        console.error("Status code:", error.response.status);
        errorMessage = error.response.data.message || errorMessage;
      } else if (error.request) {
        // Request made but no response received
        console.error("Could not reach server:", error.request);
        errorMessage = "Could not reach server. Please check your internet connection.";
      } else {
        // Error in request setup
        console.error("Request error:", error.message);
      }
      
      alert(errorMessage);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Header/>     
      <div className="min-h-screen p-8">
        <h1 className="text-2xl font-bold mb-8">CREATE ACCOUNT</h1>
        
        <form onSubmit={handleSubmit} className="bg-gray-100 rounded-lg p-6 mb-8">
          <div className="mb-6">
            <h2 className="text-xl text-gray-600 mb-4">Account Information</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-gray-600 mb-2">First Name</label>
                <input 
                  type="text"
                  name="firstName"
                  className={`w-full p-2 border rounded ${errors.firstName ? 'border-red-500' : ''}`}
                  onChange={handleChange}
                />
                {errors.firstName && <p className="text-red-500 text-sm mt-1">{errors.firstName}</p>}
              </div>
              <div>
                <label className="block text-gray-600 mb-2">Last Name</label>
                <input 
                  type="text"
                  name="lastName"
                  className={`w-full p-2 border rounded ${errors.lastName ? 'border-red-500' : ''}`}
                  onChange={handleChange}
                />
                {errors.lastName && <p className="text-red-500 text-sm mt-1">{errors.lastName}</p>}
              </div>
            </div>
          </div>

          <div className="mb-6">
            <h2 className="text-xl text-gray-600 mb-4">LOGIN & SECURITY</h2>
            <div className="grid grid-cols-1 gap-4">
              <div>
                <label className="block text-gray-600 mb-2">Username</label>
                <input 
                  type="text"
                  name="userName"
                  className={`w-full p-2 border rounded ${errors.userName ? 'border-red-500' : ''}`}
                  onChange={handleChange}
                />
                {errors.userName && <p className="text-red-500 text-sm mt-1">{errors.userName}</p>}
              </div>
              <div>
                <label className="block text-gray-600 mb-2">Email</label>
                <input 
                  type="email"
                  name="email"
                  className={`w-full p-2 border rounded ${errors.email ? 'border-red-500' : ''}`}
                  onChange={handleChange}
                />
                {errors.email && <p className="text-red-500 text-sm mt-1">{errors.email}</p>}
              </div>
              <div>
                <label className="block text-gray-600 mb-2">Password</label>
                <input 
                  type="password"
                  name="password"
                  className={`w-full p-2 border rounded ${errors.password ? 'border-red-500' : ''}`}
                  onChange={handleChange}
                />
                {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password}</p>}
              </div>
              <div>
                <label className="block text-gray-600 mb-2">Country</label>
                <input 
                  type="text"
                  name="country"
                  className={`w-full p-2 border rounded ${errors.country ? 'border-red-500' : ''}`}
                  onChange={handleChange}
                />
                {errors.country && <p className="text-red-500 text-sm mt-1">{errors.country}</p>}
              </div>
            </div>
          </div>

          <div className="mt-6">
            <button 
              type="submit"
              disabled={loading}
              className={`w-full py-2 px-4 rounded transition duration-200 
                ${loading 
                  ? 'bg-gray-400 cursor-not-allowed' 
                  : 'bg-blue-600 hover:bg-blue-700 text-white'}`}
            >
              {loading ? 'Creating Account...' : 'Create Account'}
            </button>
          </div>
        </form>
      </div>
    </>
  )
}

export default SignupPage
