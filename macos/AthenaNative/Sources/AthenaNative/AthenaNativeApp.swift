import SwiftUI
import AppKit
import Foundation


enum MessageRole {
    case user
    case athena
}


struct ChatMessage: Identifiable {
    let id = UUID()
    let role: MessageRole
    let text: String
}


struct AthenaBridge {

    static let projectPath =
        "/Users/daneanderson/Desktop/Projects/Athena Core"

    static func ollamaIsRunning() -> Bool {

        let process = Process()
        let output = Pipe()

        process.executableURL =
            URL(fileURLWithPath: "/usr/bin/curl")

        process.arguments = [
            "-s",
            "--max-time",
            "1",
            "http://127.0.0.1:11434/api/tags"
        ]

        process.standardOutput = output
        process.standardError = Pipe()

        do {
            try process.run()
            process.waitUntilExit()

            return process.terminationStatus == 0

        } catch {
            return false
        }
    }


    static func ensureOllama() {

        if ollamaIsRunning() {
            return
        }

        let process = Process()

        process.executableURL =
            URL(fileURLWithPath: "/usr/bin/open")

        process.arguments = [
            "-g",
            "-a",
            "Ollama"
        ]

        do {
            try process.run()
            process.waitUntilExit()
        } catch {
            return
        }

        for _ in 0..<20 {

            if ollamaIsRunning() {
                return
            }

            Thread.sleep(
                forTimeInterval: 0.25
            )
        }
    }


    static func run(
        _ prompt: String
    ) -> String {

        ensureOllama()

        let pythonPath =
            "\(projectPath)/.venv/bin/python"

        let process = Process()

        process.executableURL =
            URL(fileURLWithPath: pythonPath)

        process.currentDirectoryURL =
            URL(fileURLWithPath: projectPath)

        process.arguments = [
            "-c",
            """
            import os
            from core.orchestrator import process_request

            message = os.environ["ATHENA_USER_MESSAGE"]
            result = process_request(message)

            print(result)
            """
        ]

        var environment =
            ProcessInfo.processInfo.environment

        environment["ATHENA_USER_MESSAGE"] =
            prompt

        process.environment = environment

        let outputPipe = Pipe()
        let errorPipe = Pipe()

        process.standardOutput = outputPipe
        process.standardError = errorPipe

        do {

            try process.run()
            process.waitUntilExit()

            let outputData =
                outputPipe
                    .fileHandleForReading
                    .readDataToEndOfFile()

            let errorData =
                errorPipe
                    .fileHandleForReading
                    .readDataToEndOfFile()

            let output =
                String(
                    data: outputData,
                    encoding: .utf8
                ) ?? ""

            let error =
                String(
                    data: errorData,
                    encoding: .utf8
                ) ?? ""

            if process.terminationStatus != 0 {

                return """
                Athena encountered an error.

                \(error.isEmpty ? output : error)
                """
            }

            if output.trimmingCharacters(
                in: .whitespacesAndNewlines
            ).isEmpty {

                return """
                Athena completed the request but
                returned no visible response.
                """
            }

            return output.trimmingCharacters(
                in: .whitespacesAndNewlines
            )

        } catch {

            return """
            Athena could not start the local engine.

            \(error.localizedDescription)
            """
        }
    }
}


@MainActor
final class ChatModel: ObservableObject {

    @Published var messages: [ChatMessage] = []

    @Published var prompt = ""

    @Published var isRunning = false


    func newChat() {

        guard !isRunning else {
            return
        }

        messages.removeAll()
        prompt = ""
    }


    func send() {

        let text =
            prompt.trimmingCharacters(
                in: .whitespacesAndNewlines
            )

        guard
            !text.isEmpty,
            !isRunning
        else {
            return
        }

        messages.append(
            ChatMessage(
                role: .user,
                text: text
            )
        )

        prompt = ""
        isRunning = true

        Task {

            let response =
                await Task.detached(
                    priority: .userInitiated
                ) {
                    AthenaBridge.run(text)
                }
                .value

            messages.append(
                ChatMessage(
                    role: .athena,
                    text: response
                )
            )

            isRunning = false
        }
    }
}


