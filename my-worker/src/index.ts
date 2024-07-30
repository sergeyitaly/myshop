const VERCEL_DOMAIN = (globalThis as any).VERCEL_DOMAIN as string;
const NOTIFICATIONS_API = (globalThis as any).NOTIFICATIONS_API as string;
const username = (globalThis as any).USERNAME as string;
const password = (globalThis as any).PASSWORD as string;

interface AuthData {
  access_token: string;
  refresh_token: string;
}

let accessToken: string = '';
let refreshToken: string = '';
let authToken: string = '';

interface TokenResponse {
  access?: string; 
}

let tokenExpiration: number | null = null;

const ACCESS_TOKEN_LIFETIME_IN_MINUTES = 4;
const ACCESS_TOKEN_LIFETIME_IN_MS = ACCESS_TOKEN_LIFETIME_IN_MINUTES * 60 * 1000;

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


interface AuthTokenResponse {
  auth_token: string;
}

interface User {
  phone: string;
  chat_id: string;
}

interface UserResponse {
  results: User[];
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

// Register the fetch event listener
addEventListener('fetch', (event: FetchEvent) => {
  event.respondWith(handleRequest(event));
});

// Register the scheduled event listener
addEventListener('scheduled', (event: ScheduledEvent) => {
  event.waitUntil(handleScheduled(event));
});

async function handleScheduled(event: ScheduledEvent): Promise<void> {
  console.log('Scheduled event triggered');
  await performHealthCheck();
  await updateGlobalAuthToken();
}

async function performHealthCheck(): Promise<void> {
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

async function authenticateWithCredentials(): Promise<AuthData | void> {
  const authUrl = `${(globalThis as any).VERCEL_DOMAIN}/api/token/`;
  try {
    const response = await fetch(authUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: new URLSearchParams({
        username: username,
        password: password,
      }),
    });

    console.log('Authentication response status:', response.status);
    if (!response.ok) { throw new Error(`Authentication failed with status ${response.status}`);}

    const data = await response.json() as AuthData;

    if (data.access_token && data.refresh_token) {return data;} 
    else {throw new Error('Invalid response format: Access token or refresh token missing.');}
    } catch (error) {console.error('Authenticate with cridentials. Error during authentication:', error);}
}

function isTokenResponse(data: any): data is TokenResponse {
  return data && typeof data === 'object' && 'access' in data;
}

async function getRefreshedToken(refreshToken: string | undefined): Promise<string | void> {
  const tokenRefreshUrl = `${(globalThis as any).VERCEL_DOMAIN}/api/token/refresh/`;

  if (!refreshToken) {
    console.error('GetRefreshedToken. No refresh token provided.');
    return;
  }

  console.log('Attempting to refresh token with refresh token:', refreshToken);

  try {
    const response = await fetch(tokenRefreshUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refresh: refreshToken }),
    });

    console.log('GetRefreshedToken. Token refresh response status:', response.status);

    if (!response.ok) {
      const responseClone = response.clone();
      const errorText = await responseClone.text();
      console.error(`Failed to refresh token: ${response.status} ${response.statusText}. Response body: ${errorText}`);
      return;
    }
    const data: unknown = await response.json();
    console.log('Token refresh response data:', data);

    if (isTokenResponse(data) && data.access) {
      console.log('Successfully refreshed token:', data.access);
      return data.access;
    } else {
      console.error('Invalid response format: Access token missing.');
    }
  } catch (error) {
    console.error('Error refreshing token:', error);
  }
}

async function updateGlobalAuthToken() {
  try {
    if (!accessToken || isTokenExpired()) {
      console.log('No valid auth token found or token expired. Authenticating with username and password...');
      const authData = await authenticateWithCredentials();

      if (authData) {
        refreshToken = authData.refresh_token;
        accessToken = authData.access_token;
        tokenExpiration = Date.now() + ACCESS_TOKEN_LIFETIME_IN_MS;
        console.log('Global access and refresh token updated successfully');
      } else {
        throw new Error('GlobalAuthToken. Authentication failed. No auth data received.');
      }
    } else {
      const newAccesToken = await getRefreshedToken(refreshToken);
      if (newAccesToken) {
        accessToken = newAccesToken;
        tokenExpiration = Date.now() + ACCESS_TOKEN_LIFETIME_IN_MS;
        console.log('Global access token updated successfully');
      } else {
        throw new Error('GlobalAuthToken.Failed to refresh auth token.');
      }
    }
  } catch (error) {
    console.error('GlobalAuthToken. Error updating global auth token:', error);
  }
}

