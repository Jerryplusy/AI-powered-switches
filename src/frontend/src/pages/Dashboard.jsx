import React from 'react';
import { Box, Text } from '@chakra-ui/react';
import DocumentTitle from '@/components/system/pages/DocumentTitle';
import PageContainer from '@/components/system/PageContainer';
import DashboardBackground from '@/components/system/pages/DashboardBackground';
import FadeInWrapper from '@/components/system/layout/FadeInWrapper';

const Dashboard = () => {
  return (
    <DocumentTitle title={'控制台'}>
      <DashboardBackground />
      <PageContainer>
        <FadeInWrapper delay={0.1} yOffset={-5}>
          <Box p={6}>
            <Text fontSize={'xl'}>控制台奇怪的功能+1</Text>
          </Box>
        </FadeInWrapper>
      </PageContainer>
    </DocumentTitle>
  );
};

export default Dashboard;
