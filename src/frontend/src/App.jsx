import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppShell from '@/components/system/layout/AppShell';
import buildRoutes from '@/constants/routes/routes';

const App = () => {
  const isProd = process.env.NODE_ENV === 'production';
  return (
    <BrowserRouter basename={isProd ? '/AI-powered-switches' : '/'}>
      <Routes>
        <Route path="/" element={<AppShell />}>
          {buildRoutes()}
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
