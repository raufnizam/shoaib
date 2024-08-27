import React from 'react';
import { motion } from 'framer-motion';
import { CONTACT } from '../constants';

function Contact() {
  return (
    <div className='border-b border-neutral-900 h-[50vh] flex flex-col items-center justify-center'>
      <motion.h2 
        whileInView={{ opacity: 1, y: 0 }}
        initial={{ opacity: 0, y: -100 }}
        transition={{ duration: 1.5 }}
        className="text-center text-4xl mb-6"
      >
        Get In Touch
      </motion.h2>
      <div className="text-center tracking-tighter">
        <motion.p 
          whileInView={{ opacity: 1, x: 0 }}
          initial={{ opacity: 0, x: 100 }}
          transition={{ duration: 0.5 }}
          className="my-4"
        >
          {CONTACT.phoneNo}
        </motion.p>
        <a 
          href='#' 
          className="my-4 border-b border-neutral-500 hover:border-neutral-900"
        >
          {CONTACT.email}
        </a>
      </div>
    </div>
  );
}

export default Contact;
