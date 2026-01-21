import { defineBackend } from '@aws-amplify/backend';
import { auth } from './auth/resource';
import { data } from './data/resource';

/**
 * AI Film Studio - Amplify Gen 2 Backend Configuration
 * @see https://docs.amplify.aws/gen2
 */
const backend = defineBackend({
  auth,
  data,
});

// Configure custom domain and headers
backend.addOutput({
  custom: {
    API: {
      url: process.env.NEXT_PUBLIC_API_URL || 'https://api-prod.aifilmstudio.com',
      websocket: process.env.NEXT_PUBLIC_WS_URL || 'wss://api-prod.aifilmstudio.com',
    },
  },
});
