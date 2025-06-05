import { Outlet, useLocation } from 'react-router-dom';
import PageTransition from './PageTransition';
import { Box } from '@chakra-ui/react';
import { AnimatePresence } from 'framer-motion';

/**
 * 应用加壳
 * @returns {JSX.Element}
 * @constructor
 */
const AppShell = () => {
  const location = useLocation();

  return (
    <Box position={'relative'} height={'100vh'} overflow={'hidden'}>
      <Box overflowY={'auto'} height={'100%'}>
        <AnimatePresence mode={'wait'}>
          <PageTransition key={location.pathname}>
            <Outlet />
          </PageTransition>
        </AnimatePresence>
      </Box>
    </Box>
  );
};

export default AppShell;
