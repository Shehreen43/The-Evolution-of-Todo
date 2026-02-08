const axios = require('axios');

const FRONTEND_URL = 'http://localhost:3000';
const BACKEND_URL = 'http://localhost:8000';

async function testChatEndpoint() {
    console.log('='.repeat(80));
    console.log('TESTING FIXED CHAT ENDPOINT');
    console.log('='.repeat(80));

    try {
        // 1. Authenticate
        console.log('\n[STEP 1] Authenticating...');
        const email = 'endpoint_test@example.com';
        const password = 'EndpointTest123!';

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
                name: 'Endpoint Tester'
            });
        }

        const token = authResp.data.token;
        const userId = authResp.data.user.id;
        console.log(`[PASS] Authenticated as ${userId}`);

        const headers = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json'
        };

        // 2. Test Fixed Frontend Chat Proxy
        console.log('\n[STEP 2] Testing FIXED Frontend Chat Proxy...');
        try {
            const chatResp = await axios.post(
                `${FRONTEND_URL}/api/${userId}/chat`,
                {
                    messages: [
                        { role: 'user', content: 'Say "PROXY_FIXED" if you can read this.' }
                    ]
                },
                {
                    headers,
                    responseType: 'stream',
                    timeout: 30000
                }
            );

            console.log(`[PASS] Frontend chat proxy connected (status: ${chatResp.status})`);
            console.log('       Streaming response: ', '');

            let fullResponse = '';
            chatResp.data.on('data', (chunk) => {
                const text = chunk.toString();
                fullResponse += text;
                process.stdout.write(text);
            });

            await new Promise((resolve, reject) => {
                chatResp.data.on('end', () => {
                    console.log(`\n[DONE] Received ${fullResponse.length} characters`);
                    resolve();
                });
                chatResp.data.on('error', (err) => {
                    console.error(`\n[FAIL] Stream error: ${err.message}`);
                    reject(err);
                });
                setTimeout(() => reject(new Error('Timeout')), 30000);
            });

        } catch (e) {
            if (e.response?.status === 429 || e.message?.includes('429')) {
                console.log(`[INFO] Hit rate limit (expected) - but connection worked!`);
            } else {
                console.log(`[FAIL] Frontend chat proxy failed: ${e.response?.status} - ${e.message}`);
            }
        }

        console.log('\n' + '='.repeat(80));
        console.log('TEST COMPLETE');
        console.log('='.repeat(80));

    } catch (error) {
        console.error(`\n[ERROR] Test failed: ${error.message}`);
        if (error.response) {
            console.error(`Response: ${error.response.status}`);
        }
    }
}

testChatEndpoint();
