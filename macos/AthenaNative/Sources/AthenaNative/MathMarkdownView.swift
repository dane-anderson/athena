
import SwiftUI
import WebKit


private final class PassthroughWebView: WKWebView {

    override func scrollWheel(
        with event: NSEvent
    ) {
        nextResponder?.scrollWheel(
            with: event
        )
    }

    override func mouseDragged(
        with event: NSEvent
    ) {
        super.mouseDragged(
            with: event
        )

        _ = autoscroll(
            with: event
        )
    }
}




struct MathMarkdownView: View {

    let markdown: String

    @State
    private var contentHeight: CGFloat = 60


    var body: some View {

        MathWebView(
            markdown: markdown,
            contentHeight: $contentHeight
        )
        .frame(
            height: contentHeight
        )
    }
}


private struct MathWebView: NSViewRepresentable {

    let markdown: String

    @Binding
    var contentHeight: CGFloat


    func makeCoordinator() -> Coordinator {

        Coordinator(self)
    }


    func makeNSView(
        context: Context
    ) -> WKWebView {

        let configuration =
            WKWebViewConfiguration()

        configuration
            .userContentController
            .add(
                context.coordinator,
                name: "heightChanged"
            )

        let webView = PassthroughWebView(
            frame: .zero,
            configuration: configuration
        )

        webView.navigationDelegate =
            context.coordinator

        webView.setValue(
            false,
            forKey: "drawsBackground"
        )

        return webView
    }


    func updateNSView(
        _ webView: WKWebView,
        context: Context
    ) {

        context.coordinator.parent = self

        let html = buildHTML(
            markdown: markdown
        )

        guard
            context.coordinator.lastHTML
                != html
        else {
            return
        }

        context.coordinator.lastHTML =
            html

        webView.loadHTMLString(
            html,
            baseURL: nil
        )
    }


    static func dismantleNSView(
        _ nsView: WKWebView,
        coordinator: Coordinator
    ) {

        nsView.configuration
            .userContentController
            .removeScriptMessageHandler(
                forName: "heightChanged"
            )
    }


    private func buildHTML(
        markdown: String
    ) -> String {

        // Base64 keeps LaTeX backslashes completely intact.
        let encoded =
            Data(markdown.utf8)
                .base64EncodedString()

        return """
        <!DOCTYPE html>

        <html>

        <head>

        <meta
            name="viewport"
            content="width=device-width, initial-scale=1.0"
        >

        <link
            rel="stylesheet"
            href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css"
        >

        <script
            src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js">
        </script>

        <script
            src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js">
        </script>

        <script
            src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js">
        </script>


        <style>

        :root {
            color-scheme: light dark;
        }


        html,
        body {
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
        }


        body {
            font-family:
                -apple-system,
                BlinkMacSystemFont,
                "SF Pro Text",
                sans-serif;

            font-size: 14px;
            line-height: 1.55;

            color: #1d1d1f;

            padding:
                2px 2px 8px 2px;
        }


        @media (prefers-color-scheme: dark) {

            body {
                color: #f5f5f7;
            }

            code {
                background: #2c2c2e;
            }

            pre {
                background: #1c1c1e;
            }
        }


        h1,
        h2,
        h3,
        h4 {
            margin:
                18px 0 8px 0;

            line-height: 1.25;
        }


        h1 {
            font-size: 23px;
        }


        h2 {
            font-size: 20px;
        }


        h3 {
            font-size: 17px;
        }


        p {
            margin:
                0 0 12px 0;
        }


        ul,
        ol {
            margin:
                8px 0 12px 22px;

            padding: 0;
        }


        li {
            margin:
                4px 0;
        }


        code {
            font-family:
                ui-monospace,
                SFMono-Regular,
                Menlo,
                monospace;

            background: #f2f2f2;

            padding:
                2px 5px;

            border-radius:
                5px;
        }


        pre {
            font-family:
                ui-monospace,
                SFMono-Regular,
                Menlo,
                monospace;

            background: #f5f5f5;

            padding:
                12px;

            border-radius:
                8px;

            white-space: pre-wrap;
        }


        pre code {
            background: transparent;
            padding: 0;
        }


        .katex-display {
            margin:
                16px 0;

            overflow-x: auto;
            overflow-y: hidden;
        }


        .katex {
            font-size: 1.10em;
        }

        </style>

        </head>


        <body>

        <div id="content"></div>


        <script>

        const encoded = "\(encoded)";

        const binary =
            atob(encoded);

        const bytes =
            Uint8Array.from(
                binary,
                character =>
                    character.charCodeAt(0)
            );

        const source =
            new TextDecoder("utf-8")
                .decode(bytes);


        const content =
            document.getElementById(
                "content"
            );


        // First render Markdown.
        content.innerHTML =
            marked.parse(
                source,
                {
                    gfm: true,
                    breaks: true
                }
            );


        // Then render all LaTeX math.
        renderMathInElement(
            content,
            {
                delimiters: [
                    {
                        left: "$$",
                        right: "$$",
                        display: true
                    },
                    {
                        left: "\\\\[",
                        right: "\\\\]",
                        display: true
                    },
                    {
                        left: "$",
                        right: "$",
                        display: false
                    },
                    {
                        left: "\\\\(",
                        right: "\\\\)",
                        display: false
                    }
                ],

                throwOnError: false,

                ignoredTags: [
                    "script",
                    "noscript",
                    "style",
                    "textarea",
                    "pre",
                    "code"
                ]
            }
        );


        function reportHeight() {

            const height =
                Math.ceil(
                    document.documentElement
                        .scrollHeight
                );

            window.webkit
                .messageHandlers
                .heightChanged
                .postMessage(height);
        }


        // Recalculate when the content lays itself out.
        const observer =
            new ResizeObserver(
                reportHeight
            );

        observer.observe(
            document.body
        );


        requestAnimationFrame(
            reportHeight
        );

        setTimeout(
            reportHeight,
            100
        );

        setTimeout(
            reportHeight,
            500
        );

        </script>

        </body>

        </html>
        """
    }


    final class Coordinator:
        NSObject,
        WKNavigationDelegate,
        WKScriptMessageHandler {

        var parent: MathWebView

        var lastHTML: String?


        init(
            _ parent: MathWebView
        ) {

            self.parent = parent
        }


        func userContentController(
            _ userContentController:
                WKUserContentController,
            didReceive message:
                WKScriptMessage
        ) {

            guard
                message.name
                    == "heightChanged"
            else {
                return
            }


            guard
                let number =
                    message.body as? NSNumber
            else {
                return
            }


            let newHeight =
                CGFloat(
                    truncating: number
                )


            DispatchQueue.main.async {

                self.parent
                    .contentHeight =
                    max(
                        50,
                        newHeight + 2
                    )
            }
        }
    }
}