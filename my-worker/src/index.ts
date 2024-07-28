addEventListener('scheduled', (event: ScheduledEvent) => {
  event.waitUntil(handleScheduled(event));
});

async function handleScheduled(event: ScheduledEvent): Promise<void> {
  console.log('Cron job triggered');
  await performHealthCheck();
}

async function performHealthCheck(): Promise<void> {
  const VERCEL_DOMAIN = (globalThis as any).VERCEL_DOMAIN as string;
  const healthCheckUrl = `${VERCEL_DOMAIN}/api/health_check`;
  try {
    const response = await fetch(healthCheckUrl);
    if (response.ok) {
      console.log('Vercel health check successful');
    } else {
      console.error('Vercel health check failed:', response.statusText);
    }
  } catch (error) {
    console.error('Error performing health check:', error);
  }
}

interface Order {
  id: number;
  // Add other order properties as needed
}

addEventListener('fetch', (event: FetchEvent) => {
  event.respondWith(handleRequest(event));
});

async function setWebhook(event: FetchEvent, hashValue: string, webhookUrl: string): Promise<Response> {
  const url = new URL(event.request.url);
  url.pathname = `/${hashValue}/`;
  url.searchParams.set('command', 'setWebhook');
  url.searchParams.set('url', webhookUrl);

  const response = await fetch(url.toString());

  if (response.ok) {
    return new Response("Webhook set successfully", { status: 200 });
  } else {
    const errorText = await response.text();
    console.error('Failed to set webhook:', errorText);
    return new Response("Failed to set webhook", { status: response.status });
  }
}

async function getWebhook(event: FetchEvent, hashValue: string): Promise<Response> {
  const url = new URL(event.request.url);
  url.pathname = `/${hashValue}/`;
  url.searchParams.set('command', 'getWebhook');

  const response = await fetch(url.toString());

  if (response.ok) {
    const webhookInfo = await response.json();
    return new Response(JSON.stringify(webhookInfo), { status: 200 });
  } else {
    const errorText = await response.text();
    console.error('Failed to get webhook:', errorText);
    return new Response("Failed to get webhook", { status: response.status });
  }
}

async function deleteWebhook(event: FetchEvent, hashValue: string): Promise<Response> {
  const url = new URL(event.request.url);
  url.pathname = `/${hashValue}/`;
  url.searchParams.set('command', 'delWebhook');

  const response = await fetch(url.toString());

  if (response.ok) {
    return new Response("Webhook deleted successfully", { status: 200 });
  } else {
    const errorText = await response.text();
    console.error('Failed to delete webhook:', errorText);
    return new Response("Failed to delete webhook", { status: response.status });
  }
}

async function getMe(event: FetchEvent, hashValue: string): Promise<Response> {
  const url = new URL(event.request.url);
  url.pathname = `/${hashValue}/`;
  url.searchParams.set('command', 'getMe');

  const response = await fetch(url.toString());

  if (response.ok) {
    const botInfo = await response.json();
    return new Response(JSON.stringify(botInfo), { status: 200 });
  } else {
    const errorText = await response.text();
    console.error('Failed to get bot info:', errorText);
    return new Response("Failed to get bot info", { status: response.status });
  }
}

interface Contact {
  phone_number: string;
}

interface Message {
  contact?: Contact;
  chat: {
    id: string;
  };
}

interface Update {
  message?: Message;
}



