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

let tokenExpiration: number = 0;

const ACCESS_TOKEN_LIFETIME_IN_MINUTES = 5;
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


let lastHealthCheckStatus: 'success' | 'failure' | 'unknown' = 'unknown';
let cachedChatIds: Set<string> = new Set<string>();



interface ApiResponse {
  results?: UsersIDs[];
  users?: UsersIDs[];
}

interface UsersIDs {
  chat_id: string;
}

interface ApiResponseVercel {
  results?: User[];
  users?: User[];
}

interface UserNotify {
  chat_id: string;
  phone: string;
}

interface ApiResponseVercelNotify {
  results?: UserNotify[];
  users?: UserNotify[];
}

const phoneNumbers = new Map<string, string>();
const chatIds = new Set<string>();
let orderPageNumber: number = 1;


// Define the expected response type from the API
interface ChatIdResponse {
  chat_ids: string[]; // Assuming the response contains a `chat_ids` array
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
  await updateGlobalAuthToken();
  await performHealthCheck();
 // await updateSubmittedToCreated();
 // await updateCreatedToProcessed();
 // await updateProcessedToComplete();
}

async function fetchChatIds(): Promise<Set<string>> {
  const vercelUrl = `${VERCEL_DOMAIN}/api/telegram_users/`;
  await updateGlobalAuthToken();

  try {

    const response = await fetch(vercelUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Token ${authToken}`, // Use TokenAuthentication
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch data from Vercel: ${response.statusText}`);
    }

    const data = await response.json() as ApiResponseVercelNotify;
    console.log('Fetched data:', data);

    let chatIds: string[] = [];
    if (data.results && Array.isArray(data.results)) {
      chatIds = data.results.map((user: UserNotify) => user.chat_id);

    } else if (data.users && Array.isArray(data.users)) {
      chatIds = data.users.map((user: UserNotify) => user.chat_id);
    } else {
      throw new Error('Unexpected data structure');
    }

    return new Set(chatIds);
  } catch (error) {
    console.error(`Error fetching chat IDs from Vercel: ${error}`);
    return new Set(); // Return the empty set on error
  }
}

async function sendNotificationToAllUsers(chatIds: Set<string>, message: string): Promise<void> {
  await updateGlobalAuthToken();

  for (const chatId of chatIds) {
    try {
      const url = `https://api.telegram.org/bot${NOTIFICATIONS_API}/sendMessage`;
      const response = await fetch(url, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          chat_id: chatId,
          text: message,
        }),
      });

      if (!response.ok) {
        throw new Error(`Failed to send Telegram notification to chat ID ${chatId}: ${response.statusText}`);
      }
    } catch (error) {
      console.error(`Error sending notification to chat ID ${chatId}: ${error}`);
    }
  }
}
async function performHealthCheck(): Promise<void> {
  const healthCheckUrl = `${VERCEL_DOMAIN}/api/health_check`;
  try {
    const response = await fetch(healthCheckUrl);
    if (response.ok) {
      console.log('Vercel health check successful');

      if (lastHealthCheckStatus === 'failure') {
        const successMessage = '✅ Server up and running!';
        // Ensure cachedChatIds is not empty before sending notifications
        if (cachedChatIds.size > 0) {
          await sendNotificationToAllUsers(cachedChatIds, successMessage);
        }
        lastHealthCheckStatus = 'success';
      }

      cachedChatIds = await fetchChatIds();
    } else {
      const errorMessage = `🚨 Server is down: ${response.statusText}`;
      console.error(errorMessage);

      if (lastHealthCheckStatus !== 'failure') {
        // Ensure cachedChatIds is not empty before sending notifications
        if (cachedChatIds.size > 0) {
          await sendNotificationToAllUsers(cachedChatIds, errorMessage);
        }
        lastHealthCheckStatus = 'failure';
      }
    }
  } catch (error) {
    const errorMessage = `❗ Error performing health check: ${error}`;
    console.error(errorMessage);

    if (lastHealthCheckStatus !== 'failure') {
      // Ensure cachedChatIds is not empty before sending notifications
      if (cachedChatIds.size > 0) {
        await sendNotificationToAllUsers(cachedChatIds, errorMessage);
      }
      lastHealthCheckStatus = 'failure';
    }
  }
}


