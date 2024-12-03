package com.koloryt;

import android.os.Bundle;
import android.webkit.WebResourceRequest;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main); // Set the layout file
        
        // Initialize the WebView from the XML layout
        WebView webView = findViewById(R.id.webview);
        
        // Enable JavaScript for better compatibility with modern websites
        webView.getSettings().setJavaScriptEnabled(true);
        
        // Load the Vercel-hosted URL
        webView.loadUrl("https://myshop-topaz-five.vercel.app/");

        // Ensure that links open within the WebView, not an external browser
        webView.setWebViewClient(new WebViewClient() {
            @Override
            public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                view.loadUrl(request.getUrl().toString()); // Handle links within the WebView
                return true; // Don't open in an external browser
            }
        });
    }

}
