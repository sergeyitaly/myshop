# Preserve class names for reflection
-keep class androidx.** { *; }
-keep class com.koloryt.** { *; }

# Keep native methods (used by some libraries like Firebase or Retrofit)
-keepclasseswithmembers class * {
    native <methods>;
}

# Keep classes used by Android annotations
-keep class android.** { *; }
-keep class com.google.** { *; }

# Avoid obfuscation of Gson or any other serialization libraries
-keep class com.google.gson.** { *; }

# Keep Firebase classes (if used)
-keep class com.google.firebase.** { *; }
-keep class com.google.android.gms.** { *; }

# Keep Retrofit classes
-keep class retrofit2.** { *; }

# Keep classes used by reflection in OkHttp or other libraries
-keep class okhttp3.** { *; }

# Keep classes used by reflection in Picasso, Glide, etc. (if used)
-keep class com.squareup.picasso.** { *; }
-keep class com.bumptech.glide.** { *; }