// Other functions (updateGlobalAuthToken, updateSubmittedToCreated, etc.) should be defined elsewhere in your code.

async function getHealthStatus(): Promise<string> {
  const healthCheckUrl = `${VERCEL_DOMAIN}/api/health_check`;
  try {
    const response = await fetch(healthCheckUrl);
    if (response.ok) {
      return '✅ Server up and running!';
    } else {
      return `🚨 Server is down: ${response.statusText}`;
    }
  } catch (error) {
    return `❗ Error performing health check: ${error}`;
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
  return accessToken === null || Date.now() > tokenExpiration;
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



async function fetchPhoneNumbersFromVercel(): Promise<string[]> {
  const vercelUrl = `${VERCEL_DOMAIN}/api/telegram_users/`;

  try {
    await updateGlobalAuthToken();
    const response = await fetch(vercelUrl, {
      method: 'GET',
      headers: {
        'Authorization': `Token ${authToken}`, // Use TokenAuthentication
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to fetch data from Vercel: ${response.statusText}`);
    }

    const data = await response.json() as ApiResponseVercel; // Explicitly cast the response to ApiResponse
    console.log('Fetched data:', data);

    if (data.results && Array.isArray(data.results)) {
      return data.results.map((user: User) => user.phone);
    } else if (data.users && Array.isArray(data.users)) {
      return data.users.map((user: User) => user.phone);
    } else {
      throw new Error('Unexpected data structure');
    }
  } catch (error) {
    console.error(`Error fetching data from Vercel: ${error}`);
    throw error;
  }
}

async function processUpdate(update: any): Promise<void> {
  if (update.message) {
    await processMessage(update.message);
  } else if (update.callback_query) {

    await processCallbackQuery(update.callback_query);
  }
}




// Function to check if a chat ID is registered
async function isChatIdRegistered(chatId: string): Promise<boolean> {
  const url = `${VERCEL_DOMAIN}/api/telegram_users`;

  try {
    await updateGlobalAuthToken();
    const response = await fetch(url, {
      method: 'GET',
      headers: { 'Content-Type': 'application/json' },
    });

    if (response.ok) {
      // Parse the JSON response
      const data = await response.json();

      // Type guard function to check if data matches ChatIdResponse
      function isChatIdResponse(data: any): data is ChatIdResponse {
        return data && Array.isArray(data.chat_ids);
      }

      if (isChatIdResponse(data)) {
        // Check if the chatId is included in the array of registered chat IDs
        return data.chat_ids.includes(chatId);
      } else {
        console.error('Unexpected response format from API.');
        return false;
      }
    } else {
      console.error(`Failed to fetch chat IDs: ${response.statusText}`);
      return false;
    }
  } catch (error: unknown) {
    if (error instanceof Error) {
      console.error(`Error fetching chat IDs: ${error.message}`);
    } else {
      console.error(`Unknown error occurred: ${error}`);
    }
    return false;
  }
}


async function processMessage(message: any): Promise<void> {
  const chatId = message.chat.id;

  if (message.contact) {
    await updateGlobalAuthToken();
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
    chatIds.add(chatId);

    // Send the custom keyboard with "Order", "Orders", and "KOLORYT" buttons
    await sendCustomKeyboard(chatId);

  } else if (message.text === 'Start') {
    const isRegistered = await isChatIdRegistered(chatId);
    if (!isRegistered) {
      await sendMessage(chatId, '📞 To get notifications, please share your phone number.');
      await sendContactRequest(chatId);
    } else {
      await sendMessage(chatId, 'You are already registered.');
    }

  } else if (message.text === 'Order') {
    await updateGlobalAuthToken();
    const phoneNumber = phoneNumbers.get(chatId);
    if (phoneNumber) {
      await sendOrderDetails(phoneNumber, chatId);
    } else {
      await sendMessage(chatId, '🔍 Phone number not found. Please share your phone number first.');
      await sendContactRequest(chatId);
    }

  } else if (message.text === 'Orders') {
    await updateGlobalAuthToken();
    const phoneNumber = phoneNumbers.get(chatId);
    if (phoneNumber) {
      await sendAllOrdersDetails(chatId);
    } else {
      await sendMessage(chatId, '🔍 Phone number not found. Please share your phone number first.');
      await sendContactRequest(chatId);
    }

  } else if (message.text === 'KOLORYT') {
    await sendMessage(chatId, `You can proceed to KOLORYT here: \n${VERCEL_DOMAIN}`);
    try {
      const healthStatus = await getHealthStatus();
      await sendMessage(chatId, `Current status:\n${healthStatus}`);
    } catch (error) {
      await sendMessage(chatId, '⚠️ Unable to fetch server status at the moment.');
    }

  } else if (message.text === '/telegram_users') {
    try {
      await updateGlobalAuthToken();
      const allPhoneNumbers = await fetchPhoneNumbersFromVercel();
      const phoneNumberList = allPhoneNumbers.join('\n');
      await sendMessage(chatId, `Registered phone numbers:\n${phoneNumberList}`);
    } catch (error) {
      await sendMessage(chatId, '⚠️ Failed to retrieve phone numbers. Please try again later.');
    }
  } else {
    // Send the custom keyboard with correct options
    await sendCustomKeyboard(chatId);
  }
}

async function processCallbackQuery(callbackQuery: any): Promise<void> {
  await updateGlobalAuthToken();
  const chatId = callbackQuery.message.chat.id;
  const callbackData = callbackQuery.data;
  const phoneNumber = phoneNumbers.get(chatId);


  if (!phoneNumber) {
    await sendMessage(chatId, '🔍 Phone number not found. Please share your phone number first.');
    await sendContactRequest(chatId);

    return;
  }

  if (callbackData === 'Order') {
    await updateGlobalAuthToken();
    await sendOrderDetails(phoneNumber, chatId);
  } else if (callbackData === 'Orders') {
    await sendAllOrdersDetails(chatId);
  } else if (callbackData === 'Start') {
    await updateGlobalAuthToken();
    await sendMessage(chatId, '📞 To get notifications, please share your phone number.');
    await sendContactRequest(chatId);
  } else {
    await sendMessage(chatId, '⚠️ Unknown action.');
  }

  // Acknowledge that the callback query has been processed
  await acknowledgeCallbackQuery(callbackQuery.id);
}

async function acknowledgeCallbackQuery(callbackQueryId: string): Promise<void> {
  const url = `https://api.telegram.org/bot${NOTIFICATIONS_API}/answerCallbackQuery`;
  await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      callback_query_id: callbackQueryId,
      text: 'Processing your request...',
      show_alert: false, // You can set to true if you want to show an alert
    }),
  });
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
        keyboard: [
          [
            { text: 'Order' },
            { text: 'Orders' }
          ],
          [
            { text: 'Start' },
            { text: 'KOLORYT' }
          ]
        ],
        one_time_keyboard: false, // Set to false to keep the keyboard visible
        resize_keyboard: true // Adjusts the size of the keyboard
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


async function sendMessage(chatId: string, text: string, keyboard?: any): Promise<void> {
  const url = `https://api.telegram.org/bot${NOTIFICATIONS_API}/sendMessage`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text: text,
      reply_markup: keyboard ? {
        inline_keyboard: keyboard
      } : undefined
    })
  });

  if (!response.ok) {
    console.error(`Failed to send message: ${response.statusText}`);
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
    await updateGlobalAuthToken();
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
    await updateGlobalAuthToken();

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
  size?: string;
  quantity: number;
  total_sum: number;
  color_name?: string;
  item_price: string;
  color_value: string;
  product_name: string;
  collection_name: string;
}

