// ESLint 9.x Flat Config for Next.js
// This config works alongside .eslintrc.json
// Next.js uses .eslintrc.json, ESLint CLI can use this for additional rules

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
  
  // Lint TypeScript and JavaScript files
  {
    files: ["**/*.{js,jsx,ts,tsx}"],
    rules: {
      // General rules
      "no-console": ["warn", { allow: ["warn", "error"] }],
      "prefer-const": "warn",
    },
  },
];

export default eslintConfig;
