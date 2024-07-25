"use strict";

// Define types
interface Contact {
  phone_number: string;
}

interface Message {
  chat: {
    id: string;
  };
  contact?: Contact;
  text?: string;
}

interface Update {
  message?: Message;
}

(async () => {
  async function handleRequest(request: Request): Promise<Response> {
    const url = new URL(request.url);

    if (url.pathname === "/favicon.ico") {
      return new Response("Favicon not found", { status: 404 });
    }

    if (request.method === "POST") {
      try {
        const update: Update = await request.json(); // Use Update type
        console.log("Received update:", update);

        if (update.message) {
          const chatId: string = update.message.chat.id;

          if (update.message.contact) {
            const phoneNumber: string = update.message.contact.phone_number;
            await sendChatIdAndPhoneToVercel(chatId, phoneNumber);
            await sendMessage(chatId, "Thank you! Your phone number has been recorded.");
          } else if (update.message.text === "/start") {
            await sendMessage(chatId, "Please share your phone number using the contact button below.");
            await sendContactRequest(chatId);
          }
          return new Response("OK", { status: 200 });
        }

        return new Response("Invalid update", { status: 400 });
      } catch (error) {
        console.error("Error handling request:", error);
        if (error instanceof Error) {
          return new Response(`Error: ${error.message}`, { status: 500 });
        }
        return new Response("Error: Unknown error", { status: 500 });
      }
    }

    return new Response("Method Not Allowed", { status: 405 });
  }

  async function sendMessage(chatId: string, text: string): Promise<void> {
    try {
      const url = `https://api.telegram.org/bot${process.env.NOTIFICATIONS_API}/sendMessage`;
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chat_id: chatId, text })
      });
      if (!response.ok) {
        throw new Error(`Failed to send message: ${response.statusText}`);
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error(`Error in sendMessage: ${error.message}`);
        throw error;
      }
      console.error("Unknown error in sendMessage");
      throw new Error("Unknown error in sendMessage");
    }
  }

  async function sendContactRequest(chatId: string): Promise<void> {
    try {
      const url = `https://api.telegram.org/bot${process.env.NOTIFICATIONS_API}/sendMessage`;
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          chat_id: chatId,
          text: "Please share your phone number:",
          reply_markup: {
            one_time_keyboard: true,
            keyboard: [[{ text: "Share phone number", request_contact: true }]]
          }
        })
      });
      if (!response.ok) {
        throw new Error(`Failed to send contact request: ${response.statusText}`);
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error(`Error in sendContactRequest: ${error.message}`);
        throw error;
      }
      console.error("Unknown error in sendContactRequest");
      throw new Error("Unknown error in sendContactRequest");
    }
  }

  async function sendChatIdAndPhoneToVercel(chatId: string, phoneNumber: string): Promise<void> {
    try {
      const vercelUrl = `https://${process.env.VERCEL_DOMAIN}/telegram_webhook/`;
      const response = await fetch(vercelUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ chatId, phoneNumber })
      });
      if (!response.ok) {
        throw new Error(`Failed to send data to Vercel: ${response.statusText}`);
      }
    } catch (error) {
      if (error instanceof Error) {
        console.error(`Error in sendChatIdAndPhoneToVercel: ${error.message}`);
        throw error;
      }
      console.error("Unknown error in sendChatIdAndPhoneToVercel");
      throw new Error("Unknown error in sendChatIdAndPhoneToVercel");
    }
  }

  addEventListener("fetch", (event: FetchEvent) => {
    event.respondWith(handleRequest(event.request));
  });
})();
