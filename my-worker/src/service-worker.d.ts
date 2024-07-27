// service-worker.d.ts
declare var self: ServiceWorkerGlobalScope;
declare interface FetchEvent extends Event {
  readonly request: Request;
  readonly isReload: boolean;
  readonly clientId: string;
  readonly client: Client;
  respondWith(response: Promise<Response> | Response): void;
}
