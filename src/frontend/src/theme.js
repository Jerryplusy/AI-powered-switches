import { defineConfig, createSystem, defaultConfig } from '@chakra-ui/react';

const config = defineConfig({
  cssVarsRoot: ':where(:root, :host)',
  cssVarsPrefix: 'ck',
  strictTokens: true,

  globalCss: {}, //全局css

  conditions: {
    child: '& > *', //子元素选择
  },

  theme: {
    //核心主题配置
    components: {
      //组件样式
    },
    breakpoints: {
      //响应式断点
      sm: '320px',
      md: '768px',
      lg: '960px',
      xl: '1200px',
    },

    tokens: {
      //基础主题
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
      //自定义标记
      colors: {
        danger: { value: '{colors.red}' },
        primary: { value: '{colors.primary}' },
        background: { value: '{colors.bg}' },
      },
    },

    keyframes: {
      //关键帧
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
      //预定义动画样式
      fadeIn: {
        animation: 'fadeIn 0.3s ease-in',
      },
      spinSlow: {
        animation: 'spin 3s linear infinite',
      },
    },

    textStyles: {
      //文字样式
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
      //层样式
      card: {
        bg: 'white',
        boxShadow: 'soft',
        borderRadius: 'md',
        p: '4',
      },
    },
  },
});

export default createSystem(defaultConfig, config);
