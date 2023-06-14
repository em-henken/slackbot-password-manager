```mermaid
sequenceDiagram
    Slack User->>+Billiken Bot: /translate spanish Hi, how are you?
    Billiken Bot->>+googletrans Library: translate from detected language to spanish Hi, how are you?
    googletrans Library-->>-Billiken Bot: ¿Hola, cómo estás?
    Billiken Bot-->>-Slack User: 
    Slack User->>+Slack Channel: ¿Hola, cómo estás?
```