interface Order {
  order_id: number;
  phone?: string;
  status?: string;
  created_at?: string;
  processed_at?: string;
  complete_at?: string;
  canceled_at?: string;
  submitted_at?: string;
  order_items?: OrderItem[];
  TelegramUser?: TelegramUser[];
  email?: string;
}

interface OrderSummaryResponse {
  chat_id?: string;
  orders: Order[];
}

interface OrderResponse {
  count: number;
  next?: string | null;
  previous?: string | null;
  results: OrderSummaryResponse[];
}

interface TelegramUser {
  phone_number: string;
  chat_id: string;
}

const isOrderItem = (obj: any): obj is OrderItem =>
  obj && typeof obj.quantity === 'number' && typeof obj.total_sum === 'number' &&
  typeof obj.item_price === 'string' && typeof obj.color_value === 'string' &&
  typeof obj.product_name === 'string' && typeof obj.collection_name === 'string';

  const isOrder = (obj: any): obj is Order =>
    obj && typeof obj.order_id === 'number' &&
    (obj.order_items === undefined || Array.isArray(obj.order_items) && obj.order_items.every(isOrderItem)) &&
    (obj.phone === undefined || typeof obj.phone === 'string') &&
    (obj.status === undefined || typeof obj.status === 'string') &&
    (obj.created_at === undefined || typeof obj.created_at === 'string') &&
    (obj.processed_at === undefined || typeof obj.processed_at === 'string') &&
    (obj.complete_at === undefined || typeof obj.complete_at === 'string') &&
    (obj.canceled_at === undefined || typeof obj.canceled_at === 'string') &&
    (obj.submitted_at === undefined || typeof obj.submitted_at === 'string') &&
    (obj.TelegramUser === undefined || 
      Array.isArray(obj.TelegramUser) &&
      obj.TelegramUser.every((u: any): u is TelegramUser => typeof u.phone_number === 'string' && typeof u.chat_id === 'string')) &&
    (obj.email === undefined || typeof obj.email === 'string');

