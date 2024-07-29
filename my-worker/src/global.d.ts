// global.d.ts
export {};

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      VERCEL_DOMAIN: string;
      NOTIFICATIONS_API: string;
      USERNAME: string;
      PASWORD: string;
    }
  }
}