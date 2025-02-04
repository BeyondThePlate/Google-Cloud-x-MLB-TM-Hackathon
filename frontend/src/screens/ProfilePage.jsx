import React, { useState, useContext } from 'react'
import Header from '../components/Header'
import AuthContext from '../AuthContext'
import axios from 'axios'

const ProfilePage = () => {
  const {user} = useContext(AuthContext)
  const [isEditing, setIsEditing] = useState(false);
  const [userId, setUserId] = useState(null);
  const [preferences, setPreferences] = useState({
    favoriteTeam: '',
    favoritePlayer: '',
    favoritePart: '',
    watchingExperience: '',
    preferredPosition: '',
    dreamStadium: '',
    userName: '',
    email: '',
    country: '',
    firstName: '',
    lastName: ''
  })

  useState(()=> {
    async function getUserId() {
      const idRequest = await axios.get(`URL`);
      setUserId(idRequest.data.user_id)

      // Add user information to preferences
      setPreferences(prev => ({
        ...prev,
        firstName: idRequest.data.first_name || '',
        lastName: idRequest.data.last_name || '',
        userName: idRequest.data.username || '',
        email: idRequest.data.email || '',
        country: idRequest.data.country || ''
      }));

      if (idRequest.data.user_id) {
        try {
          const response = await axios.get('URL');
          if (response.data.length > 0) {
            const userPrefs = response.data[0];
            setPreferences(prev => ({
              ...prev,
              favoriteTeam: userPrefs.favorite_team || '',
              favoritePlayer: userPrefs.favorite_player || '',
              favoritePart: userPrefs.favorite_part || '',
              watchingExperience: userPrefs.watching_experience || '',
              preferredPosition: userPrefs.preferred_position || '',
              dreamStadium: userPrefs.dream_stadium || ''
            }));
          }
        } catch (error) {
          console.error('Error fetching preferences:', error);
        }
      }
    }
    getUserId()
  },[])

  const {logOut} = useContext(AuthContext)

  const handleChange = (e) => {
    setPreferences({
      ...preferences,
      [e.target.name]: e.target.value
    })
  }

  const handleSave = async (e) => {
    e.preventDefault();
    console.log("Button clicked");
    
    if (!user || !user.email) {
      console.error('User information not found');
      console.log('User:', user);
      return;
    }

    console.log('User email:', user.email);
    console.log('Current preferences:', preferences);

    try {
      console.log('Starting API request...');
      try {
        // Get isteği
        //console.log('Get isteği URL:', `URL`);


        console.log('User ID:', userId);
        const checkPreferences = await axios.get('URL');
        console.log('Get request response:', checkPreferences.data[0]);


        if (checkPreferences.data.length > 0 ) {
          console.log('Will update ID:', checkPreferences.data[0].preference_id);
          // Update isteği
          const updateResponse = await axios.put('URL', {
            favorite_team: preferences.favoriteTeam,
            favorite_player: preferences.favoritePlayer,
            favorite_part: preferences.favoritePart,
            watching_experience: preferences.watchingExperience,
            preferred_position: preferences.preferredPosition,
            dream_stadium: preferences.dreamStadium
          });
          console.log('Update response:', updateResponse.data);
          console.log('Preferences updated successfully');
        } else {
          console.log('Creating new preference...');
          // Create isteği
          const createResponse = await axios.post('URL', {
            user_id: userId,
            favorite_team: preferences.favoriteTeam,
            favorite_player: preferences.favoritePlayer,
            favorite_part: preferences.favoritePart,
            watching_experience: preferences.watchingExperience,
            preferred_position: preferences.preferredPosition,
            dream_stadium: preferences.dreamStadium
          });
          console.log('Create response:', createResponse.data);
          console.log('New preferences created');
        }


      } catch (error) {
        console.log('Error caught:', error.response?.status);
        
      }

      setIsEditing(false);
      alert('Changes saved successfully!');
    } catch (error) {
      console.error('An error occurred during the process:', error);
      console.error('Error details:', error.response?.data);
      alert('An error occurred while saving changes. Please try again.');
    }
  };

  return (
    <>
      <Header/>
      <div className="flex justify-between items-center p-4 bg-white shadow-sm">
        <button 
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 transition-colors"
          onClick={() => {
            logOut()
            console.log('Logout clicked')
          }}
        >
          Logout
        </button>
      </div>
      <div className="min-h-screen p-8">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-2xl font-bold">PROFILE PAGE</h1>
          {!isEditing && (
            <button 
              onClick={() => setIsEditing(true)}
              className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
            >
              Make Changes
            </button>
          )}
        </div>
        
        <div className="bg-gray-100 rounded-lg p-6 mb-6">
          <h2 className="text-xl text-gray-600 mb-6">Account Information</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="block text-gray-600 mb-2">First Name</label>
              <input 
                type="text"
                name="firstName"
                value={preferences.firstName}
                className="w-full p-2 border rounded bg-gray-50"
                onChange={handleChange}
                disabled={true}
              />
            </div>
            <div>
              <label className="block text-gray-600 mb-2">Last Name</label>
              <input 
                type="text"
                name="lastName"
                value={preferences.lastName}
                className="w-full p-2 border rounded bg-gray-50"
                onChange={handleChange}
                disabled={true}
              />
            </div>
          </div>

          <div className="grid grid-cols-1 gap-4">
            <div>
              <label className="block text-gray-600 mb-2">Username</label>
              <input 
                type="text"
                name="userName"
                value={preferences.userName}
                className="w-full p-2 border rounded bg-gray-50"
                onChange={handleChange}
                disabled={true}
              />
            </div>
            <div>
              <label className="block text-gray-600 mb-2">Email</label>
              <input 
                type="email"
                name="email"
                value={preferences.email}
                className="w-full p-2 border rounded bg-gray-50"
                onChange={handleChange}
                disabled={true}
              />
            </div>
            <div>
              <label className="block text-gray-600 mb-2">Country</label>
              <input 
                type="text"
                name="country"
                value={preferences.country}
                className="w-full p-2 border rounded bg-gray-50"
                onChange={handleChange}
                disabled={true}
              />
            </div>
          </div>
        </div>
        
        <div className="bg-gray-100 rounded-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-xl text-gray-600">Baseball Preferences</h2>
            {isEditing && (
              <button 
                onClick={(e) => handleSave(e)}
                className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 transition-colors"
              >
                Save Changes
              </button>
            )}
          </div>
          
          <div className="grid grid-cols-1 gap-4">
            <div>
              <label className="block text-gray-600 mb-2">Favorite Team</label>
              <input 
                type="text"
                name="favoriteTeam"
                value={preferences.favoriteTeam}
                className={`w-full p-2 border rounded ${!isEditing && 'bg-gray-50'}`}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
            
            <div>
              <label className="block text-gray-600 mb-2">Favorite Player</label>
              <input 
                type="text"
                name="favoritePlayer"
                value={preferences.favoritePlayer}
                className={`w-full p-2 border rounded ${!isEditing && 'bg-gray-50'}`}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
            
            <div>
              <label className="block text-gray-600 mb-2">What Do You Love Most About Baseball?</label>
              <textarea 
                name="favoritePart"
                value={preferences.favoritePart}
                className={`w-full p-2 border rounded ${!isEditing && 'bg-gray-50'}`}
                rows="3"
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
            
            <div>
              <label className="block text-gray-600 mb-2">How Long Have You Been Watching Baseball?</label>
              <input 
                type="text"
                name="watchingExperience"
                value={preferences.watchingExperience}
                className={`w-full p-2 border rounded ${!isEditing && 'bg-gray-50'}`}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
            
            <div>
              <label className="block text-gray-600 mb-2">Favorite Playing Position</label>
              <input 
                type="text"
                name="preferredPosition"
                value={preferences.preferredPosition}
                className={`w-full p-2 border rounded ${!isEditing && 'bg-gray-50'}`}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
            
            <div>
              <label className="block text-gray-600 mb-2">Dream Stadium to Watch a Game</label>
              <input 
                type="text"
                name="dreamStadium"
                value={preferences.dreamStadium}
                className={`w-full p-2 border rounded ${!isEditing && 'bg-gray-50'}`}
                onChange={handleChange}
                disabled={!isEditing}
              />
            </div>
          </div>
        </div>
      </div>
    </>
  )
}

export default ProfilePage
