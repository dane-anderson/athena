// swift-tools-version: 5.9

import PackageDescription

let package = Package(
    name: "AthenaNative",
    platforms: [
        .macOS(.v13)
    ],
    products: [
        .executable(
            name: "AthenaNative",
            targets: ["AthenaNative"]
        )
    ],
    targets: [
        .executableTarget(
            name: "AthenaNative"
        )
    ]
)
