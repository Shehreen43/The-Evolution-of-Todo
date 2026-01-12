'use client';

import { BaseShell } from "@/components/layout/page-layouts";
import { useSession } from "@/lib/auth-client";
import { useRouter } from "next/navigation";
import { useEffect } from "react";
import { Spinner } from "@/components/ui";

export default function ProtectedLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const { data: session, isPending } = useSession();
    const router = useRouter();

    useEffect(() => {
        if (!isPending && !session) {
            router.push("/signin");
        }
    }, [session, isPending, router]);

    if (isPending) {
        return (
            <div className="flex min-h-screen items-center justify-center bg-[#fafafa]">
                <Spinner size="xl" />
            </div>
        );
    }

    if (!session) return null;

    return (
        <BaseShell showSidebar={true}>
            {children}
        </BaseShell>
    );
}