interface OrderDetails {
  id: number;
  email: string;
  phone:string;
}
interface Order {
  id:number;
  email:string;
  phone:string;
}
async function handleRequest(event: FetchEvent): Promise<Response> {
  const url = new URL(event.request.url);
  const path = url.pathname;
  const method = event.request.method;
  const workerUrl = `${url.protocol}//${url.host}`;
  const VERCEL_DOMAIN = (globalThis as any).VERCEL_DOMAIN as string;
  const NOTIFICATIONS_API = (globalThis as any).NOTIFICATIONS_API as string;
  const AUTH_TOKEN = (globalThis as any).AUTH_TOKEN as string;

  const webhookEndpoint = "/telegram_webhook/";

  if (method === "POST") {
    console.log('Handling POST request for webhook');
    const update: Update = await event.request.json();

    if (update.message && update.message.contact) {
      const phoneNumber = update.message.contact.phone_number;
      const chatId = update.message.chat.id;

      try {
        if (await userExists(phoneNumber, chatId, VERCEL_DOMAIN, AUTH_TOKEN)) {
          console.warn(`User with phone: ${phoneNumber} and chat ID: ${chatId} already exists.`);
          await sendOrderDetails(chatId, phoneNumber, VERCEL_DOMAIN, AUTH_TOKEN, NOTIFICATIONS_API); // Assuming order details are in update.message.text
        } else {
          await sendChatIdAndPhoneToVercel(chatId, phoneNumber, VERCEL_DOMAIN, AUTH_TOKEN);
        }
      } catch (error) {
        if (error instanceof Error) {
          console.error(`Error sending data to Vercel: ${error.message}`);
        } else {
          console.error('An unknown error occurred');
        }
      }
    }

    event.waitUntil(processUpdate(update, NOTIFICATIONS_API, VERCEL_DOMAIN, AUTH_TOKEN));
    return new Response("Ok");
  } else if (method === "GET") {
    const command = url.searchParams.get("command");
    const hashValue = url.searchParams.get("hash_value");

    if (command && hashValue) {
      switch (command) {
        case "setWebhook":
          return await setWebhook(event, hashValue, workerUrl + webhookEndpoint);
        case "getWebhook":
          return await getWebhook(event, hashValue);
        case "delWebhook":
          return await deleteWebhook(event, hashValue);
        case "getMe":
          return await getMe(event, hashValue);
        default:
          return new Response("Invalid command", { status: 400 });
      }
    }
  }

  console.log('Path not found:', path);
  return new Response("Not found", { status: 404 });
}
async function processUpdate(update: any, NOTIFICATIONS_API: string, VERCEL_DOMAIN: string, AUTH_TOKEN: string): Promise<void> {
  console.log('Processing update:', update);

  if (update.message) {
    await processMessage(update.message, NOTIFICATIONS_API, VERCEL_DOMAIN, AUTH_TOKEN);
  }
}

async function processMessage(message: any, NOTIFICATIONS_API: string, VERCEL_DOMAIN: string, AUTH_TOKEN: string): Promise<void> {
  if (message.contact) {
    const phoneNumber = message.contact.phone_number;
    await sendChatIdAndPhoneToVercel(message.chat.id, phoneNumber, VERCEL_DOMAIN, AUTH_TOKEN);
  } else if (message.text === '/start') {
    await sendMessage(message.chat.id, 'To get notifications we need you share a phone number.', NOTIFICATIONS_API);
    await sendContactRequest(message.chat.id, NOTIFICATIONS_API);
  }
}

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
async function userExists(phoneNumber: string, chatId: string, VERCEL_DOMAIN: string, AUTH_TOKEN: string): Promise<boolean> {
  const vercelUrl = `${VERCEL_DOMAIN}/api/telegram_users/`;
  console.log(`Checking if user exists in Vercel API: ${vercelUrl}`);

  const formattedPhoneNumber = `+${phoneNumber.replace(/^\+/, '')}`;

  try {
    const response = await fetch(`${vercelUrl}?phone=${formattedPhoneNumber}&chat_id=${chatId}`, {
      method: 'GET',
      headers: {
        'Authorization': `Token ${AUTH_TOKEN}`
      }
    });

    console.error(`Failed to check if user exists: ${response.statusText}`);
    return false;
  } catch (error) {
    console.error(`Error checking if user exists: ${error}`);
    return false;
  }
}