const isOrderSummaryResponse = (obj: any): obj is OrderSummaryResponse =>
  obj && (obj.chat_id === undefined || typeof obj.chat_id === 'string') &&
  Array.isArray(obj.orders) && obj.orders.every(isOrder);

const isOrderResponse = (data: any): data is OrderResponse =>
  data && typeof data.count === 'number' &&
  (data.next === undefined || typeof data.next === 'string' || data.next === null) &&
  (data.previous === undefined || typeof data.previous === 'string' || data.previous === null) &&
  Array.isArray(data.results) && data.results.every(isOrderSummaryResponse);


const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  return isNaN(date.getTime()) ? dateString : date.toISOString().split('T')[0];
};

const getLatestStatusEntry = (statusDates: Record<string, string | null>): string | undefined => {
  const statusEmojis: Record<string, string> = {
    'submitted': '📝',
    'created': '🆕',
    'processed': '🔄',
    'complete': '✅',
    'canceled': '❌',
  };

  return Object.entries(statusDates)
    .filter(([_, date]) => date)
    .sort(([_, dateA], [__, dateB]) => new Date(dateB!).getTime() - new Date(dateA!).getTime())
    .map(([status, date]) => `${statusEmojis[status]} ${status.charAt(0).toUpperCase() + status.slice(1)}: ${formatDate(date!)}`)
    .shift();
};

const fetchOrderSummary = async (chatId: string): Promise<OrderResponse> => {
  if (!accessToken) throw new Error('No access token available.');

  // Construct the URL with the chatId
  const summaryUrl = `${VERCEL_DOMAIN}/api/order_summary/by_chat_id/?chat_id=${encodeURIComponent(chatId)}`;

  const response = await fetch(summaryUrl, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  });

  if (!response.ok) {
    const errorText = await response.text(); // Capture error details
    console.error(`Failed to retrieve order summary. Status: ${response.status}, Error: ${errorText}`);
    throw new Error(`Failed to retrieve order summary. Status: ${response.status}`);
  }
  const responseBody = await response.json();
  console.log('Response Body:', responseBody); // Log the raw response

  if (!isOrderResponse(responseBody)) {
    console.error('Invalid response format:', responseBody);
    throw new Error('Invalid response format.');
  }

  return responseBody;
};

