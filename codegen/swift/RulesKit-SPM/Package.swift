// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "RulesKit",
    platforms: [.macOS(.v13), .iOS(.v16)],
    products: [
        .library(name: "RulesKit", targets: ["RulesKit"]),
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-openapi-generator", from: "1.5.0"),
        .package(url: "https://github.com/apple/swift-openapi-runtime", from: "1.0.0"),
        .package(url: "https://github.com/apple/swift-openapi-urlsession", from: "1.0.0")
    ],
    targets: [
        .target(
            name: "RulesKit",
            dependencies: [
                .product(name: "OpenAPIRuntime", package: "swift-openapi-runtime"),
                .product(name: "OpenAPIURLSession", package: "swift-openapi-urlsession")
            ],
            resources: [
                .copy("openapi.yaml"),
                .copy("openapi/rules-as-functions.yaml")
            ],
            plugins: [
                .plugin(name: "OpenAPIGenerator", package: "swift-openapi-generator")
            ]
        )
    ]
)
