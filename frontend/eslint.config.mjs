// ESLint 9.x Flat Config for Next.js
// This is a minimal flat config that works with ESLint 9.x
// Next.js will use .eslintrc.json, but this provides additional rules

const eslintConfig = [
  // Ignore patterns (must be first in flat config)
  {
    ignores: [
      "node_modules/**",
      ".next/**",
      "out/**",
      "dist/**",
      "build/**",
      "*.config.js",
      "*.config.mjs",
      "*.config.ts",
      "*.config.cjs",
      "public/**",
      "coverage/**",
      ".turbo/**",
      ".eslintrc.json.bak",
    ],
  },
  
  // Custom rules (Next.js rules come from .eslintrc.json)
  {
    rules: {
      // TypeScript rules
      "@typescript-eslint/no-unused-vars": [
        "warn",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
        },
      ],
      "@typescript-eslint/no-explicit-any": "warn",
      
      // React rules
      "react/no-unescaped-entities": "warn",
      "react-hooks/exhaustive-deps": "warn",
      
      // General rules
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "prefer-const": "warn",
    },
  },
];

export default eslintConfig;
