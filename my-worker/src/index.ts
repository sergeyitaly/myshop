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

async function sendNotificationToUsersByLanguage(
  chatIds: Set<string>,
  enMessage: string,
  ukMessage: string
): Promise<void> {
  await updateGlobalAuthToken();

  for (const chatId of chatIds) {
    const isEnglish = getUserLanguage(chatId) === 'en';
    const message = isEnglish ? enMessage : ukMessage;

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
        const enSuccessMessage = '✅ Server up and running!';
        const ukSuccessMessage = '✅ Сервер працює!';

        // Send success notifications based on user language preference
        await sendNotificationToUsersByLanguage(cachedChatIds, enSuccessMessage, ukSuccessMessage);
        lastHealthCheckStatus = 'success';
      }

      cachedChatIds = await fetchChatIds();
    } else {
      const enErrorMessage = `🚨 Server is down: ${response.statusText}`;
      const ukErrorMessage = `🚨 Сервер не працює: ${response.statusText}`;
      console.error(enErrorMessage);

      if (lastHealthCheckStatus !== 'failure') {
        await sendNotificationToUsersByLanguage(cachedChatIds, enErrorMessage, ukErrorMessage);
        lastHealthCheckStatus = 'failure';
      }
    }
  } catch (error) {
    const enErrorMessage = `❗ Error performing health check: ${error}`;
    const ukErrorMessage = `❗ Помилка перевірки стану сервера: ${error}`;
    console.error(enErrorMessage);

    if (lastHealthCheckStatus !== 'failure') {
      await sendNotificationToUsersByLanguage(cachedChatIds, enErrorMessage, ukErrorMessage);
      lastHealthCheckStatus = 'failure';
    }
  }
}


