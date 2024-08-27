import React, { useState } from 'react';
import { HERO_CONTENT } from '../constants';
import { motion } from 'framer-motion';
import axios from 'axios';

const container = (delay) => ({
  hidden: { x: -100, opacity: 0 },
  visible: {
    x: 0,
    opacity: 1,
    transition: { duration: 0.5, delay: delay },
  },
});

function Hero() {
  const [url, setUrl] = useState('');
  const [mode, setMode] = useState('video');

  const handleSubmit = async (event) => {
    event.preventDefault();

    try {
      const response = await axios.post('/download', {
        url: url,
        mode: mode,
      });
      console.log('Success:', response.data);
      // Handle success (e.g., display a message or process response)
    } catch (error) {
      console.error('Error:', error);
      // Handle error (e.g., display an error message)
    }
  };

  return (
    <div className="flex items-center justify-center h-[80vh] border-b border-neutral-900">
      <div className="flex flex-wrap w-full max-w-screen-xl px-4 lg:px-8">
        <div className="w-full lg:w-1/2 flex flex-col items-center lg:items-start">
          <motion.h2
            variants={container(0.5)}
            initial="hidden"
            animate="visible"
            className="text-6xl tracking-tight text-transparent bg-gradient-to-r from-pink-300 via-slate-500 to-purple-500 bg-clip-text"
          >
            All Video Downloader
          </motion.h2>
          <motion.p
            variants={container(1)}
            initial="hidden"
            animate="visible"
            className="py-6 my-2 font-light tracking-tighter max-w-xl"
          >
            {HERO_CONTENT}
          </motion.p>
        </div>
        <div className="w-full lg:w-1/2 flex justify-center lg:p-8">
          <motion.div
            initial={{ x: 100, opacity: 0 }}
            animate={{
              x: 0,
              opacity: 1,
              transition: { duration: 1.2 },
            }}
            className="flex flex-col space-y-4 max-w-md w-full"
          >
            <form className="space-y-4" onSubmit={handleSubmit}>
              <input
                type="text"
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="URL..."
                className="w-full px-4 py-2 text-gray-700 bg-black border-transparent border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
              />
              <select
                id="mode"
                name="mode"
                value={mode}
                onChange={(e) => setMode(e.target.value)}
                className="mt-1 w-full px-4 py-2.5 bg-black border-transparent border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              >
                <option value="video">Video</option>
                <option value="audio">Audio</option>
                <option value="playlist">Playlist</option>
              </select>
              <button
                type="submit"
                className="rounded bg-neutral-900 px-4 py-2 font-medium text-purple-900 hover:bg-purple-950 hover:text-white transition-transform"
              >
                Download
              </button>
            </form>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

export default Hero;
