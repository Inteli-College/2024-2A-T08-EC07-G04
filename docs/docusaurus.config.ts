import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';
const config: Config = {
  title: 'Fillmore',
  tagline: 'Dinosaurs are cool',
  favicon: 'img/logo_fillmore.png',
  // Set the production url of your site here
  url: 'https://inteli-college.github.io/',
  // Set the /<baseUrl>/ pathname under which your site is served
  // For GitHub pages deployment, it is often '/<projectName>/'
  baseUrl: '/2024-2A-T08-EC07-G04/',
  // GitHub pages deployment config.
  // If you aren't using GitHub pages, you don't need these.
  organizationName: 'Inteli-College', // Usually your GitHub org/user name.
  projectName: '2024-2A-T08-EC07-G04', // Usually your repo name.
  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',
  // Even if you don't use internationalization, you can use this field to set
  // useful metadata like html lang. For example, if your site is Chinese, you
  // may want to replace "en" with "zh-Hans".
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  presets: [
    [
      'classic',
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: './sidebars.ts',
          // Please change this to your repo.
          // Remove this to remove the "edit this page" links.
          routeBasePath: '/',
          // editUrl: 'https://github.com/Inteli-College/2024-2A-T08-EC07-G05/tree/docs/setup/docs',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      }),
    ],
  ],
  themeConfig: {
    // Replace with your project's social card
    // image: 'img/docusaurus-social-card.jpg',
    navbar: {
      title: 'Fillmore',
      logo: {
        alt: 'Docusaurus',
        src: 'img/logo_fillmore.png',
      },
      items: [],
    },
    footer: {
      style: 'dark',
      links: [],
      copyright: `Copyright © ${new Date().getFullYear()} Fillmore. Built with Docusaurus.`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    customCss: `
      @media screen and (min-width: 1900px) {
        html {
          zoom: 60%;
        }
      }
    `,
  } satisfies Preset.ThemeConfig,
};
export default config;