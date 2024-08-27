import React from 'react'
import { FaGithub, FaLinkedin } from 'react-icons/fa'
import { FaInstagram } from 'react-icons/fa'


function Navbar() {
  return (
    <nav className=' flex  items-center justify-between py-6'>
        <div className="flex flex-shrink-0 items-center">
          <p>OK</p>
        </div>
        <div className='m-8 flex justify-center items-center gap-4 text2xl'>
          < FaLinkedin />
          < FaGithub />
          < FaInstagram />
        </div>
    </nav>
  )
}

export default Navbar