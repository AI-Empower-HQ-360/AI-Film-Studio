'use client';

import { Authenticator } from '@aws-amplify/ui-react';
import '@aws-amplify/ui-react/styles.css';
import { ReactNode } from 'react';

interface AmplifyAuthProviderProps {
  children: ReactNode;
}

/**
 * Amplify Gen 2 Authentication Provider
 * Wraps your app with authentication UI
 */
export function AmplifyAuthProvider({ children }: AmplifyAuthProviderProps) {
  return (
    <Authenticator
      signUpAttributes={['email', 'name']}
      loginMechanisms={['email']}
    >
      {({ signOut, user }) => (
        <div>
          {children}
        </div>
      )}
    </Authenticator>
  );
}

export { useAuthenticator } from '@aws-amplify/ui-react';
