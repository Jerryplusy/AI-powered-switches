import { useEffect } from 'react';

const DocumentTitle = ({ title, children }) => {
  useEffect(() => {
    document.title = title || '网络管理后台';
  }, [title]);
  return children;
};

export default DocumentTitle;
