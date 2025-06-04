import manageIcon from '@/resources/welcome/image/setting.svg';
import MotionCard from '@/components/ui/MotionCard';
import { useNavigate } from 'react-router-dom';

const DashboardCard = () => {
  const navigate = useNavigate();
  return <MotionCard icon={manageIcon} text="管理后台" onClick={() => navigate('/dashboard')} />;
};

export default DashboardCard;
