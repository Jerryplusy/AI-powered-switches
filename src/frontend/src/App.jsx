import { Route, Routes } from 'react-router-dom';
import Welcome from '@/pages/Welcome';
import Dashboard from '@/pages/Dashboard';

const App = () => {
  return (
    <Routes>
      <Route path={'/'} element={<Welcome />} />
      <Route path={'/dashboard'} element={<Dashboard />} />
    </Routes>
  );
};

export default App;