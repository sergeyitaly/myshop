package com.koloryt;

import android.os.Bundle;
import android.webkit.CookieManager;
import android.webkit.JavascriptInterface;
import android.webkit.WebResourceRequest;
import android.webkit.WebResourceResponse;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.view.KeyEvent;
import android.view.Window;
import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;
import androidx.core.splashscreen.SplashScreen;

import java.io.InputStream;
import java.net.HttpURLConnection;
import android.content.Intent;
import android.net.Uri;
import android.os.AsyncTask;
import android.widget.Toast;
import android.content.ActivityNotFoundException;
import java.util.Map;
import java.util.HashMap;
import java.io.IOException; 
import java.net.URL;
import java.util.concurrent.ExecutorService; 
import java.util.concurrent.Executors; 
import java.util.HashSet;
import java.util.Set;

public class MainActivity extends AppCompatActivity {

    private WebView webView;
    private WindowInsetsControllerCompat insetsController;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        // Install the splash screen
        SplashScreen splashScreen = SplashScreen.installSplashScreen(this);

        super.onCreate(savedInstanceState);
        setTheme(R.style.AppTheme);

        // Enforce light mode for all versions
        AppCompatDelegate.setDefaultNightMode(AppCompatDelegate.MODE_NIGHT_NO);

        // Set content view and enable immersive mode
        setContentView(R.layout.activity_main);
        initializeFullScreenMode(WindowInsetsCompat.Type.systemBars(),
                WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);

        // Initialize WebView
        webView = findViewById(R.id.webview);
        configureWebView();

        // Load the URL into the WebView
        webView.loadUrl("https://myshop-topaz-five.vercel.app/");

