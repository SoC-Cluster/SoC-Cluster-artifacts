GOOS=android GOARCH=arm64 CC=$ANDROID_NDK/toolchains/llvm/prebuilt/darwin-x86_64/bin/aarch64-linux-android21-clang go build -x $1
