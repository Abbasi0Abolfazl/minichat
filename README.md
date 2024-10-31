# MiniChat

MiniChat is a simple chat server/client application built using Python's `multiprocessing` module, specifically utilizing `Listener` and `Client` for inter-process communication. This project serves as a lightweight chat solution that can run in a command-line interface (CLI) on both Windows and Linux systems.

## Features

- **Multi-threaded**: Runs the server and client in separate threads, allowing for simultaneous message handling and user input.
- **Authentication**: Uses a simple password mechanism to authenticate clients connecting to the server.
- **Cross-platform**: Tested on both Windows and Linux environments.
- **Clear Console**: Clears the console for a cleaner chat log display.

## Usage

To run the MiniChat application, you need to specify whether you want to start a server or connect as a client. The command-line arguments are as follows:

### Server

To start the chat server, use the following command:

```bash
python minichat.py -host host:port nickname password
```

### Client

To connect to an existing chat server, use the following command:

```bash
python minichat.py -connect host:port nickname password
```

### Example

1. **Start the server**:
   ```bash
   python minichat.py -host 127.0.0.1:5000 Alice secret
   ```

2. **Connect a client**:
   ```bash
   python minichat.py -connect 127.0.0.1:5000 Bob secret
   ```

### Exit

To exit the chat, press `CTRL+C`.

## License

This project is licensed under the ISC License. For more details, please refer to the [LICENSE.txt](https://github.com/shazbits/minichat/blob/master/LICENSE.txt).

