```mermaid
classDiagram
    App <|-- PasswordManager
    SlackChannel <|-- App
    App : +OAuth Token
    App : +App-Level Token
    class PasswordManager{
        + database import
        +join()
	+add()
        +get()
        +remove()
	+update()
    }
    class SlackChannel{
        + OAuth permissions
        + AppLevel authentication
    }
```