struct MessageView: View {

    let message: ChatMessage


    var body: some View {

        if message.role == .user {

            HStack(alignment: .top) {

                Spacer(minLength: 100)

                Text(message.text)
                    .font(.system(size: 14))
                    .textSelection(.enabled)
                    .padding(.horizontal, 16)
                    .padding(.vertical, 11)
                    .background(
                        Color.accentColor
                            .opacity(0.13)
                    )
                    .clipShape(
                        RoundedRectangle(
                            cornerRadius: 18,
                            style: .continuous
                        )
                    )
            }

        } else {

            HStack(
                alignment: .top,
                spacing: 14
            ) {

                ZStack {

                    Circle()
                        .fill(
                            Color.accentColor
                                .opacity(0.14)
                        )
                        .frame(
                            width: 34,
                            height: 34
                        )

                    Image(
                        systemName: "sparkles"
                    )
                    .font(
                        .system(
                            size: 15,
                            weight: .semibold
                        )
                    )
                    .foregroundStyle(
                        Color.accentColor
                    )
                }

                VStack(
                    alignment: .leading,
                    spacing: 8
                ) {

                    Text("Athena")
                        .font(
                            .system(
                                size: 13,
                                weight: .semibold
                            )
                        )

                    MathMarkdownView(
                        markdown: message.text
                    )
                    .frame(
                        maxWidth: .infinity,
                        minHeight: 50,
                        alignment: .leading
                    )    
                }

                Spacer(minLength: 60)
            }
        }
    }
}


struct SidebarView: View {

    @ObservedObject var model: ChatModel


    var body: some View {

        VStack(
            alignment: .leading,
            spacing: 14
        ) {

            HStack(spacing: 10) {

                Image(
                    systemName:
                        "sparkles.rectangle.stack.fill"
                )
                .font(.title2)
                .foregroundStyle(
                    Color.accentColor
                )

                Text("Athena")
                    .font(
                        .system(
                            size: 21,
                            weight: .semibold
                        )
                    )
            }
            .padding(.top, 12)


            Button {

                model.newChat()

            } label: {

                Label(
                    "New Chat",
                    systemImage:
                        "square.and.pencil"
                )
                .frame(
                    maxWidth: .infinity,
                    alignment: .leading
                )
            }
            .buttonStyle(.bordered)
            .disabled(model.isRunning)


            Divider()


            Text("ATHENA CORE")
                .font(
                    .system(
                        size: 10,
                        weight: .bold
                    )
                )
                .foregroundStyle(.secondary)


            Label(
                "Quant Research",
                systemImage: "chart.xyaxis.line"
            )
            .font(.system(size: 13))


            Label(
                "Local Models",
                systemImage: "cpu"
            )
            .font(.system(size: 13))


            Label(
                "Dane Engine",
                systemImage: "function"
            )
            .font(.system(size: 13))


            Spacer()


            HStack(spacing: 8) {

                Circle()
                    .fill(.green)
                    .frame(
                        width: 8,
                        height: 8
                    )

                Text("Local")
                    .font(
                        .system(
                            size: 12,
                            weight: .medium
                        )
                    )

                Spacer()
            }
            .foregroundStyle(.secondary)
            .padding(.bottom, 8)
        }
        .padding(.horizontal, 14)
        .frame(
            minWidth: 210,
            idealWidth: 235
        )
    }
}


struct ComposerView: View {

    @ObservedObject var model: ChatModel


