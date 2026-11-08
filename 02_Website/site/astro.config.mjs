import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';
import remarkFill from './src/lib/remark-fill.mjs';

// SITE is the public URL. Set PUBLIC_SITE_URL when the domain exists (see .env.example).
const site = process.env.PUBLIC_SITE_URL || 'https://isapurindustrialpark.example';

export default defineConfig({
  site,
  output: 'static',
  trailingSlash: 'always',
  build: { inlineStylesheets: 'always' },
  integrations: [sitemap()],
  markdown: { remarkPlugins: [remarkFill] },
});