        // Handle back button press
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                if (webView.canGoBack()) {
                    webView.goBack(); // Go to the previous page in WebView
                } else {
                    finish(); // Close the activity if no pages in history
                }
            }
        });
    }



    private final Set<String> processedUrls = new HashSet<>();

    private void configureWebView() {
        webView.getSettings().setJavaScriptEnabled(true); // Enable JavaScript
        webView.getSettings().setDomStorageEnabled(true); // Enable DOM storage
        webView.getSettings().setCacheMode(WebSettings.LOAD_NO_CACHE); // Disable cache

        // Clear cookies and cache
        CookieManager cookieManager = CookieManager.getInstance();
        cookieManager.removeAllCookies(null);
        cookieManager.flush();
        webView.clearCache(true);
        webView.clearHistory();

        // Add JavaScript interface
        webView.addJavascriptInterface(new WebAppInterface(), "Android");

        // Set WebView client to handle URL loading
        webView.setWebViewClient(new WebViewClient() {

            @Override
            public WebResourceResponse shouldInterceptRequest(WebView view, WebResourceRequest request) {
                if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.LOLLIPOP) {
                    String originalUrl = request.getUrl().toString();
                    String normalizedUrl = originalUrl.replaceFirst("^https?://", ""); // Remove both "http://" and "https://"

                    synchronized (processedUrls) {
                        if (processedUrls.contains(normalizedUrl)) {
                            return super.shouldInterceptRequest(view, request); // Skip duplicates
                        }
                        processedUrls.add(normalizedUrl); // Add normalized URL to the set
                    }

                    Map<String, String> headers = new HashMap<>(request.getRequestHeaders());
                    headers.put("X-Android-Client", "Koloryt");

                    // Optionally use NetworkTask or remove it
                    ExecutorService executor = Executors.newSingleThreadExecutor();
                    executor.execute(new NetworkTask(originalUrl, headers));
                    return super.shouldInterceptRequest(view, request);
                }
                return super.shouldInterceptRequest(view, request);
            }

//The NetworkTask class in this implementation is used to execute network requests in a separate thread, fetching data from a URL.
            private class NetworkTask implements Runnable {
                private String urlString;
                private Map<String, String> headers;

                NetworkTask(String urlString, Map<String, String> headers) {
                    this.urlString = urlString;
                    this.headers = headers;
                }

                @Override
                public void run() {
                    HttpURLConnection connection = null;
                    InputStream inputStream = null;
                    try {
                        URL url = new URL(urlString);
                        connection = (HttpURLConnection) url.openConnection();
                        connection.setRequestMethod("GET");
                        for (Map.Entry<String, String> entry : headers.entrySet()) {
                            connection.setRequestProperty(entry.getKey(), entry.getValue());
                        }
                        inputStream = connection.getInputStream();
                    } catch (IOException e) {
                        e.printStackTrace();
                    } finally {
                        if (connection != null) {
                            connection.disconnect();
                        }
                    }
                }
            }

            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                String url = request.getUrl().toString();
                
                if (url.startsWith("mailto:")) {
                    Intent emailIntent = new Intent(Intent.ACTION_SENDTO);
                    emailIntent.setData(Uri.parse(url));
                    try {
                        view.getContext().startActivity(emailIntent);
                    } catch (ActivityNotFoundException e) {
                        Toast.makeText(view.getContext(), "No email app found", Toast.LENGTH_SHORT).show();
                    }
                    return true;
                } else if (url.startsWith("tg://")) {
                    Intent telegramIntent = new Intent(Intent.ACTION_VIEW);
                    telegramIntent.setData(Uri.parse(url));
                    try {
                        view.getContext().startActivity(telegramIntent);
                    } catch (ActivityNotFoundException e) {
                        Toast.makeText(view.getContext(), "Telegram is not installed", Toast.LENGTH_SHORT).show();
                    }
                    return true;
                } else if (url.contains("example.com")) {
                    view.loadUrl(url);
                    return false;
                } else {
                    Intent intent = new Intent(Intent.ACTION_VIEW);
                    intent.setData(Uri.parse(url));
                    view.getContext().startActivity(intent);
                    return true;
                }
            }


            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, android.webkit.WebResourceError error) {
                super.onReceivedError(view, request, error);

                // Check if this is a main frame error (not iframe or secondary resource errors)
                if (request.isForMainFrame()) {
                    String customErrorPage = "<html><body style='text-align:center; margin-top: 50%;'>" +
                            "<h2>No Internet Connection</h2>" +
                            "<p>Please check your internet connection and try again.</p>" +
                            "<br>"+
                            "<button onclick='goToHomePage()'> Reload </button>" +
                            "<script>" +
                            "function goToHomePage() {" +
                            "   Android.goToHomePage();" +
                            "}" +
                            "</script>" +
                            "</body></html>";
                            //style='background-color: #0b0599; color: #fff; border: 1px solid #0b0599; padding: 10px 20px; font-size: 16px; cursor: pointer;
                    view.loadData(customErrorPage, "text/html", "UTF-8");
                }
            }

        });
    }

    private void initializeFullScreenMode(int systemBarsType, int behavior) {
        Window window = getWindow();
        WindowCompat.setDecorFitsSystemWindows(window, false); // Disable fitting system windows

        // Use WindowInsetsControllerCompat to control system bars
        insetsController = WindowCompat.getInsetsController(window, window.getDecorView());
        if (insetsController != null) {
            insetsController.hide(systemBarsType); // Hide specified system bars
            insetsController.setSystemBarsBehavior(behavior); // Set the behavior for hidden bars
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        initializeFullScreenMode(WindowInsetsCompat.Type.systemBars(),
                WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
    }

    @Override
    public void onWindowFocusChanged(boolean hasFocus) {
        super.onWindowFocusChanged(hasFocus);
        if (hasFocus) {
            initializeFullScreenMode(WindowInsetsCompat.Type.systemBars(),
                    WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE);
        }
    }

    // Override the back button to minimize the app if needed
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            if (!webView.canGoBack()) {
                moveTaskToBack(true); // Minimize the app if no pages in history
                return true; // Indicate that the event is handled
            }
        }
        return super.onKeyDown(keyCode, event);
    }

        // JavaScript Interface class
        private class WebAppInterface {
            @JavascriptInterface
            public void goToHomePage() {
                runOnUiThread(() -> {
                    if (webView != null) {
                        webView.loadUrl("https://myshop-topaz-five.vercel.app/"); // Navigate to the home page
                    }
                });
            }
        }

}