async function sendChatIdAndPhoneToVercel(
  chatId: string,
  phoneNumber: string,
  VERCEL_DOMAIN: string,
  AUTH_TOKEN: string
): Promise<string | void> {
  const userExistsAlready = await userExists(phoneNumber, chatId, VERCEL_DOMAIN, AUTH_TOKEN);

  if (userExistsAlready) {
    console.warn(`User with phone: ${phoneNumber} and chat ID: ${chatId} already exists.`);
    return 'exists';
  }

  const vercelUrl = `${VERCEL_DOMAIN}/api/telegram_users/`;
  console.log(`Posting data to Vercel API: ${vercelUrl}`);

  const formattedPhoneNumber = `+${phoneNumber.replace(/^\+/, '')}`;

  try {
    const response = await fetch(vercelUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Token ${AUTH_TOKEN}`
      },
      body: JSON.stringify({ phone: formattedPhoneNumber, chat_id: chatId })
    });

    console.log(`Response status: ${response.status}`);

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Failed to send data to Vercel: ${response.statusText}. Response body: ${errorText}`);

      if (response.status === 400) {
        const errorBody = JSON.parse(errorText);
        if ((errorBody.phone && errorBody.phone.includes("telegram user with this phone already exists.")) ||
            (errorBody.chat_id && errorBody.chat_id.includes("telegram user with this chat id already exists."))) {
          console.warn(`User with phone: ${formattedPhoneNumber} and chat ID: ${chatId} already exists.`);
          return 'exists';
        }
      }

      throw new Error(`Failed to send data to Vercel: ${response.statusText}`);
    }

    return 'success';
  } catch (error) {
    console.error(`Error sending data to Vercel: ${error}`);
    throw error;
  }
}

async function sendOrderDetails(
  chatId: string,
  phoneNumber: string,
  VERCEL_DOMAIN: string,
  AUTH_TOKEN: string,
  NOTIFICATIONS_API: string
): Promise<void> {
  const formattedPhoneNumber = phoneNumber.startsWith('+') ? phoneNumber : `+${phoneNumber}`;
  const ordersUrl = `${VERCEL_DOMAIN}/api/orders/`;

  try {
    console.log(`Fetching orders from: ${ordersUrl}`);
    const response = await fetch(ordersUrl, {
      method: 'GET',
      headers: { 'Authorization': `Token ${AUTH_TOKEN}` }
    });

    if (!response.ok) {
      console.error(`Failed to retrieve orders. Status: ${response.status} ${response.statusText}`);
      await sendMessage(chatId, 'Failed to retrieve orders. Please try again later.', NOTIFICATIONS_API);
      return;
    }

    const orders = await response.json() as Order[];
    console.log(`Orders retrieved: ${JSON.stringify(orders)}`);

    const matchingOrder = orders.find(order => order.phone === formattedPhoneNumber);

    if (matchingOrder) {
      const orderDetailsUrl = `${VERCEL_DOMAIN}/api/order/${matchingOrder.id}/`;
      console.log(`Fetching order details from: ${orderDetailsUrl}`);

      const orderDetailsResponse = await fetch(orderDetailsUrl, {
        method: 'GET',
        headers: { 'Authorization': `Token ${AUTH_TOKEN}` }
      });

      if (!orderDetailsResponse.ok) {
        console.error(`Failed to retrieve order details. Status: ${orderDetailsResponse.status} ${orderDetailsResponse.statusText}`);
        await sendMessage(chatId, 'Failed to retrieve order details. Please try again later.', NOTIFICATIONS_API);
        return;
      }

      const orderDetails = await orderDetailsResponse.json() as OrderDetails;
      console.log(`Order details retrieved: ${JSON.stringify(orderDetails)}`);

      const orderDetailsMessage = `
        Order ID: ${orderDetails.id}
        Email: ${orderDetails.email}
        // Add more details as needed
      `;
      await sendMessage(chatId, `Thank you! Here is your last order: ${orderDetailsMessage}`, NOTIFICATIONS_API);
    } else {
      console.log('No orders found for this phone number.');
      await sendMessage(chatId, 'No orders found for this phone number.', NOTIFICATIONS_API);
    }
  } catch (error) {
    console.error(`Error retrieving order details: ${error}`);
    await sendMessage(chatId, 'An error occurred while retrieving order details. Please try again later.', NOTIFICATIONS_API);
  }
}

interface OrderDetails {
  id: number;
  email: string;
  phone: string;
}
interface Order {
  id: number;
  email: string;
  phone: string;
}

interface TelegramUpdate {
  update_id: number;
  message?: TelegramMessage;
}

interface TelegramMessage {
  message_id: number;
  chat: {
    id: string;
  };
  text?: string;
  contact?: {
    phone_number: string;
  };
}