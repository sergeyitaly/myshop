import dotenv from 'dotenv';
import { URL } from 'url';

// Load environment variables
dotenv.config({ path: './.env' });

const WEBHOOK = '/telegram_webhook/';
const SECRET_TOKEN = process.env.SECRET_TOKEN;
const NOTIFICATIONS_API = process.env.NOTIFICATIONS_API;
const VERCEL_DOMAIN = process.env.VERCEL_DOMAIN;

addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  if (url.pathname === WEBHOOK) {
    event.respondWith(handleWebhook(event));
  } else if (url.pathname === '/registerWebhook') {
    event.respondWith(registerWebhook(event, url, WEBHOOK, SECRET_TOKEN));
  } else if (url.pathname === '/unRegisterWebhook') {
    event.respondWith(unRegisterWebhook(event));
  } else if (url.pathname === '/favicon.ico') {
    // Serve favicon.ico with minimal overhead
    event.respondWith(new Response('Favicon not available', { status: 404 }));
  } else {
    event.respondWith(new Response('Not Found', { status: 404 }));
  }
});

async function handleWebhook(event: FetchEvent): Promise<Response> {
  // Check secret token
  const secretToken = event.request.headers.get('X-Telegram-Bot-Api-Secret-Token');
  if (secretToken !== SECRET_TOKEN) {
    return new Response('Unauthorized', { status: 403 });
  }

  try {
    const update = await event.request.json();
    console.log('Update received:', update);

    if ('message' in update) {
      await processMessage(update.message);
    }
    
    return new Response('Ok');
  } catch (error) {
    console.error('Error handling webhook:', error);
    return new Response('Internal Server Error', { status: 500 });
  }
}

async function processMessage(message: any): Promise<void> {
  if (message.contact) {
    const phoneNumber = message.contact.phone_number;
    await sendChatIdAndPhoneToVercel(message.chat.id, phoneNumber);
    await sendMessage(message.chat.id, 'Thank you! Your phone number has been recorded.');
  } else if (message.text === '/start') {
    await sendMessage(message.chat.id, 'Please share your phone number using the contact button below.');
    await sendContactRequest(message.chat.id);
  }
}

async function sendMessage(chatId: string, text: string): Promise<void> {
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

async function sendContactRequest(chatId: string): Promise<void> {
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

async function sendChatIdAndPhoneToVercel(chatId: string, phoneNumber: string): Promise<void> {
  const vercelUrl = `${VERCEL_DOMAIN}/telegram_webhook/`;
  const response = await fetch(vercelUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ chatId, phoneNumber })
  });

  if (!response.ok) {
    throw new Error(`Failed to send data to Vercel: ${response.statusText}`);
  }
}

async function registerWebhook(event: FetchEvent, requestUrl: URL, suffix: string, secret: string): Promise<Response> {
  const webhookUrl = `${requestUrl.protocol}//${requestUrl.hostname}${suffix}`;
  const response = await fetch(apiUrl('setWebhook', { url: webhookUrl, secret_token: secret }));
  const result = await response.json();
  return new Response(result.ok ? 'Ok' : JSON.stringify(result, null, 2));
}

async function unRegisterWebhook(event: FetchEvent): Promise<Response> {
  const response = await fetch(apiUrl('setWebhook', { url: '' }));
  const result = await response.json();
  return new Response(result.ok ? 'Ok' : JSON.stringify(result, null, 2));
}

function apiUrl(methodName: string, params: any = null): string {
  const query = params ? '?' + new URLSearchParams(params).toString() : '';
  return `https://api.telegram.org/bot${NOTIFICATIONS_API}/${methodName}${query}`;
}
