import React from 'react'
import { FaEnvelope, FaPhone, FaComments, FaBaseballBall } from 'react-icons/fa'
import Header from './../components/Header'

const HelpPage = () => {
  return (
    <>
     <Header/>

    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      {/* Hero Section */}
      <div className="max-w-4xl mx-auto text-center mb-12">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">Help Center</h1>
        <p className="text-xl text-gray-600">
          Welcome to the Statcast Archive Analyzer Help Center! Below, you'll find answers to common questions and guidance on how to make the most of our platform.
        </p>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto space-y-12">
        {/* How it Works Section */}
        <section className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">How Does the Tool Work?</h2>
          <p className="text-gray-600">
            Our platform uses advanced AI models and computer vision to analyze archival baseball footage. By identifying objects like the ball, bat, and players, it calculates key metrics such as pitch speed, exit velocity, and launch angle with precision.
          </p>
        </section>

        {/* Uploading Videos Section */}
        <section className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-4">Uploading Videos</h2>
          <ul className="list-disc pl-6 text-gray-600 space-y-2">
            <li>To analyze a video, simply upload a file in one of our supported formats (e.g., MP4, AVI).</li>
            <li>Ensure the footage is clear and unedited for optimal results.</li>
            <li>Once uploaded, our system will process the video and generate a detailed Statcast videos.</li>
          </ul>
        </section>

        {/* Contact Section */}
        <section className="bg-white rounded-lg shadow-md p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Contact Us</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
            <div className="flex items-center space-x-2">
              <FaEnvelope className="text-blue-600 text-xl" />
              <div>
                <p className="font-semibold">Email</p>
                <a href="mailto:gogle.cloud.25@gmail.com" className="text-blue-600 hover:text-blue-800">
                gogle.cloud.25@gmail.com
                </a>
              </div>
            </div>
            <div className="flex items-center space-x-2">
              <FaPhone className="text-blue-600 text-xl" />
              <div>
                <p className="font-semibold">Phone</p>
                <p>+90 (542) 454-4904</p>
              </div>
            </div>

          </div>
        </section>
      </div>
    </div>
    </>
  )
}

export default HelpPage