    var body: some View {

        VStack(spacing: 8) {

            HStack(
                alignment: .bottom,
                spacing: 10
            ) {

                TextEditor(
                    text: $model.prompt
                )
                .font(
                    .system(size: 14)
                )
                .scrollContentBackground(
                    .hidden
                )
                .padding(8)
                .frame(
                    minHeight: 48,
                    maxHeight: 120
                )
                .background(
                    RoundedRectangle(
                        cornerRadius: 18,
                        style: .continuous
                    )
                    .fill(
                        Color(
                            nsColor:
                                .controlBackgroundColor
                        )
                    )
                )
                .overlay(
                    RoundedRectangle(
                        cornerRadius: 18,
                        style: .continuous
                    )
                    .stroke(
                        Color.secondary
                            .opacity(0.20),
                        lineWidth: 1
                    )
                )


                Button {

                    model.send()

                } label: {

                    Image(
                        systemName: "arrow.up"
                    )
                    .font(
                        .system(
                            size: 15,
                            weight: .bold
                        )
                    )
                    .frame(
                        width: 34,
                        height: 34
                    )
                }
                .buttonStyle(.borderedProminent)
                .clipShape(Circle())
                .disabled(
                    model.isRunning ||
                    model.prompt
                        .trimmingCharacters(
                            in:
                                .whitespacesAndNewlines
                        )
                        .isEmpty
                )
                .keyboardShortcut(
                    .return,
                    modifiers: [.command]
                )
            }


            Text(
                model.isRunning
                ? "Athena is researching…"
                : "⌘ Return to send"
            )
            .font(
                .system(size: 11)
            )
            .foregroundStyle(.secondary)
        }
        .padding(.horizontal, 28)
        .padding(.top, 14)
        .padding(.bottom, 16)
    }
}


struct ChatView: View {

    @ObservedObject var model: ChatModel


    var body: some View {

        VStack(spacing: 0) {

            ScrollViewReader { proxy in

                ScrollView {

                    if model.messages.isEmpty {

                        VStack(spacing: 16) {

                            Spacer()
                                .frame(height: 130)

                            Image(
                                systemName:
                                    "sparkles.rectangle.stack.fill"
                            )
                            .font(
                                .system(size: 42)
                            )
                            .foregroundStyle(
                                Color.accentColor
                            )

                            Text(
                                "What can Athena research?"
                            )
                            .font(
                                .system(
                                    size: 25,
                                    weight: .semibold
                                )
                            )

                            Text(
                                """
                                Ask naturally. Athena will interpret the request,
                                run the appropriate local research workflow,
                                and return the completed analysis here.
                                """
                            )
                            .font(.system(size: 14))
                            .foregroundStyle(
                                .secondary
                            )
                            .multilineTextAlignment(
                                .center
                            )
                            .frame(maxWidth: 520)

                        }
                        .frame(
                            maxWidth: .infinity
                        )

                    } else {

                        LazyVStack(
                            spacing: 28
                        ) {

                            ForEach(
                                model.messages
                            ) { message in

                                MessageView(
                                    message: message
                                )
                                .id(message.id)
                            }


                            if model.isRunning {

                                HStack(
                                    spacing: 10
                                ) {

                                    ProgressView()
                                        .controlSize(
                                            .small
                                        )

                                    Text(
                                        "Athena is researching…"
                                    )
                                    .font(
                                        .system(
                                            size: 13
                                        )
                                    )
                                    .foregroundStyle(
                                        .secondary
                                    )

                                    Spacer()
                                }
                            }
                        }
                        .padding(
                            .horizontal,
                            34
                        )
                        .padding(
                            .vertical,
                            28
                        )
                        .frame(
                            maxWidth: 900
                        )
                        .frame(
                            maxWidth: .infinity
                        )
                    }
                }
                .onChange(
                    of: model.messages.count
                ) { _ in

                    if let last =
                        model.messages.last {

                        withAnimation {

                            proxy.scrollTo(
                                last.id,
                                anchor: .bottom
                            )
                        }
                    }
                }
            }


            Divider()

            ComposerView(
                model: model
            )
        }
        .background(
            Color(
                nsColor:
                    .windowBackgroundColor
            )
        )
    }
}


struct ContentView: View {

    @StateObject
    private var model = ChatModel()


    var body: some View {

        NavigationSplitView {

            SidebarView(
                model: model
            )

        } detail: {

            ChatView(
                model: model
            )
        }
        .frame(
            minWidth: 950,
            minHeight: 650
        )
    }
}


@main
struct AthenaNativeApp: App {

    var body: some Scene {

        WindowGroup("Athena") {

            ContentView()
        }
        .windowStyle(.titleBar)
        .windowToolbarStyle(.unified)
    }
}
