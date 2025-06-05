import { motion } from 'framer-motion';

/**
 * 页面动效
 * @param children
 * @returns {JSX.Element}
 * @constructor
 */
const PageTransition = ({ children }) => <motion.div>{children}</motion.div>;

export default PageTransition;
/**
 *     initial={{ opacity: 0, y: 0 }}
 *     animate={{ opacity: 1, y: 0 }}
 *     transition={{ duration: 0.2 }}
 */
