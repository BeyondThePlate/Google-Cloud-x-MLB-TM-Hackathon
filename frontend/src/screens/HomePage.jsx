import React, { useState, useEffect } from 'react';
import VideoCard from '../components/VideoCard';
import Header from '../components/Header';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { BookmarkIcon } from '@heroicons/react/24/outline';
import { useContext } from 'react';
import AuthContext from '../AuthContext';

function HomePage() {
  const navigate = useNavigate();
  const { userId } = useContext(AuthContext);
  //const SEARCH_URL = 'SEARCH URL';
  const INITIAL_URL = 'INITIAL_URL';

  //const [searchTerm, setSearchTerm] = useState('');
  //const [searchResults, setSearchResults] = useState([]);
  const [initialData, setInitialData] = useState([]);


  useEffect(() => {
    axios.get(INITIAL_URL)
      .then(response => {
        setInitialData(response.data);
        //setSearchResults(response.data);
        console.log('Initial data loaded:', response.data);
      })
      .catch(error => {
        console.error('Data loading error:', error);
      });
  }, []);


  const handleWatchVideo = (result) => {
    console.log(result, "result");


    navigate('/video', {
      state: {
        video: {
          id: result.play_id,
          title: result.title,
          description: result.description || '',
          views: result.views,
          timestamp: result.created_at,
          src: result.video_url
        }
      }
    });
  };

  const handleSave = async (e, videoId) => {
    e.stopPropagation(); // Video kartına tıklamayı engelle
    
    if (!userId) {
      alert('Please login first');
      return;
    }

    try {
      const response =await axios.post('URL', {
        user_id: userId,
        play_id: videoId
      });
      console.log("response", response);
    } catch (error) {
      console.error('Video save error:', error);
    }
  };

  // const handleSearch = async () => {
  //   console.log("searching");
  //   axios.post(SEARCH_URL, {
  //     query: searchTerm
  //   })
  //   .then(response => {
  //     setSearchResults(response.data);
  //     console.log('Arama sonucu:', response.data);
  //   })
  //   .catch(error => {
  //     console.error('Arama hatası:', error);
  //   });
  // };

  return (
    <div className="min-h-screen bg-white">
      <Header />

      {/* <div className="flex justify-end my-5 px-[10%]">
        <input
          type="text"
          placeholder="search"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-[300px] px-4 py-2.5 border border-gray-300 rounded-full focus:outline-none focus:border-[#001f3f] focus:ring-1 focus:ring-[#001f3f]"
        />
        <button 
          onClick={handleSearch}
          className="ml-2.5 px-5 py-2.5 bg-[#001f3f] text-white rounded-full hover:bg-[#003366] transition-colors duration-200"
        >
          Ara
        </button>
      </div> */}

      <div className="relative">
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 p-5">
          {initialData.map((result, index) => (
            <div 
              key={result.play_id} 
              onClick={() => handleWatchVideo(result)}
              className="relative"
            >
              <BookmarkIcon 
                className="absolute top-2 right-2 w-5 h-5 text-blue-500 cursor-pointer z-10 hover:text-blue-700"
                onClick={(e) => handleSave(e, result.play_id)}
              />
              <VideoCard 
                title={result.title}
                channel={result.channel}
                views={result.views}
                timestamp={result.created_at}
                src={result.video_url}
                category={result.category}
                index={index}
              />
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default HomePage;
