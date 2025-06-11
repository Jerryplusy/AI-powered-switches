import { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { AnimatePresence, motion } from 'framer-motion';
import { Button, HStack } from '@chakra-ui/react';
import web from '@/resources/icon/web.svg';
import githubIcon from '@/resources/welcome/image/github.svg';
import FadeInWrapper from '@/components/system/layout/FadeInWrapper';
import MotionCard from '@/components/ui/MotionCard';

const navItems = [
  { label: '面板', path: '/dashboard' },
  { label: '网络', path: '/dashboard/network' },
  { label: '交换机', path: '/dashboard/switch' },
];

/**
 * 导航栏&github按钮组件
 * @returns {JSX.Element}
 * @constructor
 */
const GithubTransitionCard = () => {
  const { pathname } = useLocation();
  const navigate = useNavigate();
  const isDashboard = pathname.startsWith('/dashboard');
  const [showNavButtons, setShowNavButtons] = useState(false);

  useEffect(() => {
    setShowNavButtons(false);
    const timer = setTimeout(() => {
      if (isDashboard) setShowNavButtons(true);
    }, 400);
    return () => clearTimeout(timer);
  }, [isDashboard]);

  return (
    <AnimatePresence mode={'wait'}>
      <motion.div
        key={isDashboard ? 'dashboard' : 'welcome'}
        initial={{ opacity: 0, height: 'auto', width: isDashboard ? 200 : 'auto' }}
        animate={{
          opacity: 1,
          height: isDashboard ? 64 : 'auto',
          width: isDashboard ? '100%' : 'fit-content',
        }}
        exit={{ opacity: 0 }}
        transition={{ duration: 0.4, ease: 'easeInOut' }}
        style={{
          position: 'fixed',
          top: 10,
          left: isDashboard ? 0 : 'auto',
          right: isDashboard ? 0 : 16,
          zIndex: 999,
          padding: isDashboard ? '0 16px' : 0,
        }}
      >
        <FadeInWrapper delay={0.1} yOffset={-10}>
          <MotionCard
            icon={isDashboard ? web : githubIcon}
            text={isDashboard ? '控制台导航栏' : 'Github'}
            hasBlurBackground
            onClick={() => {
              if (!isDashboard) {
                window.open('https://github.com/Jerryplusy/AI-powered-switches', '_blank');
              }
            }}
            justifyContent={isDashboard ? 'flex-start' : 'center'}
            alignItems={'center'}
            flexDirection={'row'}
            w={'100%'}
            px={isDashboard ? 4 : 3}
            py={isDashboard ? 3 : 2}
            noHover={isDashboard}
          >
            {isDashboard && showNavButtons && (
              <HStack spacing={4} ml={'auto'}>
                {navItems.map((item) => (
                  <Button
                    key={item.path}
                    size={'sm'}
                    variant={'ghost'}
                    color={'white'}
                    _hover={{
                      color: 'teal.300',
                      background: 'transparent',
                    }}
                    onClick={(e) => {
                      e.stopPropagation();
                      navigate(item.path);
                    }}
                  >
                    {item.label}
                  </Button>
                ))}
              </HStack>
            )}
          </MotionCard>
        </FadeInWrapper>
      </motion.div>
    </AnimatePresence>
  );
};

export default GithubTransitionCard;
