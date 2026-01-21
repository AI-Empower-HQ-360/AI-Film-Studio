import { type ClientSchema, a, defineData } from '@aws-amplify/backend';

/**
 * Data schema for AI Film Studio
 */
const schema = a.schema({
  Project: a
    .model({
      title: a.string().required(),
      script: a.string().required(),
      status: a.enum(['draft', 'processing', 'completed', 'failed']),
      videoUrl: a.url(),
      thumbnailUrl: a.url(),
      settings: a.json(),
      userId: a.string().required(),
      createdAt: a.datetime(),
      updatedAt: a.datetime(),
    })
    .authorization((allow) => [
      allow.owner(),
      allow.authenticated().to(['read']),
    ]),

  Job: a
    .model({
      projectId: a.id().required(),
      status: a.enum(['submitted', 'queued', 'processing', 'completed', 'failed']),
      progress: a.integer(),
      errorMessage: a.string(),
      resultUrl: a.url(),
      userId: a.string().required(),
      createdAt: a.datetime(),
      updatedAt: a.datetime(),
    })
    .authorization((allow) => [allow.owner()]),
});

export type Schema = ClientSchema<typeof schema>;

export const data = defineData({
  schema,
  authorizationModes: {
    defaultAuthorizationMode: 'userPool',
  },
});
