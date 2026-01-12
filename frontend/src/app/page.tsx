import Link from 'next/link';
import Image from 'next/image';
import {
  CheckSquare,
  ArrowRight,
  Zap,
  ShieldCheck,
  Layout
} from 'lucide-react';
import { Button } from '@/components/ui';

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col bg-white">
      {/* Navbar */}
      <nav className="container mx-auto flex h-20 items-center justify-between px-6">
        <div className="flex items-center gap-2">
          <div className="rounded-xl bg-emerald-600 p-2 text-white">
            <CheckSquare className="h-6 w-6" />
          </div>
          <span className="text-xl font-bold tracking-tight">
            Hackathon<span className="text-emerald-600">Todo</span>
          </span>
        </div>
        <div className="hidden items-center gap-8 md:flex">
          <Link href="#features" className="text-sm font-semibold text-gray-600 hover:text-emerald-600">Features</Link>
          <Link href="/signin" className="text-sm font-semibold text-gray-600 hover:text-emerald-600">Sign In</Link>
          <Link href="/signup">
            <Button size="sm">Get Started</Button>
          </Link>
        </div>
      </nav>

      {/* Hero Section */}
      <main className="flex-1">
        <section className="relative overflow-hidden px-6 pt-16 pb-24 text-center lg:pt-32 lg:pb-40">
          {/* 3D Spline Model Background */}
          <div className="absolute inset-0 -z-10 opacity-20 overflow-hidden">
            <iframe
              src="https://my.spline.design/techinspired3dassets01protection-ttmpLiSVTFRiok4U1M8bOV4d/embed"
              frameBorder="0"
              width="100%"
              height="100%"
              style={{
                position: 'absolute',
                top: 0,
                left: 0,
                width: '100%',
                height: '100%',
                pointerEvents: 'none',
                transform: 'scale(1.1)',
                filter: 'blur(1px)',
              }}
              allowFullScreen
            ></iframe>
          </div>

          <div className="container mx-auto max-w-4xl">
            <div className="mx-auto mb-8 flex max-w-fit items-center gap-2 rounded-full border border-emerald-100 bg-emerald-50/50 px-4 py-1.5 text-sm font-bold text-emerald-700 shadow-sm animate-fade-in-up">
              <Zap className="h-4 w-4 animate-float" />
              <span>Phase II is Live! Full-Stack Mastery.</span>
            </div>

            <h1 className="text-5xl font-black tracking-tight text-gray-900 sm:text-7xl lg:leading-[1.1] animate-fade-in-up-delay-100">
              Organize Your Tasks, <br />
              <span className="bg-gradient-to-r from-emerald-600 to-teal-500 bg-clip-text text-transparent animate-pulse-slow">
                Amplify Your Impact
              </span>
            </h1>

            <p className="mx-auto mt-8 max-w-2xl text-lg text-gray-600 sm:text-xl animate-fade-in-up-delay-200">
              A modern, intelligent todo app built for high-performance teams.
              Manage your day with precision and style.
            </p>

            <div className="mt-12 flex flex-col items-center justify-center gap-4 sm:flex-row animate-fade-in-up-delay-300">
              <Link href="/signup">
                <Button size="lg" className="h-16 px-10 text-lg shadow-xl shadow-emerald-200 hover:scale-105 transition-transform">
                  Start for Free
                  <ArrowRight className="ml-2 h-5 w-5" />
                </Button>
              </Link>
              <Link href="/signin">
                <Button variant="ghost" size="lg" className="h-16 px-10 text-lg hover:scale-105 transition-transform">
                  Sign In to Dashboard
                </Button>
              </Link>
            </div>
          </div>

          {/* Abstract Preview */}
          <div className="mt-20 flex justify-center px-4">
            <div className="relative rounded-3xl border-8 border-gray-900/5 bg-gray-900/10 p-2 shadow-2xl">
              <div className="overflow-hidden rounded-2xl bg-white shadow-inner">
                <Image
                  src="https://images.unsplash.com/photo-1484480974693-6ca0a78fb36b?auto=format&fit=crop&q=80&w=1200"
                  alt="App Dashboard Preview"
                  width={1200}
                  height={800}
                  priority
                  className="w-full max-w-[1000px] opacity-90 transition-opacity hover:opacity-100 h-auto"
                />
              </div>
            </div>
          </div>
        </section>

        {/* Features */}
        <section id="features" className="bg-gray-50 py-24 px-6">
          <div className="container mx-auto">
            <div className="text-center mb-16">
              <h2 className="text-3xl font-extrabold text-gray-900 sm:text-4xl">Everything you need to focus.</h2>
              <p className="mt-4 text-gray-600 max-w-2xl mx-auto">Built with the modern tech stack: Next.js 15, FastAPI, and Neon DB.</p>
            </div>

            <div className="grid grid-cols-1 gap-8 md:grid-cols-3">
              {[
                { title: 'Lightning Fast', desc: 'Optimistic updates ensure your UI is always snappy.', icon: Zap },
                { title: 'Secure by Design', desc: 'Stateless JWT authentication with Better Auth integration.', icon: ShieldCheck },
                { title: 'Responsive UI', desc: 'Beautifully crafted for desktop and mobile productivity.', icon: Layout },
              ].map((f, i) => (
                <div key={i} className="rounded-3xl border border-gray-100 bg-white p-8 shadow-sm transition-all hover:shadow-lg">
                  <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-2xl bg-emerald-100 text-emerald-600">
                    <f.icon className="h-6 w-6" />
                  </div>
                  <h3 className="text-xl font-bold text-gray-900">{f.title}</h3>
                  <p className="mt-3 text-gray-500 leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t py-12 px-6">
        <div className="container mx-auto flex flex-col items-center justify-between gap-6 md:flex-row">
          <p className="text-sm text-gray-500">
            © 2026 Hackathon Todo. Built by Antigravity.
          </p>
          <div className="flex gap-8">
            <Link href="#" className="text-sm text-gray-400 hover:text-gray-600">Terms</Link>
            <Link href="#" className="text-sm text-gray-400 hover:text-gray-600">Privacy</Link>
            <Link href="#" className="text-sm text-gray-400 hover:text-gray-600">GitHub</Link>
          </div>
        </div>
      </footer>
    </div>
  );
}