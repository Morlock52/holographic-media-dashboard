/**
 * Mock ChatbotAPIClient for media-assistant.html
 * This provides a fake implementation to allow the chat UI to be tested
 * without a real backend.
 */
class ChatbotAPIClient {
    constructor(options = {}) {
        console.log('Mock ChatbotAPIClient initialized with options:', options);
        this.eventListeners = new Map();
        this.isHealthy = true;
        this.fallback = false;
    }

    on(eventName, callback) {
        if (!this.eventListeners.has(eventName)) {
            this.eventListeners.set(eventName, []);
        }
        this.eventListeners.get(eventName).push(callback);
    }

    emit(eventName, data) {
        if (this.eventListeners.has(eventName)) {
            this.eventListeners.get(eventName).forEach(callback => callback(data));
        }
    }

    async healthCheck() {
        return { healthy: this.isHealthy };
    }

    async sendMessage(message, history, options) {
        console.log('Mock sendMessage called with:', { message, history, options });
        this.emit('request-start');

        // Simulate network delay
        await new Promise(resolve => setTimeout(resolve, 800 + (Math.random() * 500)));

        const response = {
            data: {
                response: `This is a mock response to your message: "${message}". In a real application, an AI would provide a more detailed answer here.`,
                usage: {
                    prompt_tokens: 50,
                    completion_tokens: 30,
                    total_tokens: 80
                }
            },
            fallback: this.fallback,
        };

        this.emit('request-success', response);
        return response;
    }
}

// Export for browser
if (typeof window !== 'undefined') {
    window.ChatbotAPIClient = ChatbotAPIClient;
}
