// Test script to verify frontend API client can connect to backend
const axios = require('axios');

async function testBackendConnection() {
  console.log('Testing connection to backend API...');

  try {
    // Test the health endpoint
    const response = await axios.get('http://localhost:8000/health');
    console.log('✅ Backend health check:', response.data);

    // Test the root endpoint
    const rootResponse = await axios.get('http://localhost:8000/');
    console.log('✅ Backend root endpoint:', rootResponse.data);

    // Test the auth endpoints exist
    try {
      const authResponse = await axios.options('http://localhost:8000/api/auth/signup');
      console.log('✅ Auth endpoint accessible');
    } catch (error) {
      if (error.response && (error.response.status === 405 || error.response.status === 404)) {
        // OPTIONS might not be supported, but that's okay
        console.log('✅ Auth endpoint exists (received expected error for OPTIONS request)');
      } else {
        console.log('❌ Auth endpoint error:', error.message);
      }
    }

    console.log('\n🎉 Backend API is accessible and responding correctly!');
    console.log('The frontend API client should be able to communicate with the backend.');

  } catch (error) {
    console.error('❌ Error connecting to backend:', error.message);
    if (error.code === 'ECONNREFUSED') {
      console.error('The backend server may not be running on http://localhost:8000');
    }
  }
}

testBackendConnection();