async function sendOrderDetails(phoneNumber: string, chatId: string | null): Promise<void> {
  if (!chatId) {
    console.error('Chat ID is missing.');
    if (phoneNumber) await sendMessage(phoneNumber, 'Chat ID is missing. Please try again later.');
    return;
  }

  try {
    const responseBody = await fetchOrderSummary(chatId);

    const summary = responseBody.results.find(result => result.chat_id === chatId);

    if (!summary || summary.orders.length === 0) {
      console.log('No orders found for this chat ID.');
      await sendMessage(chatId, 'No orders found for this phone number and chat ID.');
      return;
    }

    const latestOrder = summary.orders.reduce((latest, order) =>
      new Date(order.submitted_at || order.processed_at || '') >
      new Date(latest.submitted_at || latest.processed_at || '') ? order : latest, summary.orders[0]);

    if (!latestOrder.order_items) {
      console.log('No order items found for this order.');
      await sendMessage(chatId, 'No order items found for this order.');
      return;
    }

    const orderItemsSummary = latestOrder.order_items.map(item =>
      `- ${item.product_name}, ${item.collection_name}, Size: ${item.size || 'N/A'}, Color: ${item.color_name || 'N/A'}, ${item.quantity} pcs, ${parseFloat(item.item_price).toFixed(2)}`
    ).join('\n');

    const statusDates = {
      'submitted': latestOrder.submitted_at ?? null,
      'created': latestOrder.created_at ?? null,
      'processed': latestOrder.processed_at ?? null,
      'complete': latestOrder.complete_at ?? null,
      'canceled': latestOrder.canceled_at ?? null
    };

    const latestStatusEntry = getLatestStatusEntry(statusDates);

    const orderDetailsMessage =
      `Order ID: ${latestOrder.order_id}
      Order Items:
      ${orderItemsSummary}
      ${latestStatusEntry ? latestStatusEntry : ''}
    `;

    await sendMessage(chatId, `Thank you! Here are your order details:\n${orderDetailsMessage}`);
  } catch (error) {
    console.error(`Error retrieving order details: ${error}`);
    await sendMessage(chatId, 'An error occurred while retrieving order details. Please try again later.');
  }
}

async function sendAllOrdersDetails(chatId: string | null): Promise<void> {
  if (!chatId) {
    console.error('Chat ID is missing.');
    return;
  }

  try {
    const responseBody = await fetchOrderSummary(chatId);

    const allOrders = responseBody.results.flatMap(result => result.orders);

    if (allOrders.length === 0) {
      console.log('No orders found for this chat ID.');
      await sendMessage(chatId, 'No orders found for this chat ID.');
      return;
    }

    const ordersMessage = allOrders.map((order: Order) => {
      if (!order.order_items) {
        return `Order ID: ${order.order_id}
        No order items found for this order.`;
      }

      const orderItemsSummary = order.order_items.map((item: OrderItem) =>
        `- ${item.product_name}, ${item.collection_name}, Size: ${item.size || 'N/A'}, Color: ${item.color_name || 'N/A'}, ${item.quantity} pcs, ${parseFloat(item.item_price).toFixed(2)}`
      ).join('\n');

      const statusDates = {
        'submitted': order.submitted_at ?? null,
        'created': order.created_at ?? null,
        'processed': order.processed_at ?? null,
        'complete': order.complete_at ?? null,
        'canceled': order.canceled_at ?? null
      };

      const latestStatusEntry = getLatestStatusEntry(statusDates);

      return `Order ID: ${order.order_id}
      Order Items:
      ${orderItemsSummary}
      ${latestStatusEntry ? latestStatusEntry : ''}
      `;
    }).join('\n\n');

    await sendMessage(chatId, `Here are all your order details:\n${ordersMessage}`);
  } catch (error) {
    console.error(`Error retrieving order details: ${error}`);
    await sendMessage(chatId, 'An error occurred while retrieving order details. Please try again later.');
  }
}
