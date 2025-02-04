import React from 'react';
import Header from '../components//Header';
import { useLocation } from 'react-router-dom';
import axios from 'axios';
import { useEffect, useState } from 'react';

const VideoPage = () => {
  const location = useLocation();
  const video = location.state.video;
  console.log(video);

  const [entities, setEntities] = useState('');


  const ENTITY_LINK = 'URL' + video.id;

  useEffect(() => {
    console.log("Video id : ", video.id);
    //video.src = 'URL';
    axios.get(ENTITY_LINK)
      .then(response => {
        console.log("New data received: ", response.data);
        setEntities(response.data);
      })
      .catch(error => {
        console.error('Data loading error:', error);
      });
  }, []);

  useEffect(() => {
    console.log("Entities : ", entities);
  }, [entities]);


  return (
    <>
      <Header />
      
      <div className="flex p-5 gap-5">
        <div className="flex-[0_0_70%] overflow-y-auto h-[calc(100vh-80px)]">
          <div className="w-full mb-5 sticky top-0 bg-white">
            <video 
              src={video?.src} 
              controls 
              autoPlay 
              loop
              className="w-full aspect-video"
            />
          </div>

          <div className="mb-5">
            <h1 className="text-2xl font-bold mb-3">{video?.title}</h1>
            <p className="mb-4">{video?.description}</p>
            <div className="flex gap-4 text-sm text-gray-600">
              <span>{video?.views} views</span>
              <span>•</span>
              <span>{video?.timestamp}</span>
            </div>
          </div>
        </div>
        
        <div className="flex-[0_0_30%] overflow-y-auto h-[calc(100vh-80px)] bg-gray-50">
          <div className="flex flex-col gap-4 p-5">
          {entities?.out_out !== 'None' && (
              <div className="w-full">
                <p className="text-sm font-semibold mb-2">Out Analysis</p>
                <video 
                  src={entities?.out_out} 
                  controls 
                  autoPlay
                  loop
                  className="w-full aspect-video mb-4"
                />
              </div>
            )}
            {entities?.heatmap_out !== 'None' && (
              <div className="w-full">
                <p className="text-sm font-semibold mb-2">Heatmap</p>
                <video 
                  src={entities?.heatmap_out} 
                  controls 
                  loop
                  autoPlay
                  className="w-full aspect-video mb-4"
                />
              </div>
            )}
            {entities?.map_out !== 'None' && (
              <div className="w-full">
                <p className="text-sm font-semibold mb-2">Movement Map</p>
                <video 
                  src={entities?.map_out} 
                  controls 
                  loop
                  autoPlay
                  className="w-full aspect-video mb-4"
                />
              </div>
            )}
            {entities?.pose_pitcher_graph_out !== 'None' && (
              <div className="w-full">
                <p className="text-sm font-semibold mb-2">Pitcher Pose Analysis (Graph)</p>
                <video 
                  src={entities?.pose_pitcher_graph_out} 
                  controls 
                  autoPlay
                  loop
                  className="w-full aspect-video mb-4"
                />
              </div>
            )}
            {entities?.pose_hitter_graph_out !== 'None' && (
              <div className="w-full">
                <p className="text-sm font-semibold mb-2">Hitter Pose Analysis (Graph)</p>
                <video 
                  src={entities?.pose_hitter_graph_out} 
                  controls 
                  autoPlay
                  loop
                  className="w-full aspect-video mb-4"
                />
              </div>
            )}
            {entities?.pose_catcher_graph_out !== 'None' && (
              <div className="w-full">
                <p className="text-sm font-semibold mb-2">Catcher Pose Analysis (Graph)</p>
                <video 
                  src={entities?.pose_catcher_graph_out} 
                  controls 
                  autoPlay
                  loop
                  className="w-full aspect-video mb-4"
                />
              </div>
            )}
           
            {entities?.pose_pitcher_3d_out !== 'None' && (
              <div className="w-full">
                <p className="text-sm font-semibold mb-2">Pitcher Pose Analysis (3D)</p>
                <video 
                  src={entities?.pose_pitcher_3d_out} 
                  controls 
                  autoPlay
                  loop
                  className="w-full aspect-video mb-4"
                />
              </div>
            )}
            {entities?.pose_hitter_3d_out !== 'None' && (
              <div className="w-full">
                <p className="text-sm font-semibold mb-2">Hitter Pose Analysis (3D)</p>
                <video 
                  src={entities?.pose_hitter_3d_out} 
                  controls 
                  autoPlay
                  loop
                  className="w-full aspect-video mb-4"
                />
              </div>
            )}
            {entities?.pose_catcher_3d_out !== 'None' && (
              <div className="w-full">
                <p className="text-sm font-semibold mb-2">Catcher Pose Analysis (3D)</p>
                <video 
                  src={entities?.pose_catcher_3d_out} 
                  controls 
                  autoPlay
                  loop
                  className="w-full aspect-video mb-4"
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  );
};

export default VideoPage;
