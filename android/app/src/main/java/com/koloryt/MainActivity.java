package com.koloryt;

import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.util.Log;
import android.view.KeyEvent;
import androidx.activity.OnBackPressedCallback;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Set the layout file
        
        WebView webView = findViewById(R.id.webview);
        webView.getSettings().setJavaScriptEnabled(true);
        webView.getSettings().setDomStorageEnabled(true);
        webView.clearCache(true);
        webView.clearHistory();
        webView.loadUrl("https://myshop-topaz-five.vercel.app/");
        
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                view.loadUrl(request.getUrl().toString()); // Handle links within the WebView
                return true; // Don't open in an external browser
            }

            @Override
            public void onReceivedError(WebView view, WebResourceRequest request, android.webkit.WebResourceError error) {
                super.onReceivedError(view, request, error);
                Log.e("WebViewError", "Error loading URL: " + error.getDescription().toString());
            }
        });

        // Handle back button press using OnBackPressedDispatcher
        getOnBackPressedDispatcher().addCallback(this, new OnBackPressedCallback(true) {
            @Override
            public void handleOnBackPressed() {
                WebView webView = findViewById(R.id.webview);
                if (webView.canGoBack()) {
                    webView.goBack();  // Go to the previous page in WebView
                } else {
                    // If the WebView cannot go back, close the activity
                    finish(); // Close the activity without calling deprecated onBackPressed()
                }
            }
        });
    }

    // Override the back button to minimize the app if needed
    @Override
    public boolean onKeyDown(int keyCode, KeyEvent event) {
        if (keyCode == KeyEvent.KEYCODE_BACK) {
            WebView webView = findViewById(R.id.webview);
            if (!webView.canGoBack()) {
                moveTaskToBack(true);  // Minimize the app if no pages in history
                return true;  // Indicate that the event is handled
            }
        }
        return super.onKeyDown(keyCode, event);
    }
}
