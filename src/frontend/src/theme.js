import { defineConfig, createSystem, defaultConfig } from '@chakra-ui/react';

const config = defineConfig({
  cssVarsRoot: ':where(:root, :host)',
  cssVarsPrefix: 'ck',
  strictTokens: false,

  globalCss: {
    'html, body': {
      margin: 0,
      padding: 0,
      fontFamily: "'Roboto', sans-serif",
      backgroundColor: '{colors.bg}',
      color: '{colors.text}',
    },
  },

  conditions: {
    cqSm: '@container(min-width: 320px)',
    child: '& > *',
  },

  theme: {
    breakpoints: {
      sm: '320px',
      md: '768px',
      lg: '960px',
      xl: '1200px',
    },

    tokens: {
      colors: {
        bg: '#f9fafb',
        text: '#1a202c',
        primary: '#319795',
        red: '#E53E3E',
        muted: '#718096',
      },
      radii: {
        md: '12px',
        lg: '24px',
      },
      shadows: {
        soft: '0 4px 12px rgba(0, 0, 0, 0.1)',
      },
    },

    semanticTokens: {
      colors: {
        danger: { value: '{colors.red}' },
        primary: { value: '{colors.primary}' },
        background: { value: '{colors.bg}' },
      },
    },

    keyframes: {
      fadeIn: {
        from: { opacity: 0 },
        to: { opacity: 1 },
      },
      spin: {
        from: { transform: 'rotate(0deg)' },
        to: { transform: 'rotate(360deg)' },
      },
    },

    animationStyles: {
      fadeIn: {
        animation: 'fadeIn 0.3s ease-in',
      },
      spinSlow: {
        animation: 'spin 3s linear infinite',
      },
    },

    textStyles: {
      heading: {
        description: 'Page heading',
        value: {
          fontSize: '2xl',
          fontWeight: 'bold',
        },
      },
      body: {
        value: {
          fontSize: 'md',
          lineHeight: '1.5',
        },
      },
    },

    layerStyles: {
      card: {
        bg: 'white',
        boxShadow: 'soft',
        borderRadius: 'md',
        p: '4',
      },
    },
  },
});

const system = createSystem(defaultConfig, config);

export default system;
