import FadeInWrapper from './FadeInWrapper';

/**
 * 递归为组件及子组件添加载入动效
 * @param children 子组件
 * @param baseDelay 延迟
 * @param increment 增值
 * @param className 类名
 * @returns {JSX.Element}
 * @constructor
 */
const StaggeredFadeIn = ({ children, baseDelay = 0.2, increment = 0.1, className = '' }) => {
  return (
    <>
      {React.Children.map(children, (child, index) => (
        <FadeInWrapper key={index} delay={baseDelay + index * increment} className={className}>
          {child}
        </FadeInWrapper>
      ))}
    </>
  );
};

export default StaggeredFadeIn;
