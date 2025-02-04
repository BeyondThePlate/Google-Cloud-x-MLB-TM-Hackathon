import React, { useState, useEffect, useCallback } from 'react';
import VideoCard from '../components/VideoCard';
import Header from '../components/Header';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../AuthContext';
import { useContext } from 'react';
import { TrashIcon } from '@heroicons/react/24/outline';

function MyMediaPage() {
  const navigate = useNavigate();
  const { userId } = useContext(AuthContext);
  const [activeTab, setActiveTab] = useState('saved'); // 'saved' or 'my'
  const [videos, setVideos] = useState([]);
  const [loading, setLoading] = useState(false);
  const [unavailableVideos, setUnavailableVideos] = useState({});

  const checkVideoAvailability = async (videoId) => {
    try {
      const response = await axios.get('URL'+ videoId);
      console.log("Link", `URL`);
      console.log("Get Video Entity Response", response);
      return true;
    } catch (error) {
      console.log("Error", error);
      if (error.response?.status === 404) {
        return false;
      }
      return true; // Diğer hatalarda varsayılan olarak video var sayılsın
    }
  };

  const fetchVideos = async () => {
    if (!userId) return;

    console.log("userId", userId);
    
    const SAVED_VIDEOS_URL = 'SAVED_VIDEOS_URL';
    const MY_VIDEOS_URL = 'MY_VIDEOS_URL';
    
    setLoading(true);
    try {
      const url = activeTab === 'saved' ? SAVED_VIDEOS_URL : MY_VIDEOS_URL;
      const response = await axios.get(url);
      console.log( activeTab==='saved' ? response.data : "my videos");
      setVideos(response.data || []);

      // Tüm videoların varlığını kontrol et
      const unavailableStatus = {};
      for (const video of response.data || []) {
        console.log("Video Play Id", video.play_id);
        const isAvailable = await checkVideoAvailability(video.play_id);
        if (!isAvailable) {
          unavailableStatus[video.play_id] = true;
        }
      }
      setUnavailableVideos(unavailableStatus);
    } catch (error) {
      console.error('Error loading video:', error);
      setVideos([]);
    } finally {
      setLoading(false);
    }
  };
  
  
  useEffect(() => {
    fetchVideos();
  }, [activeTab, userId]);

  

  const handleWatchVideo = (video) => {
    navigate('/video', {
      state: {
        video: {
          id: video.play_id,
          title: video.title,
          description: video.description || '',
          views: video.views,
          timestamp: video.created_at,
          src: video.video_url
        }
      }
    });
  };

  const handleDelete = async (e, videoId) => {
    e.stopPropagation(); // Video kartına tıklamayı engelle
    
    if (window.confirm('Are you sure you want to delete this video?')) {
      try {
        const response = await axios.delete(`URL`);
        // Videoyu UI'dan kaldır
        console.log("response", response);
        setVideos(prevVideos => prevVideos.filter(video => video.play_id !== videoId));
        alert('Video successfully deleted');
      } catch (error) {
        console.error('Video silme hatası:', error);
      }
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      {/* Tab Navigation */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
        <div className="border-b border-gray-200">
          <nav className="-mb-px flex space-x-8" aria-label="Tabs">
            <button
              onClick={() => setActiveTab('saved')}
              className={`${
                activeTab === 'saved'
                  ? 'border-[#001f3f] text-[#001f3f]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm sm:text-base transition-colors duration-200`}
            >
              Saved Videos
            </button>
            <button
              onClick={() => setActiveTab('my')}
              className={`${
                activeTab === 'my'
                  ? 'border-[#001f3f] text-[#001f3f]'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              } whitespace-nowrap py-4 px-1 border-b-2 font-medium text-sm sm:text-base transition-colors duration-200`}
            >
              My Videos
            </button>
          </nav>
        </div>

        {/* Video Grid */}
        {loading ? (
          <div className="flex justify-center items-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-[#001f3f]"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 py-8">
            {videos.map((video, index) => (
              
              <div 
                key={video?.play_id} 
                onClick={() => !unavailableVideos[video.play_id] && handleWatchVideo(video)}
                className={`flex flex-col w-full mx-auto bg-gray-50 rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 ${!unavailableVideos[video.play_id] ? 'cursor-pointer' : 'cursor-not-allowed opacity-70'} relative`}
              >
                <div className="w-full aspect-video relative">
                  {activeTab === 'saved' && (
                    <TrashIcon 
                      className="absolute bottom-2 right-2 w-5 h-5 text-red-500 cursor-pointer z-10 hover:text-red-700"
                      onClick={(e) => handleDelete(e, video.play_id)}
                    />
                  )}
                  {unavailableVideos[video.play_id] && (
                    <div className="absolute inset-0 flex items-center justify-center bg-black bg-opacity-50 z-20">
                      <p className="text-white font-medium">Video is no longer available</p>
                    </div>
                  )}
                  <VideoCard 
                    title={video.title}
                    channel={video.channel}
                    views={video.views}
                    timestamp={activeTab === 'saved' ? video.saved_at : video.created_at}
                    src={video.video_url}
                    category={video.category} 
                    index={index}
                  /> 
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Empty State */}
        {!loading && videos.length === 0 && (
          <div className="flex flex-col items-center justify-center h-64">
            <p className="text-gray-500 text-lg">
              {activeTab === 'saved' 
                ? 'No saved videos yet.' 
                : 'You haven\'t uploaded any videos yet.'}
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default MyMediaPage;