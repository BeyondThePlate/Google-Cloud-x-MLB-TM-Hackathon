import { Link, useNavigate } from 'react-router-dom';

const Header = () => {
  const navigate = useNavigate();
  return (
    <header className="flex justify-between items-center bg-[#001f3f] px-5 py-2.5 text-white">
      <div onClick={() => navigate('/')} className="text-2xl font-bold cursor-pointer hover:text-gray-300">Baseball</div>
      
      <nav className="flex items-center space-x-4">
      <Link to="/mymedia" className="hover:text-gray-300">MY MEDIA</Link>
      <Link to="/upload" className="hover:text-gray-300">UPLOAD VIDEO</Link>
      <Link to="/profile" className="hover:text-gray-300">PROFILE</Link>
      <Link to="/login" className="hover:text-gray-300">LOG IN</Link>
      <Link to="/signup" className="hover:text-gray-300">SIGN UP</Link>
        
      </nav>

      <div className="flex items-center space-x-4">
      <Link to="/about" className="hover:text-gray-300">ABOUT US</Link>
    <Link to="/help" className="hover:text-gray-300">HELP</Link>
      </div>
    </header>
  );
};

export default Header;
