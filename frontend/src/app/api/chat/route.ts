import { NextRequest, NextResponse } from "next/server";

export async function POST(request: NextRequest) {
  try {
    const body = await request.json();
    const { messages, userId, token } = body;  // Get token from request body

    // Get the last message as the user input
    const lastMessage = messages[messages.length - 1];
    if (!lastMessage) {
      return NextResponse.json({ error: "No message found" }, { status: 400 });
    }

    // Extract conversation ID from existing messages if available
    let conversationId = null;
    // Look for an existing conversation ID in the message history
    for (const msg of messages) {
      if (msg.id && typeof msg.id === 'number') {
        // This could be conversation ID if it's a numeric ID from backend
        conversationId = msg.id;
        break;
      }
    }

    // Construct the backend URL - use the regular endpoint which supports tools
    const backendUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat`;

    console.log(`[AI-SDK-PROXY] Request to: ${backendUrl}`);
    console.log(`[AI-SDK-PROXY] Token: ${token ? token.substring(0, 20) + '...' : 'MISSING'}`);
    console.log(`[AI-SDK-PROXY] Message: ${lastMessage.content.substring(0, 50)}...`);
    console.log(`[AI-SDK-PROXY] Conversation ID: ${conversationId}`);

    // Create headers with authorization
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    } else {
      console.warn('[AI-SDK-PROXY] No token found in request body!');
      return NextResponse.json({ error: "Authentication token required" }, { status: 401 });
    }

    // Call backend endpoint with streaming enabled
    const backendResponse = await fetch(backendUrl, {
      method: 'POST',
      headers: headers,
      body: JSON.stringify({
        message: lastMessage.content,
        conversation_id: conversationId,
        stream: true  // Enable streaming
      }),
    });

    if (!backendResponse.ok) {
      const errorText = await backendResponse.text();
      console.error(`[AI-SDK-PROXY] Backend error: ${backendResponse.status} - ${errorText}`);
      return NextResponse.json({ error: errorText }, { status: backendResponse.status });
    }

    // Directly forward the streaming response from backend to frontend
    // This preserves the streaming nature without intermediate processing
    const stream = backendResponse.body;

    if (!stream) {
      return new NextResponse(null, {
        status: 500,
        statusText: "Backend stream is null"
      });
    }

    return new NextResponse(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'X-Accel-Buffering': 'no', // Disable nginx buffering
      },
    });

  } catch (error: any) {
    console.error("[AI-SDK-PROXY] Error:", error);
    return NextResponse.json({ error: "Internal Server Error" }, { status: 500 });
  }
}