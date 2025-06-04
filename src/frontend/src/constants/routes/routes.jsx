import { Route } from 'react-router-dom';
import Welcome from '@/pages/Welcome';
import Dashboard from '@/pages/Dashboard';

const routeList = [
  { path: '/', element: <Welcome /> },
  { path: '/dashboard', element: <Dashboard /> },
];

const buildRoutes = () =>
  routeList.map(({ path, element }) => <Route key={path} path={path} element={element} />);

export default buildRoutes;
