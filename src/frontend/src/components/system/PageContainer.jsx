import { Box } from '@chakra-ui/react';

/**
 * 解决导航栏占位问题
 * @param children
 * @returns {JSX.Element}
 * @constructor
 */
const PageContainer = ({ children }) => {
  return (
    <Box pt={'60px'} px={6}>
      {children}
    </Box>
  );
};

export default PageContainer;
