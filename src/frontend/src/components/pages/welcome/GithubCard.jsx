import githubIcon from '@/resources/welcome/image/github.svg';
import MotionCard from '@/components/ui/MotionCard';

const GithubCard = () => {
  return (
    <MotionCard
      icon={githubIcon}
      text={'github'}
      onClick={() => window.open('https://github.com/Jerryplusy/AI-powered-switches', '_blank')}
    />
  );
};

export default GithubCard;
