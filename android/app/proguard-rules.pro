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

# Example: Keep classes used in Retrofit
-keep class retrofit2.** { *; }
