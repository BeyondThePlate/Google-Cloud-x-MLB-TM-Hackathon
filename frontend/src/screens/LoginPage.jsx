import React, { useState, useContext } from 'react'
import Header from '../components/Header'
import AuthContext from '../AuthContext'
import { useNavigate } from 'react-router-dom';

const LoginPage = () => {
  const { logIn } = useContext(AuthContext)
  const navigate = useNavigate();
  const [loading, setLoading] = useState(false);

  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })

  const [errors, setErrors] = useState({})

  const validateForm = () => {
    const newErrors = {}
    
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required'
    }
    if (!formData.password.trim()) {
      newErrors.password = 'Password is required'
    }

    setErrors(newErrors)
    return Object.keys(newErrors).length === 0
  }

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    if (!validateForm()) {
      return
    }

    setLoading(true)
    try {
      await logIn(formData.email, formData.password)
      console.log("Login successful")
      navigate("/")
    } catch (error) {
      console.error("Login error:", error)
      let errorMessage = "Login failed. Please try again.";
      
      if (error.code === 'auth/user-not-found') {
        errorMessage = "No user found with this email address.";
      } else if (error.code === 'auth/wrong-password') {
        errorMessage = "Incorrect password.";
      } else if (error.code === 'auth/invalid-email') {
        errorMessage = "Invalid email address.";
      } else if (error.code === 'auth/too-many-requests') {
        errorMessage = "Too many failed login attempts. Please try again later.";
      }
      
      alert(errorMessage);
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <Header/>     
      <div className="min-h-screen p-8">
        <h1 className="text-2xl font-bold mb-8">LOGIN</h1>
        
        <form onSubmit={handleSubmit} className="bg-gray-100 rounded-lg p-6 mb-8 max-w-md mx-auto">
          <div className="mb-6">
            <h2 className="text-xl text-gray-600 mb-4">Login Information</h2>
            <div className="grid grid-cols-1 gap-4">
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
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </div>
        </form>
      </div>
    </>
  )
}

export default LoginPage
