# Geometric
### Linux OS for phones

### Concept
A linux distro phone that you plug into your computer to send commands to. It shows the currect task in a GUI dashboard on supported commands (ollama, curl, etc), it also supports voice assistant etc. etc.
```mermaid
flowchart TD
    A[Phone] -->|USB| B(PC)
    B --> C{Phone shell on PC}
    C -->|Linux command| D[Command]
    D --> E[Draw UI and get terminal updates]
    E --> C
    C -->|Network download| A
```