// swift-tools-version: 6.0
import PackageDescription

let package = Package(
    name: "RulesKit",
    platforms: [.macOS(.v13), .iOS(.v16)],
    products: [
        .library(name: "RulesKit", targets: ["RulesKit"]),
    ],
    dependencies: [
        .package(url: "https://github.com/apple/swift-openapi-generator", from: "1.5.0")
    ],
    targets: [
        .target(
            name: "RulesKit",
            resources: [
                .copy("openapi/rules-as-functions.yaml")
            ],
            plugins: [
                .plugin(name: "OpenAPIGenerator", package: "swift-openapi-generator")
            ]
        )
    ]
)
