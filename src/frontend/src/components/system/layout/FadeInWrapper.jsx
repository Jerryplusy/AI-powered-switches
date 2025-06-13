import { AnimatePresence, motion } from 'framer-motion';

/**
 * 组件进入 / 离开时的淡入淡出动画
 * @param children 子组件
 * @param delay 延迟
 * @param yOffset y轴偏移量
 * @param duration 动画时间
 * @param className 类名
 * @param props
 * @returns {JSX.Element}
 * @constructor
 */
const FadeInWrapper = ({
  children,
  delay = 0,
  yOffset = 10,
  duration = 0.6,
  className = '',
  ...props
}) => {
  return (
    <AnimatePresence mode="wait">
      <motion.div
        key="fade-wrapper"
        initial={{ opacity: 0, y: yOffset }}
        animate={{ opacity: 1, y: 0 }}
        exit={{ opacity: 0, y: -yOffset }}
        transition={{
          delay,
          duration,
          ease: [0.16, 0.77, 0.47, 0.97],
        }}
        className={className}
        {...props}
      >
        {children}
      </motion.div>
    </AnimatePresence>
  );
};

export default FadeInWrapper;
