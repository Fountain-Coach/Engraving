// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "RulesKit",
    platforms: [.macOS(.v13), .iOS(.v16)],
    products: [
        .library(name: "RulesKit", targets: ["RulesKit"]),
    ],
    dependencies: [
        // Apple: https://github.com/apple/swift-openapi-generator
        .package(url: "https://github.com/apple/swift-openapi-generator", from: "1.5.0")
    ],
    targets: [
        .target(
            name: "RulesKit",
            plugins: [
                .plugin(name: "OpenAPIGenerator", package: "swift-openapi-generator")
            ],
            resources: [.process("openapi")]
        ),
        .testTarget(
            name: "RulesKitTests",
            dependencies: ["RulesKit"]
        )
    ]
)