async function getHealthStatus(isEnglish: boolean): Promise<string> {
  const healthCheckUrl = `${VERCEL_DOMAIN}/api/health_check`;
  try {
    const response = await fetch(healthCheckUrl);
    if (response.ok) {
      return isEnglish ? '✅ Server up and running!' : '✅ Сервер працює!';
    } else {
      return isEnglish ? `🚨 Server is down: ${response.statusText}` : `🚨 Сервер не працює: ${response.statusText}`;
    }
  } catch (error) {
    return isEnglish ? `❗ Error performing health check: ${error}` : `❗ Помилка перевірки стану сервера: ${error}`;
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

// Map to store user language preferences
const userLanguages = new Map<string | number, string>();

// Helper function to get user's current language or default to 'en'
function getUserLanguage(chatId: string | number): string {
  return userLanguages.get(chatId) || 'en';
}

// Helper function to toggle language
function toggleUserLanguage(chatId: string | number): void {
  const currentLanguage = getUserLanguage(chatId);
  const newLanguage = currentLanguage === 'en' ? 'uk' : 'en';
  userLanguages.set(chatId, newLanguage);
}

// Modified processMessage to handle language toggle
async function processMessage(message: any): Promise<void> {
  const chatId = message.chat.id;

  if (message.contact) {
    // Existing contact handling code
    await updateGlobalAuthToken();
    const phoneNumber = message.contact.phone_number;
    const userExistsFlag = await userExists(phoneNumber, chatId);

    if (userExistsFlag) {
      console.warn(`User with phone: ${phoneNumber} and chat ID: ${chatId} already exists.`);
    } else {
      console.log('Posting new user data to Vercel API');
      await sendChatIdAndPhoneToVercel(phoneNumber, chatId);
    }

    phoneNumbers.set(chatId, phoneNumber);
    chatIds.add(chatId);

    // Send the custom keyboard with the appropriate language
    await sendCustomKeyboard(chatId);

  } else if (message.text === 'En/Uk' || message.text === 'Укр/En') {
    // Toggle the user's language preference
    toggleUserLanguage(chatId);
    // Send updated keyboard with the new language setting
    await sendCustomKeyboard(chatId);

  } else if (message.text === 'Order' || message.text === 'Замовлення') {
    // Existing order handling code
    await updateGlobalAuthToken();
    const phoneNumber = phoneNumbers.get(chatId);
    if (phoneNumber) {
      await sendOrderDetails(phoneNumber, chatId);
    } else {
      await sendMessage(chatId, '🔍 Phone number not found. Please share your phone number first.');
      await sendContactRequest(chatId);
    }

  } else if (message.text === 'Orders' || message.text === 'Всі замовлення') {
    // Existing orders handling code
    await updateGlobalAuthToken();
    const phoneNumber = phoneNumbers.get(chatId);
    if (phoneNumber) {
      await sendAllOrdersDetails(chatId);
    } else {
      await sendMessage(chatId, '🔍 Phone number not found. Please share your phone number first.');
      await sendContactRequest(chatId);
    }

  } else if (message.text === 'KOLORYT') {
    const isEnglish = getUserLanguage(chatId) === 'en';
    const message = isEnglish
    ? `You can proceed to KOLORYT here: \n${VERCEL_DOMAIN}`
    : `Ви можете перейти до KOLORYT тут: \n${VERCEL_DOMAIN}`;

    try {
      await sendMessage(chatId, message);
  
      const healthStatus = await getHealthStatus(isEnglish);
      await sendMessage(chatId, isEnglish ? `Current status:\n${healthStatus}` : `Поточний статус:\n${healthStatus}`);
    } catch (error) {
      await sendMessage(chatId, isEnglish ? '⚠️ Unable to fetch server status at the moment.' : '⚠️ Наразі неможливо отримати стан сервера.');
    }
  }
   else {
    // Send the custom keyboard with correct options
    await sendCustomKeyboard(chatId);
  }
}

// Send keyboard with dynamic button labels based on user's language preference
async function sendCustomKeyboard(chatId: string | number): Promise<void> {
  const isEnglish = getUserLanguage(chatId) === 'en';

  const orderButtonText = isEnglish ? 'Order' : 'Замовлення';
  const ordersButtonText = isEnglish ? 'Orders' : 'Всі замовлення';
  const langButtonText = isEnglish ? 'En/Uk' : 'Укр/En';
  const kolorytButtonText = 'KOLORYT'; // Assuming this doesn't change

  const url = `https://api.telegram.org/bot${NOTIFICATIONS_API}/sendMessage`;
  const response = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      chat_id: chatId,
      text: isEnglish ? 'Choose an action:' : 'Оберіть дію:',
      reply_markup: {
        keyboard: [
          [
            { text: orderButtonText },
            { text: ordersButtonText }
          ],
          [
            { text: langButtonText },
            { text: kolorytButtonText }
          ]
        ],
        one_time_keyboard: false,
        resize_keyboard: true
      }
    })
  });

  if (!response.ok) {
    throw new Error(`Failed to send custom keyboard: ${response.statusText}`);
  }
}

