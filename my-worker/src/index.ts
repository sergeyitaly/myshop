self.addEventListener('fetch', (event: FetchEvent) => {
  event.respondWith(handleRequest(event));
});

async function handleRequest(event: FetchEvent): Promise<Response> {
  const url = new URL(event.request.url);

  // Access environment variables
  const VERCEL_DOMAIN = (globalThis as any).VERCEL_DOMAIN as string;
  const NOTIFICATIONS_API = (globalThis as any).NOTIFICATIONS_API as string;
  const SECRET_TOKEN = (globalThis as any).SECRET_TOKEN as string;
  const AUTH_TOKEN = (globalThis as any).AUTH_TOKEN as string;

  const WEBHOOK = "/telegram_webhook/";

  if (url.pathname === WEBHOOK) {
    return handleWebhook(event, SECRET_TOKEN, NOTIFICATIONS_API, VERCEL_DOMAIN, AUTH_TOKEN);
  } else if (url.pathname === '/registerWebhook') {
    return registerWebhook(event, url, WEBHOOK, SECRET_TOKEN, NOTIFICATIONS_API);
  } else if (url.pathname === '/unRegisterWebhook') {
    return unRegisterWebhook(event, NOTIFICATIONS_API);
  } else if (url.pathname === '/processUpdates') {
    return processPendingUpdates(NOTIFICATIONS_API, VERCEL_DOMAIN, AUTH_TOKEN);
  } else if (url.pathname === '/favicon.ico') {
    return new Response('Favicon not available', { status: 404 });
  } else {
    return new Response('Not Found', { status: 404 });
  }
}

// Handle webhook requests
async function handleWebhook(event: FetchEvent, SECRET_TOKEN: string, NOTIFICATIONS_API: string, VERCEL_DOMAIN: string, AUTH_TOKEN: string): Promise<Response> {
  const secretToken = event.request.headers.get('X-Telegram-Bot-Api-Secret-Token');
  if (secretToken !== SECRET_TOKEN) {
    return new Response('Unauthorized', { status: 403 });
  }

  try {
    const update: TelegramUpdate = await event.request.json();
    console.log('Update received:', update);

    if (update.message) {
      await processMessage(update.message, NOTIFICATIONS_API, VERCEL_DOMAIN, AUTH_TOKEN);
    }

    return new Response('Ok');
  } catch (error) {
    console.error('Error handling webhook:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
}

// Process pending updates
async function processPendingUpdates(NOTIFICATIONS_API: string, VERCEL_DOMAIN: string, AUTH_TOKEN: string): Promise<Response> {
  const url = `https://api.telegram.org/bot${NOTIFICATIONS_API}/getUpdates`;
  const response = await fetch(url);
  const result = await response.json() as TelegramApiResponse;

  if (result.ok && result.result) {
    const updates = result.result;
    for (const update of updates) {
      if (update.message) {
        await processMessage(update.message, NOTIFICATIONS_API, VERCEL_DOMAIN, AUTH_TOKEN);
      }
    }
    return new Response('Updates processed');
  } else {
    return new Response('Failed to fetch updates', { status: 500 });
  }
}

// Process incoming messages
async function processMessage(message: TelegramMessage, NOTIFICATIONS_API: string, VERCEL_DOMAIN: string, AUTH_TOKEN: string): Promise<void> {
  if (message.contact) {
    const phoneNumber = message.contact.phone_number;
    await sendChatIdAndPhoneToVercel(message.chat.id, phoneNumber, VERCEL_DOMAIN, AUTH_TOKEN);
    await sendMessage(message.chat.id, 'Thank you! Your phone number has been recorded.', NOTIFICATIONS_API);
  } else if (message.text === '/start') {
    await sendMessage(message.chat.id, 'Please share your phone number using the contact button below.', NOTIFICATIONS_API);
    await sendContactRequest(message.chat.id, NOTIFICATIONS_API);
  }
}

// Send a message to a chat
async function sendMessage(chatId: string, text: string, NOTIFICATIONS_API: string): Promise<void> {
  const url = `https://api.telegram.org/bot${NOTIFICATIONS_API}/sendMessage`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chat_id: chatId, text })
  });

  if (!response.ok) {
    throw new Error(`Failed to send message: ${response.statusText}`);
  }
}

// Send a contact request to a chat
async function sendContactRequest(chatId: string, NOTIFICATIONS_API: string): Promise<void> {
  const url = `https://api.telegram.org/bot${NOTIFICATIONS_API}/sendMessage`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text: 'Please share your phone number:',
      reply_markup: {
        one_time_keyboard: true,
        keyboard: [[{ text: 'Share phone number', request_contact: true }]]
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Failed to send contact request: ${response.statusText}`);
  }
}

// Send chat ID and phone number to Vercel
async function sendChatIdAndPhoneToVercel(chatId: string, phoneNumber: string, VERCEL_DOMAIN: string, AUTH_TOKEN: string): Promise<void> {
  const vercelUrl = `${VERCEL_DOMAIN}/api/telegram_users/`;
  console.log(`Posting data to Vercel API: ${vercelUrl}`);
  
  const response = await fetch(vercelUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Token ${AUTH_TOKEN}`  // Pass the AUTH_TOKEN as a parameter
    },
    body: JSON.stringify({ chatId, phoneNumber })
  });

  console.log(`Response status: ${response.status}`);
  if (!response.ok) {
    const errorText = await response.text();
    console.error(`Failed to send data to Vercel: ${response.statusText}. Response body: ${errorText}`);
    throw new Error(`Failed to send data to Vercel: ${response.statusText}`);
  }
}

// Register a webhook with Telegram
async function registerWebhook(event: FetchEvent, requestUrl: URL, suffix: string, secret: string, NOTIFICATIONS_API: string): Promise<Response> {
  const webhookUrl = `${requestUrl.protocol}//${requestUrl.hostname}${suffix}`;
  const response = await fetch(apiUrl('setWebhook', { url: webhookUrl, secret_token: secret }, NOTIFICATIONS_API));
  const result = await response.json() as TelegramApiResponse;

  return new Response(result.ok ? 'Ok' : JSON.stringify(result, null, 2));
}

// Unregister a webhook with Telegram
async function unRegisterWebhook(event: FetchEvent, NOTIFICATIONS_API: string): Promise<Response> {
  const response = await fetch(apiUrl('setWebhook', { url: '' }, NOTIFICATIONS_API));
  const result = await response.json() as TelegramApiResponse;

  return new Response(result.ok ? 'Ok' : JSON.stringify(result, null, 2));
}

// Build the API URL
function apiUrl(methodName: string, params: any = null, NOTIFICATIONS_API: string): string {
  const query = params ? '?' + new URLSearchParams(params).toString() : '';
  return `https://api.telegram.org/bot${NOTIFICATIONS_API}/${methodName}${query}`;
}

// Define interfaces
interface TelegramApiResponse {
  ok: boolean;
  result?: any;
  description?: string;
}

interface TelegramUpdate {
  update_id: number;
  message?: TelegramMessage;
  // Add other properties if needed
}

interface TelegramMessage {
  chat: { id: string };
  text?: string;
  contact?: { phone_number: string };
  // Add other properties if needed
}