function isTokenExpired(): boolean {
  return tokenExpiration === null || Date.now() > tokenExpiration;
}

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


async function handleRequest(event: FetchEvent): Promise<Response> {
  const url = new URL(event.request.url);
  const path = url.pathname;
  const method = event.request.method;
  const workerUrl = `${url.protocol}//${url.host}`;

  const webhookEndpoint = "/telegram_webhook/";

  if (method === "POST") {
    console.log('Handling POST request for webhook');
    const update: Update = await event.request.json();

    if (update.message && update.message.contact) {
      const phoneNumber = update.message.contact.phone_number;
      const chatId = update.message.chat.id;

      try {
        const userExistsFlag = await userExists(phoneNumber, chatId);

        if (userExistsFlag) {
          console.warn(`User with phone: ${phoneNumber} and chat ID: ${chatId} already exists.`);
          await updateGlobalAuthToken();
          await sendOrderDetails(phoneNumber, chatId); // Fetch and send order details based on phone number
        } else {
          console.log('Posting new user data to Vercel API');
          await updateGlobalAuthToken();
          await sendChatIdAndPhoneToVercel(phoneNumber, chatId);
        }
      } catch (error) {
        if (error instanceof Error) {
          console.error(`Error handling request: ${error.message}`);
        } else {
          console.error('An unknown error occurred');
        }
      }
    }

    event.waitUntil(processUpdate(update));
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

async function processUpdate(update: any): Promise<void> {
  console.log('Processing update:', update);

  if (update.message) {
    await processMessage(update.message);
  }
}



const phoneNumbers = new Map<string, string>();

async function processMessage(message: any): Promise<void> {
  const chatId = message.chat.id;

  if (message.contact) {
    const phoneNumber = message.contact.phone_number;
    const userExistsFlag = await userExists(phoneNumber, chatId);

    if (userExistsFlag) {
      console.warn(`User with phone: ${phoneNumber} and chat ID: ${chatId} already exists.`);
       } else {
               console.log('Posting new user data to Vercel API');
                await sendChatIdAndPhoneToVercel(phoneNumber, chatId);
               }

    // Store the phone number in the map
    phoneNumbers.set(chatId, phoneNumber);
    // Send the custom keyboard with "Order" and "Orders" buttons
       await sendCustomKeyboard(chatId);
       } // eof message.contact
  else if (message.text === '/start') {
        await sendMessage(message.chat.id, 'To get notifications, please share your phone number.');
        await sendContactRequest(message.chat.id);
         } 
        else if (message.text === 'Order') {
          const phoneNumber = phoneNumbers.get(chatId);
          if (phoneNumber) {
            await sendCustomKeyboard(message.chat.id);
            await updateGlobalAuthToken();
            await sendOrderDetails(phoneNumber, message.chat.id);
      // Ensure the custom keyboard is shown after sending the order details
               } 
            else {
               await sendMessage(message.chat.id, 'Phone number not found. Please share your phone number first.');
               await sendContactRequest(message.chat.id);
                  }
          } 
        else if (message.text === 'Orders') {
          const phoneNumber = phoneNumbers.get(chatId);
          if (phoneNumber) {
            // Ensure the custom keyboard is shown after sending all orders details
            await sendCustomKeyboard(message.chat.id);
            await updateGlobalAuthToken();
            await sendAllOrdersDetails(phoneNumber, message.chat.id);

            } 
            else {

               await sendMessage(message.chat.id, 'Phone number not found. Please share your phone number first.');
               await sendContactRequest(message.chat.id);
                }    
           } //eof message.text
        else {            await sendCustomKeyboard(message.chat.id);}
}

async function sendCustomKeyboard(chatId: string): Promise<void> {
  const url = `https://api.telegram.org/bot${NOTIFICATIONS_API}/sendMessage`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text: 'Choose an action:',
      reply_markup: {
        one_time_keyboard: true,
        resize_keyboard: true,
        keyboard: [
          [{ text: 'Order' }],
          [{ text: 'Orders' }]
        ]
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Failed to send custom keyboard: ${response.statusText}`);
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
        resize_keyboard: true,
        keyboard: [[{ text: 'Share phone number', request_contact: true }]]
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Failed to send contact request: ${response.statusText}`);
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
// Function to get the auth token
async function getAuthToken(): Promise<string> {
  const LOGIN_URL = `${VERCEL_DOMAIN}/auth/token/login/`;

  try {
    const response = await fetch(LOGIN_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username: username,
        password: password
      }),
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Failed to authenticate: ${response.statusText}. Response body: ${errorText}`);
      throw new Error(`Failed to authenticate: ${response.statusText}`);
    }
    const data = await response.json() as AuthTokenResponse; // Type assertion here
    authToken = data.auth_token;
    if (!authToken) {
      throw new Error('Token not found in response');
    }

    return authToken;
  } catch (error) {
    console.error(`Error getting auth token: ${error}`);
    throw error;
  }
}// Function to check if a user exists
async function userExists(phoneNumber: string, chatId: string): Promise<boolean> {
  const vercelUrl = `${VERCEL_DOMAIN}/api/telegram_users/`;
  const formattedPhoneNumber = phoneNumber.startsWith('+') ? phoneNumber : `+${phoneNumber}`;

  try {
    // Get the auth token
    const authToken = await getAuthToken();
    
    // Fetch users with the token
    const response = await fetch(vercelUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Token ${authToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Failed to fetch users from Vercel: ${response.statusText}. Response body: ${errorText}`);
      throw new Error(`Failed to fetch users from Vercel: ${response.statusText}`);
    }

    const data = await response.json() as UserResponse; // Type assertion here
    const users: User[] = data.results;

    // Check if a user with the given phone number or chat ID exists
    const userExistsByPhone = users.some(user => user.phone === formattedPhoneNumber);
    const userExistsByChatId = users.some(user => user.chat_id === chatId);

    return userExistsByPhone || userExistsByChatId;
  } catch (error) {
    console.error(`Error checking if user exists: ${error}`);
    throw error;
  }
}

