import { NextRequest, NextResponse } from "next/server";

export async function POST(
    request: NextRequest,
    props: { params: Promise<{ userId: string }> }
) {
    const params = await props.params;
    const userId = params.userId;

    try {
        const body = await request.json();

        // Vercel AI SDK sends data in specific format
        // It sends an array of messages, and we need the last one (the user's input)
        let message;
        let conversation_id = null;

        if (body.messages && Array.isArray(body.messages)) {
            // Get the last message (the current user input)
            const lastMessage = body.messages[body.messages.length - 1];
            if (lastMessage && lastMessage.content) {
                message = lastMessage.content;
            }

            // Check if there's conversation context in the messages
            // Look for any existing conversation ID or context
            for (const msg of body.messages) {
                if (msg.id && typeof msg.id === 'number') {
                    // This might be a conversation identifier
                    conversation_id = msg.id;
                    break;
                }
            }
        } else {
            // Fallback to other possible formats
            message = body.message || body.input || body.text;
            conversation_id = body.conversation_id || body.conversationId;
        }

        if (!message) {
            console.log('[CHAT-PROXY] No message found in request body:', JSON.stringify(body, null, 2));
            return NextResponse.json({ error: "No message found" }, { status: 400 });
        }

        const backendUrl = `${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat/stream`;

        // Forward authorization header
        const authHeader = request.headers.get('Authorization');

        console.log(`[CHAT-PROXY] Request to: ${backendUrl}`);
        console.log(`[CHAT-PROXY] Authorization: ${authHeader ? authHeader.substring(0, 20) + '...' : 'MISSING'}`);
        console.log(`[CHAT-PROXY] Message: ${message.substring(0, 50)}...`);

        const headers: Record<string, string> = {
            'Content-Type': 'application/json',
        };

        if (authHeader) {
            headers['Authorization'] = authHeader;
        }

        // Call backend endpoint with streaming enabled
        const backendResponse = await fetch(backendUrl, {
            method: 'POST',
            headers: headers,
            body: JSON.stringify({
                message: message,
                conversation_id: conversation_id || null // Use provided conversation_id or null
            }),
        });

        if (!backendResponse.ok) {
            const errorText = await backendResponse.text();
            console.error(`[CHAT-PROXY] Backend error: ${backendResponse.status} - ${errorText}`);

            // Return a user-friendly error message
            const userFriendlyError = {
                error: "Something went wrong with the AI service",
                userMessage: "The AI service is temporarily unavailable. Please try again in a moment.",
                details: errorText,
                timestamp: new Date().toISOString()
            };

            return NextResponse.json(userFriendlyError, { status: backendResponse.status });
        }

        // Directly forward the streaming response from backend to frontend
        // This preserves the streaming nature without intermediate processing
        const stream = backendResponse.body;

        if (!stream) {
            // Return a user-friendly error message
            const userFriendlyError = {
                error: "Stream connection failed",
                userMessage: "There was a problem connecting to the AI service. Please try again.",
                details: "Backend stream is null",
                timestamp: new Date().toISOString()
            };

            return new NextResponse(JSON.stringify(userFriendlyError), {
                status: 500,
                headers: {
                    'Content-Type': 'application/json',
                }
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
        console.error("[CHAT-PROXY] Error:", error);

        // Return a user-friendly error message
        const userFriendlyError = {
            error: "Connection error",
            userMessage: "There was a problem connecting to the AI service. Please check your internet connection and try again.",
            details: error.message || "Unknown error occurred",
            timestamp: new Date().toISOString()
        };

        return NextResponse.json(userFriendlyError, { status: 500 });
    }
}
