import reflex as rx

config = rx.Config(
    app_name="reflex_react_github_calendar_demo",
    plugins=[
        rx.plugins.SitemapPlugin(),
        rx.plugins.TailwindV4Plugin(),
    ],
)