// Function to send chat ID and phone number to Vercel
async function sendChatIdAndPhoneToVercel(phoneNumber: string, chatId: string): Promise<string | void> {
  try {
    // Check if the user already exists
    const userExistsAlready = await userExists(phoneNumber, chatId);
    if (userExistsAlready) {
      console.warn(`User with phone: ${phoneNumber} and chat ID: ${chatId} already exists.`);
      return 'exists';
    }

    const vercelUrl = `${VERCEL_DOMAIN}/api/telegram_users/`;
    console.log(`Posting data to Vercel API: ${vercelUrl}`);
    const formattedPhoneNumber = `+${phoneNumber.replace(/^\+/, '')}`;
    // Send data to Vercel
    const response = await fetch(vercelUrl, {
      method: 'POST',
      headers: {
        'Authorization': `Token ${authToken}`, // Use TokenAuthentication
        'Content-Type': 'application/json',
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

interface OrderItem {
  quantity: number;
  product_name: string;
  collection_name: string;
  size: string;
  color_name: string;
  color_value: string;
  item_price: string;
  total_sum: number;
}

interface Order {
  id: number;
  name: string;
  surname: string;
  phone: string;
  email: string;
  address: string | null;
  receiver: boolean;
  receiver_comments: string;
  submitted_at: string;
  parent_order: string | null;
  present: boolean;
  order_items: OrderItem[];
}

interface OrdersResponse {
  count: number;
  next: string | null;
  previous: string | null;
  results: Order[];
}

interface OrderDetails {
  id: number;
  email: string;
  order_items: OrderItem[];
  // Add other fields as needed
}
async function sendOrderDetails(phoneNumber: string, chatId: string): Promise<void> {
  const formattedPhoneNumber = phoneNumber.startsWith('+') ? phoneNumber : `+${phoneNumber}`;
  const ordersUrl = `${VERCEL_DOMAIN}/api/orders/`;

  try {
    // Ensure that accessToken is available and valid
    if (!accessToken) {
      console.error('No access token available.');
      await sendMessage(chatId, 'Authorization error. Please try again later.');
      return;
    }

    console.log(`Fetching orders from: ${ordersUrl}`);
    const response = await fetch(ordersUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`, // Use Bearer scheme for JWT
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Failed to retrieve orders. Status: ${response.status} ${response.statusText}. Response body: ${errorText}`);
      await sendMessage(chatId, 'Failed to retrieve orders. Please try again later.');
      return;
    }

    const ordersResponse = await response.json() as OrdersResponse; // Type assertion here
    const orders = ordersResponse.results;
    console.log(`Orders retrieved: ${JSON.stringify(orders)}`);

    const matchingOrder = orders.find(order => order.phone === formattedPhoneNumber);

    if (matchingOrder) {
      const orderDetailsUrl = `${VERCEL_DOMAIN}/api/orders/${matchingOrder.id}/`;
      console.log(`Fetching order details from: ${orderDetailsUrl}`);

      const orderDetailsResponse = await fetch(orderDetailsUrl, {
        method: 'GET',
        headers: {
          'Authorization': `Bearer ${accessToken}`, // Use Bearer scheme for JWT
          'Content-Type': 'application/json',
        },
      });

      if (!orderDetailsResponse.ok) {
        const errorText = await orderDetailsResponse.text();
        console.error(`Failed to retrieve order details. Status: ${orderDetailsResponse.status} ${orderDetailsResponse.statusText}. Response body: ${errorText}`);
        await sendMessage(chatId, 'Failed to retrieve order details. Please try again later.');
        return;
      }

      const orderDetails = await orderDetailsResponse.json() as OrderDetails; // Type assertion here
      console.log(`Order details retrieved: ${JSON.stringify(orderDetails)}`);

      const orderItemsSummary = orderDetails.order_items.map(item => 
        `- ${item.product_name}, ${item.collection_name}, ${item.size}, ${item.color_name}, ${item.quantity} pcs, ${parseFloat(item.item_price).toFixed(2)}`
      ).join('\n');
      const orderDetailsMessage = `
      Order ID: ${orderDetails.id}
      Email: ${orderDetails.email}
      
      Order Items:
      ${orderItemsSummary}

      `;
      
      await sendMessage(chatId, `Thank you! Here are your last order details:\n${orderDetailsMessage}`);
    } else {
      console.log('No orders found for this phone number.');
      await sendMessage(chatId, 'No orders found for this phone number.');
    }
  } catch (error) {
    console.error(`Error retrieving order details: ${error}`);
    await sendMessage(chatId, 'An error occurred while retrieving order details. Please try again later.');
  }
}

async function sendAllOrdersDetails(phoneNumber: string, chatId: string): Promise<void> {
  const ordersUrl = `${VERCEL_DOMAIN}/api/orders/`;
  const formattedPhoneNumber = phoneNumber.startsWith('+') ? phoneNumber : `+${phoneNumber}`;

  try {
    if (!accessToken) {
      console.error('No access token available.');
      await sendMessage(chatId, 'Authorization error. Please try again later.');
      return;
    }

    const response = await fetch(ordersUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`Failed to retrieve orders. Status: ${response.status} ${response.statusText}. Response body: ${errorText}`);
      await sendMessage(chatId, 'Failed to retrieve orders. Please try again later.');
      return;
    }

    const ordersResponse = await response.json() as OrdersResponse;
    const orders = ordersResponse.results.filter(order => order.phone === formattedPhoneNumber);

    // Function to format date
    const formatDate = (dateString: string): string => {
      const date = new Date(dateString);
      return date.toISOString().split('T')[0]; // YYYY-MM-DD format
    };

    if (orders.length > 0) {
      const ordersSummary = orders.map(order => 
        `Order ID: ${order.id}, Submitted at: ${formatDate(order.submitted_at)}`
      ).join('\n');
      await sendMessage(chatId, `Here are all your orders:\n${ordersSummary}`);
    } else {
      await sendMessage(chatId, 'No orders found for this phone number.');
    }
  } catch (error) {
    console.error(`Error retrieving orders: ${error}`);
    await sendMessage(chatId, 'An error occurred while retrieving orders. Please try again later.');
  }
}
