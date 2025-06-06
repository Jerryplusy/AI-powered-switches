import { Box } from '@chakra-ui/react';

/**
 * 卡片组件
 * @param children
 * @param props
 * @returns {JSX.Element}
 * @constructor
 */
const Card = ({ children, ...props }) => (
  <Box
    bg={'rgba(255,255,255,0.1)'}
    backdropFilter={'blur(10px)'}
    borderRadius={'xl'}
    boxShadow={'lg'}
    p={6}
    {...props}
  >
    {children}
  </Box>
);

export default Card;
