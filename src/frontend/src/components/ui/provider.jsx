'use client';
import { ChakraProvider } from '@chakra-ui/react';
import { ColorModeProvider } from './color-mode';
import createSystem from '@/theme';

const system = createSystem;

export function Provider(props) {
  return (
    <ChakraProvider value={system}>
      <ColorModeProvider {...props} />
    </ChakraProvider>
  );
}
