/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        navy: {
          50: '#e8e8ed',
          100: '#d1d1db',
          200: '#a3a3b7',
          300: '#757593',
          400: '#47476f',
          500: '#1a1a2e',
          600: '#151525',
          700: '#10101c',
          800: '#0b0b13',
          900: '#06060a',
        },
        electric: {
          50: '#eef0fd',
          100: '#dce1fb',
          200: '#b9c3f7',
          300: '#97a5f3',
          400: '#7487ef',
          500: '#4361ee',
          600: '#1b3bdb',
          700: '#152daa',
          800: '#0f2079',
          900: '#091348',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        heading: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
      },
      typography: (theme) => ({
        DEFAULT: {
          css: {
            maxWidth: '75ch',
            color: theme('colors.gray.700'),
            a: {
              color: theme('colors.electric.500'),
              '&:hover': {
                color: theme('colors.electric.600'),
              },
            },
            'h1, h2, h3, h4': {
              color: theme('colors.navy.500'),
              fontWeight: '700',
            },
            code: {
              color: theme('colors.electric.600'),
              backgroundColor: theme('colors.gray.100'),
              padding: '0.2em 0.4em',
              borderRadius: '0.25rem',
              fontWeight: '500',
            },
            'code::before': { content: '""' },
            'code::after': { content: '""' },
          },
        },
        dark: {
          css: {
            color: theme('colors.gray.300'),
            a: {
              color: theme('colors.electric.400'),
              '&:hover': {
                color: theme('colors.electric.300'),
              },
            },
            'h1, h2, h3, h4': {
              color: theme('colors.gray.100'),
            },
            code: {
              color: theme('colors.electric.300'),
              backgroundColor: theme('colors.navy.600'),
            },
          },
        },
      }),
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
