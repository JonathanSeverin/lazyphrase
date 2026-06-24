A lightweight text expansion tool for Linux.
This project allows you to define custom hotkeys (e.g. Alt+Q) that trigger text snippets. When activated, the program will either insert a predefined phrase directly into the active application or display a list of available snippets to choose from.
The project is designed as a learning-focused system-level application, exploring global keyboard input handling, event-driven programming, and interaction with the operating system.

⚠️ Note:
This project currently targets Linux with X11.
Due to security restrictions in Wayland, global keyboard listeners (required for hotkeys and text expansion) are not supported in a straightforward way.