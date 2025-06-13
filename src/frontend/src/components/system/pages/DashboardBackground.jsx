import React, { useState, useEffect } from 'react';
import { Box } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);

/**
 * 控制台背景
 * @returns {JSX.Element}
 * @constructor
 */
const DashboardBackground = () => {
  const [mousePos, setMousePos] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePos({ x: e.clientX, y: e.clientY });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  const spotlight = {
    background: `radial-gradient(
      circle at ${mousePos.x}px ${mousePos.y}px,
      rgba(255, 255, 255, 0.05) 0%,
      rgba(255, 255, 255, 0.02) 120px,
      transparent 240px
    )`,
  };

  return (
    <MotionBox
      position={{ base: 'fixed' }}
      top={0}
      left={0}
      w={{ base: '100vw' }}
      h={{ base: '100vh' }}
      zIndex={-1}
      background={{
        base: 'linear-gradient(135deg, #18274C 0%, #21397F 50%, #1D3062 100%)',
      }}
      _after={{
        content: { base: '""' },
        position: { base: 'absolute' },
        top: 0,
        left: 0,
        w: { base: '100%' },
        h: { base: '100%' },
        pointerEvents: { base: 'none' },
        ...spotlight,
        transition: { base: 'background 0.2s ease' },
      }}
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 1.2, ease: 'easeInOut' }}
    />
  );
};

export default DashboardBackground;
