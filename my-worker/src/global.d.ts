// global.d.ts
export {};

declare global {
  namespace NodeJS {
    interface ProcessEnv {
      VERCEL_DOMAIN: string;
      NOTIFICATIONS_API: string;
      SECRET_TOKEN: string;
      AUTH_TOKEN: string; 
    }
  }
}
