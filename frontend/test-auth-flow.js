/**
 * Test script to verify the authentication flow works correctly
 */

const axios = require('axios');

// Test configuration
const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';
const FRONTEND_BASE_URL = process.env.FRONTEND_BASE_URL || 'http://localhost:3000';

async function testAuthFlow() {
    console.log('🧪 Testing Authentication Flow...\n');

    try {
        // Test 1: Verify backend is running
        console.log('1️⃣  Testing backend connectivity...');
        const healthCheck = await axios.get(`${API_BASE_URL}/health`);
        console.log('✅ Backend is accessible:', healthCheck.data.status);

        // Test 2: Try to register a test user
        console.log('\n2️⃣  Testing user registration...');
        const testUser = {
            email: `testuser_${Date.now()}@example.com`,
            password: 'TestPass123!',
            name: 'Test User'
        };

        try {
            const signupResponse = await axios.post(`${API_BASE_URL}/api/auth/signup`, testUser);
            console.log('✅ User registration successful:', signupResponse.data.user.email);
            const token = signupResponse.data.token;

            // Test 3: Verify token can be used to access protected endpoint
            console.log('\n3️⃣  Testing token authentication...');
            const profileResponse = await axios.get(`${API_BASE_URL}/api/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            console.log('✅ Token authentication successful:', profileResponse.data.email);

            // Test 4: Test login with the same credentials
            console.log('\n4️⃣  Testing user login...');
            const loginResponse = await axios.post(`${API_BASE_URL}/api/auth/signin`, {
                email: testUser.email,
                password: testUser.password
            });
            console.log('✅ User login successful:', loginResponse.data.user.email);

            // Test 5: Test logout
            console.log('\n5️⃣  Testing logout...');
            const logoutResponse = await axios.post(`${API_BASE_URL}/api/auth/logout`, {}, {
                headers: {
                    'Authorization': `Bearer ${loginResponse.data.token}`
                }
            });
            console.log('✅ Logout successful');

            console.log('\n🎉 All authentication tests passed!');
            console.log('✅ Registration, login, profile access, and logout work correctly.');

        } catch (signupError) {
            if (signupError.response) {
                console.error('❌ Signup/Login error:', signupError.response.data);
            } else {
                console.error('❌ Network error:', signupError.message);
            }
            throw signupError;
        }

    } catch (error) {
        console.error('\n❌ Authentication flow test failed:', error.message);
        process.exit(1);
    }
}

// Run the test
testAuthFlow();