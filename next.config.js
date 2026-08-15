/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'https://jurisiva-ai.onrender.com/api/:path*',
      },
      {
        source: '/health',
        destination: 'https://jurisiva-ai.onrender.com/health',
      },
    ];
  },
};

module.exports = nextConfig;
