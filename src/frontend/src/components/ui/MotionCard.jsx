import { Box, Text, Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);

const MotionCard = ({ icon, text, onClick }) => (
  <MotionBox
    whileHover={{ y: -5 }}
    display={'flex'}
    alignItems={'center'}
    bg={'whiteAlpha.200'}
    border={'1px solid'}
    borderColor={'gray.600'}
    px={4}
    py={2}
    borderRadius={'md'}
    cursor={'pointer'}
    onClick={onClick}
  >
    {icon && <Image src={icon} boxSize={5} mr={2} />}
    <Text color={'white'}>{text}</Text>
  </MotionBox>
);

export default MotionCard;
