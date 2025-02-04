import React from 'react'
import { FaBaseballBall, FaChartLine, FaHistory } from 'react-icons/fa'
import Header from './../components/Header'

const AboutPage = () => {
  return (<>
    
    <Header/>

    <div className="min-h-screen bg-gray-50">
      {/* Hero Section - Updated to be elevated */}
      <div className="relative py-20">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-blue-700 text-white rounded-lg shadow-lg p-12 text-center">
            <h1 className="text-4xl md:text-5xl font-bold mb-6">About Us</h1>
            <p className="text-xl text-blue-100">
              Revolutionizing how we engage with baseball's rich history
            </p>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10">
        {/* Mission Card */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <p className="text-lg text-gray-700 leading-relaxed mb-6">
            Welcome to Statcast Archive Analyzer, a groundbreaking platform dedicated to revolutionizing how we engage with baseball's rich history. Our mission is simple: to bring the power of modern analytics to archival game footage, enabling fans, analysts, and players to uncover new insights into the game they love.
          </p>
        </div>

        {/* Features Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-12">
          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <FaBaseballBall className="text-4xl text-blue-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-3">Cutting-Edge Technology</h3>
            <p className="text-gray-600">
              Utilizing advanced AI and computer vision to extract valuable metrics from historic footage
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <FaChartLine className="text-4xl text-blue-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-3">Advanced Analytics</h3>
            <p className="text-gray-600">
              Access detailed Statcast metrics like pitch speed, exit velocity, and launch angle
            </p>
          </div>

          <div className="bg-white rounded-lg shadow-md p-6 text-center">
            <FaHistory className="text-4xl text-blue-600 mx-auto mb-4" />
            <h3 className="text-xl font-semibold mb-3">Historical Insights</h3>
            <p className="text-gray-600">
              Bridge the gap between baseball's analog past and its digital future
            </p>
          </div>
        </div>

        {/* Vision Section */}
        <div className="bg-white rounded-lg shadow-lg p-8 mb-12">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Our Vision</h2>
          <p className="text-gray-700 leading-relaxed mb-6">
            Our vision is to bridge the gap between baseball's analog past and its digital future, fostering a deeper appreciation for the game and its history.
          </p>
          <p className="text-gray-700 leading-relaxed">
            Join us on this journey as we unlock the hidden stories behind every pitch, swing, and play.
          </p>
        </div>
      </div>
    </div>
    </>
  )
}

export default AboutPage
