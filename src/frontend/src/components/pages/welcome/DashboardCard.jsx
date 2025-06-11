import manageIcon from '@/resources/welcome/image/setting.svg';
import MotionCard from '@/components/ui/MotionCard';
import { useNavigate } from 'react-router-dom';
import FadeInWrapper from '@/components/system/layout/FadeInWrapper';

/**
 * 进入管理后台按钮组件
 * @returns {JSX.Element}
 * @constructor
 */
const DashboardCard = () => {
  const navigate = useNavigate();
  return (
    <FadeInWrapper delay={0.4} yOffset={-5}>
      <MotionCard icon={manageIcon} text={'管理后台'} onClick={() => navigate('/dashboard')} />
    </FadeInWrapper>
  );
};

export default DashboardCard;
