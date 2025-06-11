import { Box, Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';
import image from '@/resources/welcome/image/background.png';

const MotionBox = motion(Box);

/**
 * 带高斯模糊的背景
 * @returns {JSX.Element}
 * @constructor
 */
const BackgroundBlur = () => (
  <MotionBox
    position={'absolute'}
    top={0}
    left={0}
    width={'100%'}
    height={'100%'}
    filter={'blur(6px)'}
    zIndex={0}
    initial={{ opacity: 0 }}
    animate={{ opacity: 1 }}
    transition={{ duration: 0.4, ease: 'easeInOut' }}
  >
    <Image src={image} objectFit={'cover'} width={'100%'} height={'100%'} />
  </MotionBox>
);

export default BackgroundBlur;
