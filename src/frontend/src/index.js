import React from 'react';
import ReactDOM from 'react-dom/client';
import App from '@/App';
import { Provider } from '@/components/ui/provider';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <Provider>
    <App />
  </Provider>
);
