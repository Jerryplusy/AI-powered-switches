import githubIcon from '@/resources/welcome/image/github.svg';
import MotionCard from '@/components/ui/MotionCard';
import FadeInWrapper from '@/components/system/layout/FadeInWrapper';

/**
 * GitHub按钮组件
 * @returns {JSX.Element}
 * @constructor
 */
const GithubCard = () => {
  return (
    <FadeInWrapper delay={0.1} yOffset={-10}>
      <MotionCard
        icon={githubIcon}
        text={'Github'}
        onClick={() => window.open('https://github.com/Jerryplusy/AI-powered-switches', '_blank')}
      />
    </FadeInWrapper>
  );
};

export default GithubCard;
