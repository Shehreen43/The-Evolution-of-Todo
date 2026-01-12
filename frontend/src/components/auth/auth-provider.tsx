"use client";

import React from "react";
import { useSession } from "@/lib/auth-client";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  // Initialize session state safely
  const sessionQuery = useSession();
  const session = sessionQuery?.data || {};
  const isPending = sessionQuery?.isPending || true;

  return (
    <div className={isPending ? "opacity-50 pointer-events-none" : ""}>
      {children}
    </div>
  );
}
