import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const faq = z.array(z.object({ q: z.string(), a: z.string() })).optional();

const pages = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/pages' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    h1: z.string(),
    lead: z.string().optional(),
    pageType: z.enum(['home', 'plots', 'amenities', 'location', 'brands', 'gallery', 'blog', 'faq', 'contact', 'landing', 'about', 'other']),
    draft: z.boolean().default(false),
    schema: z.array(z.string()).default([]),
    faq,
    place: z.string().optional(), // landing pages: place name used in the distance block
    cta: z.string().optional(),
  }),
});

const posts = defineCollection({
  loader: glob({ pattern: '**/*.md', base: './src/content/posts' }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    h1: z.string(),
    lead: z.string().optional(),
    date: z.coerce.date(),
    draft: z.boolean().default(false),
    faq,
  }),
});

export const collections = { pages, posts };
