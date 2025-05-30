import { Button } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionButton = motion(Button);

const NavButton = ({ children, ...props }) => (
  <MotionButton
    whileHover={{ scale: 1.02 }}
    whileTap={{ scale: 0.95 }}
    colorScheme={'teal'}
    variant={'solid'}
    borderRadius={'lg'}
    {...props}
  >
    {children}
  </MotionButton>
);

export default NavButton;
