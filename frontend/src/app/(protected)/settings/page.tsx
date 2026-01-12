'use client';

import React from 'react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/forms';

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Settings</h1>
        <p className="text-muted-foreground">
          Manage your account settings and preferences.
        </p>
      </div>

      <hr className="my-6 border-gray-200" />

      <div className="border rounded-lg p-6 bg-white shadow-sm">
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">Account Information</h2>
          <p className="text-muted-foreground">
            Update your account information and preferences.
          </p>
        </div>
        <div className="space-y-4">
          <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
            <div className="space-y-2">
              <label htmlFor="firstName" className="text-sm font-medium">First Name</label>
              <Input id="firstName" placeholder="John" />
            </div>
            <div className="space-y-2">
              <label htmlFor="lastName" className="text-sm font-medium">Last Name</label>
              <Input id="lastName" placeholder="Doe" />
            </div>
          </div>
          <div className="space-y-2">
            <label htmlFor="email" className="text-sm font-medium">Email</label>
            <Input id="email" type="email" placeholder="john@example.com" />
          </div>
          <div className="space-y-2">
            <label htmlFor="timezone" className="text-sm font-medium">Timezone</label>
            <select id="timezone" className="w-full rounded-md border border-input bg-background px-3 py-2">
              <option>(GMT-12:00) International Date Line West</option>
              <option>(GMT-11:00) Midway Island, Samoa</option>
              <option>(GMT-10:00) Hawaii</option>
              <option>(GMT-09:00) Alaska</option>
              <option>(GMT-08:00) Pacific Time (US & Canada)</option>
              <option>(GMT-07:00) Mountain Time (US & Canada)</option>
              <option>(GMT-06:00) Central Time (US & Canada)</option>
              <option>(GMT-05:00) Eastern Time (US & Canada)</option>
              <option>(GMT-04:00) Atlantic Time (Canada)</option>
            </select>
          </div>
          <Button>Save Changes</Button>
        </div>
      </div>

      <div className="border rounded-lg p-6 bg-white shadow-sm">
        <div className="mb-6">
          <h2 className="text-xl font-semibold mb-2">Danger Zone</h2>
          <p className="text-muted-foreground">
            Permanently delete your account and all your data.
          </p>
        </div>
        <Button variant="destructive">Delete Account</Button>
      </div>
    </div>
  );
}