#!/bin/zsh
set -e

ROOT="/Users/daneanderson/Desktop/Projects/Athena Core"
SWIFT_DIR="$ROOT/macos/AthenaNative"
APP="/Applications/Athena.app"
APP_BINARY="$APP/Contents/MacOS/Athena"

echo "🔨 Building latest Athena..."

cd "$SWIFT_DIR"

swift build -c release

BIN_DIR="$(swift build -c release --show-bin-path)"
NEW_BINARY="$BIN_DIR/AthenaNative"

if [ ! -f "$NEW_BINARY" ]; then
    echo "❌ Could not find built AthenaNative binary."
    exit 1
fi

echo "🛑 Closing old Athena..."
pkill -x Athena 2>/dev/null || true

sleep 1

if [ ! -f "$APP_BINARY.backup" ]; then
    echo "💾 Saving original app binary..."
    cp "$APP_BINARY" "$APP_BINARY.backup"
fi

echo "✨ Installing newest Athena..."
cp "$NEW_BINARY" "$APP_BINARY"
chmod +x "$APP_BINARY"

echo "🔏 Refreshing local app signature..."
codesign \
    --force \
    --deep \
    --sign - \
    "$APP"

echo "🚀 Opening Athena..."
open "$APP"

echo "✅ Athena.app is updated."