async function processCallbackQuery(callbackQuery: any): Promise<void> {
  await updateGlobalAuthToken();
  const chatId = callbackQuery.message.chat.id;
  const callbackData = callbackQuery.data;
  const phoneNumber = phoneNumbers.get(chatId);

  if (!phoneNumber) {
    await sendMessage(chatId, getUserLanguage(chatId) === 'en'
      ? '🔍 Phone number not found. Please share your phone number first.'
      : '🔍 Номер телефону не знайдено. Спочатку поділіться своїм номером телефону.');
    await sendContactRequest(chatId);
    return;
  }

  if (callbackData === 'Order') {
    await updateGlobalAuthToken();
    await sendOrderDetails(phoneNumber, chatId);
  } else if (callbackData === 'Orders') {
    await sendAllOrdersDetails(chatId);
  } else if (callbackData === 'En/Uk') {
    // Toggle language preference
    await updateGlobalAuthToken();
    const currentLang = getUserLanguage(chatId);
    const newLang = currentLang === 'en' ? 'uk' : 'en';
    userLanguages.set(chatId, newLang);

    // Confirm the language change
    const confirmationText = newLang === 'en' ? 'Language set to English.' : 'Мову змінено на українську.';
    await sendMessage(chatId, confirmationText);

    // Update keyboard with the new language button label
    await sendCustomKeyboard(chatId);
  } else {
    await sendMessage(chatId, getUserLanguage(chatId) === 'en'
      ? '⚠️ Unknown action.'
      : '⚠️ Невідома дія.');
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


interface TelegramUser {
  phone_number: string;
  chat_id: string;
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
  created_at?: string | null;
  processed_at?: string | null;
  complete_at?: string | null;
  canceled_at?: string | null;
  submitted_at?: string | null;
  order_items?: OrderItem[];
  TelegramUser?: TelegramUser[];
  email?: string;
}

interface OrderSummaryResponse {
  results: Order[];
}

interface OrderResponse {
  results: Order[];
}

const isOrderResponse = (data: any): data is OrderResponse => {
  return data &&
    typeof data.order_id === 'number' &&
    (data.created_at === null || typeof data.created_at === 'string') &&
    (data.submitted_at === null || typeof data.submitted_at === 'string') &&
    (data.processed_at === null || typeof data.processed_at === 'string') &&
    (data.complete_at === null || typeof data.complete_at === 'string') &&
    (data.canceled_at === null || typeof data.canceled_at === 'string') &&
    Array.isArray(data.order_items) &&
    data.order_items.every((item: any) =>
      typeof item.product_name === 'string' &&
      typeof item.collection_name === 'string' &&
      typeof item.size === 'string' &&
      typeof item.color_name === 'string' &&
      typeof item.quantity === 'number' &&
      typeof item.total_sum === 'number' &&
      typeof item.item_price === 'string' &&
      typeof item.color_value === 'string'
    );
};

const isValidOrder = (order: any): order is Order => {
  return order && typeof order.order_id === 'number' &&
    (order.created_at === null || typeof order.created_at === 'string') &&
    (order.submitted_at === null || typeof order.submitted_at === 'string') &&
    (order.processed_at === null || typeof order.processed_at === 'string') &&
    (order.complete_at === null || typeof order.complete_at === 'string') &&
    (order.canceled_at === null || typeof order.canceled_at === 'string') &&
    Array.isArray(order.order_items) && order.order_items.every(isOrderItem);
};
const isOrderSummaryResponse = (data: any): data is OrderSummaryResponse => {
  return data &&
    Array.isArray(data.results) &&
    data.results.every((order: any) =>
      typeof order.order_id === 'number' &&
      (order.created_at === null || typeof order.created_at === 'string') &&
      (order.submitted_at === null || typeof order.submitted_at === 'string') &&
      (order.processed_at === null || typeof order.processed_at === 'string') &&
      (order.complete_at === null || typeof order.complete_at === 'string') &&
      (order.canceled_at === null || typeof order.canceled_at === 'string') &&
      Array.isArray(order.order_items) &&
      order.order_items.every((item: any) =>
        typeof item.product_name === 'string' &&
        typeof item.collection_name === 'string' &&
        typeof item.size === 'string' &&
        typeof item.color_name === 'string' &&
        typeof item.quantity === 'number' &&
        typeof item.total_sum === 'number' &&
        typeof item.item_price === 'string' &&
        typeof item.color_value === 'string'
      )
    );
};

const isOrderItem = (item: any): item is OrderItem => {
  return item && typeof item.product_name === 'string' &&
    typeof item.collection_name === 'string' &&
    typeof item.size === 'string' &&
    typeof item.color_name === 'string' &&
    typeof item.quantity === 'number' &&
    typeof item.total_sum === 'number' &&
    typeof item.item_price === 'string' &&
    typeof item.color_value === 'string';
};

const getLatestStatusEntry = (statusDates: Record<string, string | null>, isEnglish: boolean): string | undefined => {
  const statusEmojis: Record<string, string> = {
    'submitted': '📝',
    'created': '🆕',
    'processed': '🔄',
    'complete': '✅',
    'canceled': '❌',
  };

  const statusLabels: Record<string, { en: string; uk: string }> = {
    'submitted': { en: 'Submitted', uk: 'Подано' },
    'created': { en: 'Created', uk: 'Створено' },
    'processed': { en: 'Processed', uk: 'Оброблено' },
    'complete': { en: 'Complete', uk: 'Завершено' },
    'canceled': { en: 'Canceled', uk: 'Скасовано' },
  };

  // Ensure statusDates entries are sorted and mapped correctly
  return Object.entries(statusDates)
    .filter(([_, date]) => date !== null)
    .sort(([_, dateA], [__, dateB]) => new Date(dateB!).getTime() - new Date(dateA!).getTime())
    .map(([status, date]) => {
      const label = isEnglish ? statusLabels[status].en : statusLabels[status].uk;
      return `${statusEmojis[status]} ${label}: ${formatDate(date!)}`;
    })
    .shift();
};


// Example usage
const formatDate = (date: string): string => {
  // Dummy implementation for formatting dates
  return new Date(date).toLocaleDateString();
};

const fetchOrderSummary = async (chatId: string): Promise<OrderSummaryResponse> => {
  try {
    const response = await fetch(`${VERCEL_DOMAIN}/api/order_summary/by_chat_id/${chatId}/`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error(`Failed to retrieve order summary. Status: ${response.status}`);
    }

    const contentType = response.headers.get('Content-Type');
    if (!contentType || !contentType.includes('application/json')) {
      throw new Error('Unexpected Content-Type. Expected application/json.');
    }

    const responseBody: unknown = await response.json();
    console.log('Response Body:', responseBody);

    if (isOrderSummaryResponse(responseBody)) {
      return responseBody;
    } else {
      console.error('Invalid response format:', responseBody);
      throw new Error('Invalid response format.');
    }

  } catch (error) {
    console.error(`Error during fetch operation: ${error}`);
    throw error;
  }
};
async function sendOrderDetails(phoneNumber: string, chatId: string | null): Promise<void> {
  const isEnglish = chatId ? getUserLanguage(chatId) === 'en' : true;

  if (!chatId) {
    const errorMessage = isEnglish ? 'Chat ID is missing. Please try again later.' : 'Відсутній ідентифікатор чату. Будь ласка, спробуйте пізніше.';
    console.error('Chat ID is missing.');
    if (phoneNumber) await sendMessage(phoneNumber, errorMessage);
    return;
  }

  try {
    const responseBody = await fetchOrderSummary(chatId);
    const orderResults = responseBody.results;

    if (!orderResults || orderResults.length === 0) {
      const noOrdersMessage = isEnglish ? 'No orders found for this chat ID.' : 'Замовлення для цього чату не знайдено.';
      await sendMessage(chatId, noOrdersMessage);
      return;
    }

    const latestOrder = orderResults.reduce((prev, current) => (prev.order_id > current.order_id ? prev : current));

    if (!latestOrder.order_items || latestOrder.order_items.length === 0) {
      const noItemsMessage = isEnglish ? 'No order items found for the latest order.' : 'Не знайдено товарів для останнього замовлення.';
      await sendMessage(chatId, noItemsMessage);
      return;
    }

    const orderItemsSummary = latestOrder.order_items.map((item: OrderItem) =>
      `- ${item.product_name}, ${item.collection_name}, ${isEnglish ? 'Size' : 'Розмір'}: ${item.size || 'N/A'}, ${isEnglish ? 'Color' : 'Колір'}: ${item.color_name || 'N/A'}, ${item.quantity} ${isEnglish ? 'pcs' : 'шт'}, $${parseFloat(item.item_price).toFixed(2)}`
    ).join('\n');

    const statusDates = {
      submitted: latestOrder.submitted_at ?? null,
      created: latestOrder.created_at ?? null,
      processed: latestOrder.processed_at ?? null,
      complete: latestOrder.complete_at ?? null,
      canceled: latestOrder.canceled_at ?? null,
    };

    // Pass `isEnglish` to getLatestStatusEntry
    const latestStatusEntry = getLatestStatusEntry(statusDates, isEnglish);

    const orderDetailsMessage =
      `${isEnglish ? 'Order ID' : 'Номер замовлення'}: ${latestOrder.order_id}\n` +
      `${isEnglish ? 'Order Items' : 'Товари в замовленні'}:\n${orderItemsSummary}\n` +
      `${latestStatusEntry || ''}`;

    const thankYouMessage = isEnglish ? 'Thank you! Here are your order details:' : 'Дякуємо! Ось ваші деталі замовлення:';
    await sendMessage(chatId, `${thankYouMessage}\n${orderDetailsMessage}`);
  } catch (error) {
    const errorMessage = isEnglish ? 'An error occurred while retrieving order details. Please try again later.' : 'Сталася помилка при отриманні деталей замовлення. Будь ласка, спробуйте пізніше.';
    console.error(`Error retrieving order details: ${error}`);
    await sendMessage(chatId, errorMessage);
  }
}

async function sendAllOrdersDetails(chatId: string | null): Promise<void> {
  const isEnglish = chatId ? getUserLanguage(chatId) === 'en' : true;

  if (!chatId) {
    console.error('Chat ID is missing.');
    return;
  }

  try {
    const responseBody = await fetchOrderSummary(chatId);
    const orderResults = responseBody.results;

    if (!orderResults || orderResults.length === 0) {
      const noOrdersMessage = isEnglish ? 'No orders found for this chat ID.' : 'Замовлення для цього чату не знайдено.';
      await sendMessage(chatId, noOrdersMessage);
      return;
    }

    const ordersMessage = orderResults.map(order => {
      if (!order.order_items || order.order_items.length === 0) {
        return `${isEnglish ? 'Order ID' : 'Номер замовлення'}: ${order.order_id}\n${isEnglish ? 'No order items found for this order.' : 'Товари для цього замовлення не знайдено.'}`;
      }

      const orderItemsSummary = order.order_items.map((item: OrderItem) =>
        `- ${item.product_name}, ${item.collection_name}, ${isEnglish ? 'Size' : 'Розмір'}: ${item.size || 'N/A'}, ${isEnglish ? 'Color' : 'Колір'}: ${item.color_name || 'N/A'}, ${item.quantity} ${isEnglish ? 'pcs' : 'шт'}, $${parseFloat(item.item_price).toFixed(2)}`
      ).join('\n');

      const statusDates = {
        submitted: order.submitted_at ? new Date(order.submitted_at).toLocaleString() : 'N/A',
        created: order.created_at ? new Date(order.created_at).toLocaleString() : 'N/A',
        processed: order.processed_at ? new Date(order.processed_at).toLocaleString() : 'N/A',
        complete: order.complete_at ? new Date(order.complete_at).toLocaleString() : 'N/A',
        canceled: order.canceled_at ? new Date(order.canceled_at).toLocaleString() : 'N/A'
      };

      // Pass `isEnglish` to getLatestStatusEntry
      const latestStatusEntry = getLatestStatusEntry(statusDates, isEnglish);

      return `${isEnglish ? 'Order ID' : 'Номер замовлення'}: ${order.order_id}\n${isEnglish ? 'Order Items' : 'Товари в замовленні'}:\n${orderItemsSummary}\n${isEnglish ? 'Latest Status' : 'Останній статус'}: ${latestStatusEntry || (isEnglish ? 'Status not available.' : 'Статус недоступний.')}`;
    }).join('\n\n');

    const allOrdersMessage = isEnglish ? 'Here are all your order details:' : 'Ось усі ваші деталі замовлень:';
    await sendMessage(chatId, `${allOrdersMessage}\n${ordersMessage}`);
  } catch (error) {
    const errorMessage = isEnglish ? 'An error occurred while retrieving all order details. Please try again later.' : 'Сталася помилка при отриманні всіх деталей замовлень. Будь ласка, спробуйте пізніше.';
    console.error(`Error retrieving all orders details: ${error}`);
    await sendMessage(chatId, errorMessage);
  }
}
