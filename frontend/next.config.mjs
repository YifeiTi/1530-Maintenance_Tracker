const backendUrl = (process.env.API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

const nextConfig = {
  async rewrites() {
    return [{ source: '/api/reports/:path*', destination: `${backendUrl}/reports/:path*` }];
  },
};

export default nextConfig;
