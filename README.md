# cli_for_gemini

Command Line Interface for using Gemini AI
Here’s a README template you can use for your GitHub repository. It covers the basics of using the CLI on different operating systems and includes contribution guidelines.

---

# Gemini CLI

## About the Project

The **Gemini CLI** is a command-line interface tool designed for interacting with the Gemini API. It allows users to set an API key, ask questions, and reset the API key. The CLI supports both command-based and interactive modes, making it versatile for various use cases.

## Installation

### Windows

1. **Download the Executable:**

   - Download the `gemini-cli.exe` file from the [releases section](link-to-releases).

2. **Running the Executable:**
   - Double-click the `gemini-cli.exe` file to run it in interactive mode.
   - To use commands, open Command Prompt or PowerShell and run:
     ```
     gemini-cli.exe <command>
     ```
3. **Compile Your Own Executable:**
   - If you prefer to compile your own executable, clone the repository, navigate to the src directory, and run the following command:
   ```bash
   pyinstaller --onefile --name gemini-cli --add-data "config.json;." cli_script.py
   ```

### Linux and macOS

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo/src
   ```

2. **Create a Virtual Environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Running the CLI:**
   - To run in interactive mode:
     ```bash
     python cli_script.py
     ```
   - To use commands:
     ```bash
     python cli_script.py <command>
     ```

## Commands

- **setkey**: Set the Gemini API key. You will be prompted to enter your API key.
- **ask**: Enter interactive mode to ask questions using the Gemini API.
- **resetkey**: Reset the Gemini API key by removing it from the configuration.
- **help**: Show help information.

## Contribution

We welcome contributions to improve the Gemini CLI. To contribute:

1. **Fork the Repository:**

   - Click on the "Fork" button at the top-right of this page.

2. **Clone Your Fork:**

   ```bash
   git clone https://github.com/yourusername/your-fork.git
   ```

3. **Create a New Branch:**

   ```bash
   git checkout -b feature/your-feature
   ```

4. **Make Changes and Commit:**

   - Describe your changes clearly in your commit messages.

5. **Push Your Changes:**

   ```bash
   git push origin feature/your-feature
   ```

6. **Create a Pull Request:**
   - Go to the original repository and click on "New Pull Request."

### Guidelines

- **Code Style:** Follow the existing code style of the project.
- **Documentation:** Ensure that any new features or changes are well-documented.
- **Testing:** Add or update tests as necessary.

## License

This project is licensed under the GNU GENERAL PUBLIC License - see the [LICENSE](LICENSE) file for details.

---
