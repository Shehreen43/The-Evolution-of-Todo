const axios = require('axios');

const FRONTEND_URL = 'http://localhost:3000';
const BACKEND_URL = 'http://localhost:8000';

async function verifyFrontendChat() {
    console.log('='.repeat(80));
    console.log('FRONTEND CHAT VERIFICATION');
    console.log('='.repeat(80));

    try {
        // 1. Test Backend Health
        console.log('\n[STEP 1] Checking Backend Health...');
        const healthResp = await axios.get(`${BACKEND_URL}/health`);
        console.log(`[PASS] Backend is healthy: ${healthResp.data.status}`);

        // 2. Authenticate
        console.log('\n[STEP 2] Authenticating...');
        const email = 'frontend_chat_test@example.com';
        const password = 'FrontendTest123!';

        let authResp;
        try {
            authResp = await axios.post(`${BACKEND_URL}/api/auth/signin`, {
                email,
                password
            });
        } catch (e) {
            console.log('Signin failed, trying signup...');
            authResp = await axios.post(`${BACKEND_URL}/api/auth/signup`, {
                email,
                password,
                name: 'Frontend Chat Tester'
            });
        }

        const token = authResp.data.token;
        const userId = authResp.data.user.id;
        console.log(`[PASS] Authenticated as ${userId}`);

        const headers = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };

        // 3. Test Frontend Chat API Proxy
        console.log('\n[STEP 3] Testing Frontend Chat Proxy (/api/{userId}/chat)...');
        try {
            const chatResp = await axios.post(
                `${FRONTEND_URL}/api/${userId}/chat`,
                {
                    messages: [
                        { role: 'user', content: 'Reply with FRONTEND_PROXY_OK' }
                    ]
                },
                { headers }
            );
            console.log(`[PASS] Frontend chat proxy responded.`);
            console.log(`       Response preview: ${JSON.stringify(chatResp.data).substring(0, 100)}...`);
        } catch (e) {
            console.log(`[FAIL] Frontend chat proxy failed: ${e.response?.status} - ${e.response?.data || e.message}`);
        }

        // 4. Test Direct Backend Chat
        console.log('\n[STEP 4] Testing Direct Backend Chat (/api/{userId}/chat)...');
        try {
            const backendChatResp = await axios.post(
                `${BACKEND_URL}/api/${userId}/chat`,
                { message: 'Reply with BACKEND_DIRECT_OK' },
                { headers }
            );
            console.log(`[PASS] Backend chat responded.`);
            console.log(`       AI Response: ${backendChatResp.data.response}`);
        } catch (e) {
            console.log(`[FAIL] Backend chat failed: ${e.response?.status} - ${e.response?.data?.detail || e.message}`);
        }

        // 5. Test Backend Streaming
        console.log('\n[STEP 5] Testing Backend Streaming (/api/{userId}/chat/stream)...');
        try {
            const streamResp = await axios.post(
                `${BACKEND_URL}/api/${userId}/chat/stream`,
                { message: 'Reply with STREAM_OK' },
                {
                    headers,
                    responseType: 'stream'
                }
            );
            console.log(`[PASS] Backend streaming connection established.`);
            console.log('       Chunks: ', '');

            let chunks = '';
            streamResp.data.on('data', (chunk) => {
                chunks += chunk.toString();
            });

            await new Promise((resolve, reject) => {
                streamResp.data.on('end', () => {
                    console.log(`       Received ${chunks.length} bytes`);
                    resolve();
                });
                streamResp.data.on('error', reject);
            });
        } catch (e) {
            console.log(`[FAIL] Backend streaming failed: ${e.response?.status} - ${e.message}`);
        }

        console.log('\n' + '='.repeat(80));
        console.log('VERIFICATION COMPLETE');
        console.log('='.repeat(80));

    } catch (error) {
        console.error(`\n[ERROR] Verification failed: ${error.message}`);
        if (error.response) {
            console.error(`Response: ${error.response.status} - ${JSON.stringify(error.response.data)}`);
        }
    }
}

verifyFrontendChat();
