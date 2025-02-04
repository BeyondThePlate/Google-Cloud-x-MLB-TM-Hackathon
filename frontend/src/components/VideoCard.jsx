const formatDate = (timestamp) => {
  const date = new Date(timestamp);
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  
  const day = date.getDate();
  const month = months[date.getMonth()];
  const year = date.getFullYear().toString().substr(-2);
  
  return `${day} ${month} ${year}`;
};

const VideoCard = ({ title, channel, category, views, timestamp, index }) => {
  // Let's import all images statically
  const images = {
    1: require('../assets/baseball_1.png'),
    2: require('../assets/baseball_2.jpg'),
    3: require('../assets/baseball_3.jpg'),
    4: require('../assets/baseball_4.jpg'),
    5: require('../assets/baseball_5.jpg'),
    6: require('../assets/baseball_6.jpg'),
    7: require('../assets/baseball_7.jpg'),
    8: require('../assets/baseball_8.jpg'),
    9: require('../assets/baseball_9.jpg'),
  };

  const imageNumber = (index % 10) + 1;

  return (
    <div className="cursor-pointer transform transition-all duration-200 hover:-translate-y-1 hover:shadow-xl rounded-lg overflow-hidden bg-white shadow-md">
      <div className="aspect-video w-full h-60 overflow-hidden">
        <img 
          src={images[imageNumber]} 
          alt={title}
          className="w-full h-full object-cover rounded-t-lg" 
        />
      </div>
      <div className="p-4">
        <h3 className="text-base font-medium text-gray-900">{title}</h3>
        <p className="text-sm text-gray-600 mt-2">{category}</p>
        <p className="text-sm text-gray-500 mt-1">{views} views • {formatDate(timestamp)}</p>
      </div>
    </div>
  );
};

export default VideoCard;
