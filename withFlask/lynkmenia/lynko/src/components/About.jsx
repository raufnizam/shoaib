import React from "react";
import { motion } from "framer-motion";
import { ABOUT_TEXT } from "../constants";
import { FaAndroid, FaApple, FaLinux, FaWindows } from "react-icons/fa";

function About() {
  const iconVariants = (duration) => ({
    initial: { y: -10 },
    animate: {
      y: [10, -10],
      transition: {
        duration: duration,
        type: "linear",
        repeat: Infinity,
        repeatType: "reverse",
      },
    },
  });

  return (
    <div className="border-b border-neutral-900 pb-4 mt-8 h-[60vh] flex flex-col items-center justify-center">
      <h2 className="text-center text-4xl mb-6">
        Supported <span className="text-neutral-500">Platforms</span>
      </h2>
      <div className="flex flex-wrap w-full h-full items-center justify-center">
        <div className="w-full lg:w-1/2 lg:p-8 flex items-center justify-center">
          <motion.p
            whileInView={{ opacity: 1, x: 0 }}
            initial={{ opacity: 0, x: -100 }}
            transition={{ duration: 0.5 }}
            className="text-center"
          >
            {ABOUT_TEXT}
          </motion.p>
        </div>
        <div className="w-full lg:w-1/2 flex justify-center lg:justify-start">
          <motion.div
            whileInView={{ opacity: 1, x: 0 }}
            initial={{ opacity: 0, x: 100 }}
            transition={{ duration: 0.5 }}
            className="flex flex-wrap items-center justify-center gap-4"
          >
            <motion.div
              variants={iconVariants(2.5)}
              initial="initial"
              animate="animate"
              className="rounded-2xl border-4 border-neutral-800 p-4"
            >
              <FaApple className="text-7xl text-gray-700" />
            </motion.div>

            <motion.div
              variants={iconVariants(3)}
              initial="initial"
              animate="animate"
              className="rounded-2xl border-4 border-neutral-800 p-4"
            >
              <FaAndroid className="text-7xl text-gray-700" />
            </motion.div>

            <motion.div
              variants={iconVariants(5)}
              initial="initial"
              animate="animate"
              className="rounded-2xl border-4 border-neutral-800 p-4"
            >
              <FaLinux className="text-7xl text-gray-700" />
            </motion.div>

            <motion.div
              variants={iconVariants(3)}
              initial="initial"
              animate="animate"
              className="rounded-2xl border-4 border-neutral-800 p-4"
            >
              <FaWindows className="text-7xl text-gray-700" />
            </motion.div>
          </motion.div>
        </div>
      </div>
    </div>
  );
}

export default About;
