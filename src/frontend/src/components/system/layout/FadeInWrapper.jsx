import { motion } from 'framer-motion';

/**
 * 组件载入动画
 * @param children 子组件
 * @param delay 延迟
 * @param yOffset y轴偏移量
 * @param duration 动画时间
 * @param className 类名
 * @returns {JSX.Element}
 * @constructor
 */
const FadeInWrapper = ({ children, delay = 0, yOffset = 10, duration = 0.6, className = '' }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: yOffset }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        delay,
        duration,
        ease: [0.16, 0.77, 0.47, 0.97],
      }}
      className={className}
    >
      {children}
    </motion.div>
  );
};
export default FadeInWrapper;
