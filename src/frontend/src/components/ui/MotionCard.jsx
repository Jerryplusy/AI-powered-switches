import { Box, Text, Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);

/**
 * 带有动作效果的卡片
 * @param icon 可选图标
 * @param text 文字
 * @param onClick 点击执行操作
 * @returns {JSX.Element}
 * @constructor
 */
const MotionCard = ({ icon, text, onClick }) => (
  <MotionBox
    whileHover={{
      y: -3,
      boxShadow: 'inset 0 0 0 1000px rgba(255, 255, 255, 0.3)',
    }}
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
    transition={{ duration: 0.1 }}
  >
    {icon && <Image src={icon} boxSize={5} mr={2} />}
    <Text color={'white'}>{text}</Text>
  </MotionBox>
);

export default MotionCard;
