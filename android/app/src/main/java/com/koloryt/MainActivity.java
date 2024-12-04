package com.koloryt;

import android.os.Bundle;
import android.webkit.CookieManager;
import android.webkit.WebResourceRequest;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.util.Log;
import android.view.KeyEvent;
import android.view.Window;
import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AppCompatActivity;
import androidx.appcompat.app.AppCompatDelegate;
import androidx.core.view.WindowCompat;
import androidx.core.view.WindowInsetsCompat;
import androidx.core.view.WindowInsetsControllerCompat;

public class MainActivity extends AppCompatActivity {

    private WebView webView;
    private WindowInsetsControllerCompat insetsController;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

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

        // Set WebView client to handle URL loading
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                view.loadUrl(request.getUrl().toString());
                return true; // Handle links within the WebView
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, android.webkit.WebResourceError error) {
                super.onReceivedError(view, request, error);
                Log.e("WebViewError", "Error loading URL: " + error.getDescription().toString());
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
}
