import { defineAuth } from '@aws-amplify/backend';

/**
 * Authentication configuration for AI Film Studio
 */
export const auth = defineAuth({
  loginWith: {
    email: true,
  },
  userAttributes: {
    email: {
      required: true,
      mutable: true,
    },
    name: {
      required: true,
      mutable: true,
    },
    'custom:subscription_tier': {
      dataType: 'String',
      mutable: true,
    },
    'custom:credits': {
      dataType: 'Number',
      mutable: true,
    },
  },
});
