import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AppShell from '@/components/system/layout/AppShell';
import buildRoutes from '@/constants/routes/routes';

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<AppShell />}>
          {buildRoutes()}
        </Route>
      </Routes>
    </BrowserRouter>
  );
};

export default App;
