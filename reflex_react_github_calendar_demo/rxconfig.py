import reflex as rx

config = rx.Config(
    app_name="reflex_react_github_calendar_demo",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
        # Reflex 0.9+ requires Radix Themes to be enabled explicitly.
        rx.plugins.RadixThemesPlugin(),
    ],
)
