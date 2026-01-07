/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  trailingSlash: true,
  basePath: process.env.NODE_ENV === 'production' ? '/AI-Film-Studio' : '',
  assetPrefix: process.env.NODE_ENV === 'production' ? '/AI-Film-Studio/' : '',
  images: {
    unoptimized: true
  }
};

export default nextConfig;
