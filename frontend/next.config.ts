import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.unsplash.com",
        port: "",
        pathname: "/**",
      },
    ],
  },
  serverExternalPackages: ["better-auth"],

  // This fixes Turbopack workspace root warning
  turbopack: {
    root: __dirname,
  },
};

export default nextConfig;
