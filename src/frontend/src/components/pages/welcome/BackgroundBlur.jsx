import { Box, Image } from '@chakra-ui/react';
import image from '@/resources/welcome/image/background.png';

/**
 * 带高斯模糊的背景
 * @returns {JSX.Element}
 * @constructor
 */
const BackgroundBlur = () => (
  <Box
    position={'absolute'}
    top={0}
    left={0}
    width={'100%'}
    height={'100%'}
    filter={'blur(6px)'}
    zIndex={0}
  >
    <Image src={image} objectFit={'cover'} width={'100%'} height={'100%'} />
  </Box>
);

export default BackgroundBlur;
