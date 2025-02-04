import React, { useState, useCallback } from 'react';
import Header from '../components/Header';
import { FaCloudUploadAlt, FaSpinner } from 'react-icons/fa';
import axios from 'axios';
import { useContext } from 'react';
import AuthContext from '../AuthContext';
import { useNavigate } from 'react-router-dom';

// Rastgele string üreten fonksiyon - component dışında tanımlanabilir
const generateRandomString = (length = 8) => {
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  let result = '';
  for (let i = 0; i < length; i++) {
    result += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return result;
};

const UploadVideoPage = () => {

  const { user } = useContext(AuthContext);
  const [videoFile, setVideoFile] = useState(null);
  const [videoPreview, setVideoPreview] = useState(null);
  const [formData, setFormData] = useState({
    user_id: '',
    title: '',
    description: '',
    video_url: '',
    category: '',
    visibility: 'public',
    frame: ''
  });
  const [loading, setLoading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [userId, setUserId] = useState(null);
  const navigate = useNavigate();

  useState(()=> {
    async function fetchUserId() {
    
    const idRequest = await axios.get('URL');
    setUserId(idRequest.data.user_id)
  }
  fetchUserId()
})

  // Butonlar için state
  const [buttons, setButtons] = useState({
    ball_boundary_box: false,
    ball_line_draw: false,
    ball_side_route: false,
    bat_boundary_box: false,
    bat_line_draw: false,
    glove_boundary_box: false,
    glove_line_draw: false,
    pitcher_boundary_box: false,
    pitcher_pose: false,
    catcher_pose: false,
    catcher_boundary_box: false,
    hitter_boundary_box: false,
    hitter_pose: false,
    hitter_3d_pose: false,
    catcher_3d_pose: false,
    pitcher_3d_pose: false,
    pitcher_pose_graph: false,
    hitter_pose_graph: false,
    catcher_pose_graph: false,
    map: false,
    heatmap: false
  });

  const handleFileChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setVideoFile(file);
      setVideoPreview(URL.createObjectURL(file));
    }
  };

  const handleInputChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleButtonClick = useCallback((e, buttonName) => {
    e.preventDefault();
    setButtons(prev => ({
      ...prev,
      [buttonName]: !prev[buttonName]
    }));
  }, []);    


  const uploadFileToSignedUrl = async (file, signedUrl) => {
    try {
      const response = await axios.put(signedUrl, file, {
        headers: {
          "Content-Type": "application/octet-stream",
        },
      });     
  
      if (response.status === 200 || response.status === 201) {
        console.log("File uploaded successfully:", file.name);
      } else {
        console.error("Upload error:", response.status, response.data);
      }
    } catch (error) {
      console.error("An error occurred:", error);
    }
  };



  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!formData.frame || isNaN(formData.frame) || formData.frame <= 0) {
      alert("Please enter a valid frame count!");
      return;
    }

    setLoading(true);

    try {
      // Generate file name -> Dosya adını oluştur
      const fileExtension = videoFile.name.split('.').pop();
      const randomFileName = `${generateRandomString()}.${fileExtension}`;

      // Get signed URL and upload video -> Signed URL'yi al ve video yükleme işlemleri
      const signedUrlResponse = await axios.post('URL', {
        filename: randomFileName
      });
      
      const signedUrl = signedUrlResponse.data.url;
      await uploadFileToSignedUrl(videoFile, signedUrl);

      // Save video information to database -> Video bilgilerini veritabanına kaydet
      const videoData = {
        play_id: randomFileName,
        user_id: userId,
        title: formData.title,
        description: formData.description,
        video_url: `URL`,
        category: formData.category,
        visibility: formData.visibility
      };

      const createVideoResponse = await axios.post('URL', videoData);

      if (createVideoResponse.status === 200) {
        alert("Video uploaded successfully");
        // Video analysis için vm_stimulate'e istek at
        const analysisData = {
          frame: parseInt(formData.frame),
          fileName: randomFileName,
          play_id: randomFileName,
          ball_box: buttons.ball_boundary_box,
          ball_line: buttons.ball_line_draw,
          ball_side: buttons.ball_side_route,
          bat_box: buttons.bat_boundary_box,
          bat_line: buttons.bat_line_draw,
          glove_box: buttons.glove_boundary_box,
          glove_line: buttons.glove_line_draw,
          pitcher_box: buttons.pitcher_boundary_box,
          pitcher_pose: buttons.pitcher_pose,
          catcher_box: buttons.catcher_boundary_box,
          catcher_pose: buttons.catcher_pose,
          hitter_box: buttons.hitter_boundary_box,
          hitter_pose: buttons.hitter_pose,
          hitter_3d: buttons.hitter_3d_pose,
          catcher_3d: buttons.catcher_3d_pose,
          pitcher_3d: buttons.pitcher_3d_pose,
          pitcher_graph: buttons.pitcher_pose_graph,
          hitter_graph: buttons.hitter_pose_graph,
          catcher_graph: buttons.catcher_pose_graph,
          map_button: buttons.map,
          heatmap: buttons.heatmap
        };
        console.log("Analysis Data : ", analysisData);

        const analysisResponse = await axios.post('URL', analysisData);
        
        if (analysisResponse.status === 200) {
          console.log('Video analysis started:', analysisResponse.data);
          alert("Video uploaded successfully and analysis started!");
          navigate('/mymedia');
        }
      }

    } catch (error) {
      console.error('Process error:', error);
      alert("An error occurred: " + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-white">
      <Header />
      
      <div className="max-w-4xl mx-auto px-4 py-8">
        <h1 className="text-2xl font-bold text-gray-900 mb-8">Upload Video</h1>

        <form onSubmit={handleSubmit} className="space-y-8">
          {/* Video Yükleme Alanı */}
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8">
            {!videoPreview ? (
              <div className="text-center">
                <FaCloudUploadAlt className="mx-auto h-12 w-12 text-gray-400" />
                <div className="mt-4">
                  <label htmlFor="video-upload" className="cursor-pointer">
                    <span className="mt-2 block text-sm font-medium text-gray-600">
                      Drag and drop your video or select
                    </span>
                    <input
                      id="video-upload"
                      type="file"
                      className="hidden"
                      accept="video/*"
                      onChange={handleFileChange}
                    />
                    <span className="mt-2 block text-sm text-[#001f3f] hover:text-[#003366]">
                      or browse
                    </span>
                  </label>
                </div>
              </div>
            ) : (
              <div className="relative">
                <video
                  src={videoPreview}
                  className="w-full aspect-video rounded"
                  controls
                />
                <button
                  onClick={() => {
                    setVideoFile(null);
                    setVideoPreview(null);
                  }}
                  className="absolute top-2 right-2 bg-red-500 text-white p-2 rounded-full"
                >
                  ✕
                </button>
              </div>
            )}
          </div>

          {/* Video Detayları */}
          <div className="space-y-6 bg-gray-50 p-6 rounded-lg">
            <div>
              <label className="block text-sm font-medium text-gray-700">
                Frame Count
              </label>
              <input
                type="number"
                name="frame"
                value={formData.frame}
                onChange={handleInputChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2.5"
                required
                min="1"
                placeholder="Enter frame count (1 seconds = 30 frames)"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Video Title
              </label>
              <input
                type="text"
                name="title"
                value={formData.title}
                onChange={handleInputChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2.5"
                required
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Description
              </label>
              <textarea
                name="description"
                value={formData.description}
                onChange={handleInputChange}
                rows="4"
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2.5"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Category
              </label>
              <select
                name="category"
                value={formData.category}
                onChange={handleInputChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2.5"
              >
                <option value="">Select Category</option>
                <option value="highlights">Match Highlights</option>
                <option value="analysis">Analysis</option>
                <option value="tutorial">Tutorial</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700">
                Visibility
              </label>
              <select
                name="visibility"
                value={formData.visibility}
                onChange={handleInputChange}
                className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2.5"
              >
                <option value="public">Public</option>
                <option value="private">Private</option>
              </select>
            </div>
          </div>

          {/* Analiz Seçenekleri */}
          <div className="mt-8">
            <h2 className="text-xl font-bold text-gray-900 mb-4">Analysis Options</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              {Object.entries(buttons).map(([key, value]) => (
                <button
                  key={key}
                  type="button"
                  onClick={(e) => handleButtonClick(e, key)}
                  className={`p-3 rounded-lg text-sm font-medium transition-colors duration-200 ${
                    value 
                      ? 'bg-[#001f3f] text-white' 
                      : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                  }`}
                >
                  {key.split('_').map(word => 
                    word.charAt(0).toUpperCase() + word.slice(1)
                  ).join(' ')}
                </button>
              ))}
            </div>
          </div>

          {/* Yükleme Durumu ve Buton */}
          <div className="flex items-center justify-between mt-8">
            {loading && (
              <div className="flex items-center space-x-2">
                <FaSpinner className="animate-spin text-[#001f3f]" />
                <span className="text-sm text-gray-600">
                  Uploading... {progress}%
                </span>
              </div>
            )}
            <button
              type="submit"
              disabled={!videoFile || loading}
              className={`px-6 py-2.5 bg-[#001f3f] text-white rounded-md hover:bg-[#003366] transition-colors duration-200 ${
                (!videoFile || loading) && 'opacity-50 cursor-not-allowed'
              }`}
            >
              Upload Video
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default UploadVideoPage;
