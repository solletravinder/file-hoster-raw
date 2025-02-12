# File Hoster Raw

File Hoster Raw is a simple Flask application that allows you to create a folder and upload files. This README provides instructions on how to set up and use the application.

## Getting Started

### Prerequisites

- Ensure you have [Python](https://www.python.org/downloads/) installed on your machine.
- Install [Flask](https://flask.palletsprojects.com/) and other dependencies listed in the `requirements.txt` file.

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/file-hoster-raw.git
   cd file-hoster-raw
   ```

2. Create a virtual environment and activate it:

   ```bash
   python310 or python311 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:

   ```bash
   pip install -r requirements.txt --no-cache-dir
   ```

4. Copy the example environment configuration file and update it:

   ```bash
   cp example.env .env
   ```

   Edit the `.env` file to match your configuration settings.

### Usage

To start the Flask application, run:

```bash
flask run
```

This will launch the application, and you can begin uploading files to your designated folder.

### Configuration

The `.env` file contains configuration settings that you need to update according to your environment. Ensure all necessary variables are set correctly.

### Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

### License

This project is licensed under the GNU GENERAL PUBLIC LICENSE. See the [LICENSE](LICENSE) file for details.

### Contact

For any questions or issues, please contact [solletravinder@gmail.com](mailto:solletravinder@gmail.com).

