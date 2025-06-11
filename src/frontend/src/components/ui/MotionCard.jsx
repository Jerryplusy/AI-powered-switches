import { Box, Text, Image } from '@chakra-ui/react';
import { motion } from 'framer-motion';

const MotionBox = motion(Box);

/**
 * 卡片组件
 * @param icon 可选图标
 * @param text 文字
 * @param onClick 点击执行函数
 * @param hasBlurBackground 是否模糊背景
 * @param noHover 是否禁用 hover 动画
 * @param children 子组件
 * @param props
 * @returns {JSX.Element}
 * @constructor
 */
const MotionCard = ({
  icon,
  text,
  onClick,
  hasBlurBackground = false,
  disableHover = false,
  children,
  ...props
}) => (
  <MotionBox
    position={'relative'}
    display={'flex'}
    alignItems={'center'}
    bg={'whiteAlpha.200'}
    border={'1px solid'}
    borderColor={'gray.600'}
    px={4}
    py={2}
    borderRadius={'md'}
    cursor={onClick ? 'pointer' : 'default'}
    onClick={onClick}
    transition={'all 0.2s ease'}
    overflow={'hidden'}
    _hover={
      disableHover
        ? {}
        : {
            _before: {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              bg: 'whiteAlpha.100',
              zIndex: 1,
            },
          }
    }
    {...props}
  >
    {hasBlurBackground && (
      <Box
        position={'absolute'}
        top={0}
        left={0}
        right={0}
        bottom={0}
        backdropFilter={'blur(4px)'}
        zIndex={-1}
      />
    )}
    {icon && <Image src={icon} boxSize={5} mr={2} zIndex={2} />}
    {text && (
      <Text color={'white'} zIndex={2}>
        {text}
      </Text>
    )}
    <Box zIndex={2}>{children}</Box>
  </MotionBox>
);

export default MotionCard;
