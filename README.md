# Hotel Mahajan International - Guest ID Management System

This is a secure Flask-based web application designed for hotel staff to manage guest check-ins by uploading identification documents (IDs). It features OCR (Optical Character Recognition) to extract text from uploaded images, stores guest data in MongoDB, provides a viewing interface for registered guests grouped by room, and includes access logging for security. The application supports HTTPS via self-signed SSL certificates and requires authentication for access.

## Features

- **Secure Authentication**: Login system with configurable username and password via environment variables.
- **ID Upload and OCR**: Upload multiple ID images per guest, extract text using Tesseract OCR, and store images and metadata in MongoDB.
- **Guest Viewing**: Display guests sorted by check-in date (descending) and then by room (ascending), grouped by room for easy management. Images are displayed as base64-encoded previews.
- **Access Logging**: Automatically logs all non-static requests (path, method, IP, user agent, timestamp) to MongoDB.
- **SSL Support**: Runs with HTTPS using self-signed certificates (auto-generated if missing).
- **Responsive UI**: Glassmorphism-style interface with background images for a modern hotel-themed look.
- **Logout Functionality**: Secure session management with flash messages for user feedback.

## Prerequisites

- Python 3.8+ 
- MongoDB (local instance running on `localhost:27017`)
- Tesseract OCR (installed system-wide; e.g., via Homebrew on macOS: `brew install tesseract`)
- ImageMagick (optional, for better OCR support)

## Installation

1. Clone or download the project to your local directory.
2. Create and activate a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install Python dependencies:
   ```
   pip install flask pymongo pytesseract pillow
   ```
   Note: `cryptography` may be needed for SSL certificate generation if not already installed: `pip install cryptography`.

4. Ensure MongoDB is running locally on the default port (27017).

## Configuration

Set environment variables for login credentials (optional; defaults provided):
```
export LOGIN_USERNAME=your_username
export LOGIN_PASSWORD=your_password
```

The application connects to a local MongoDB instance and uses two collections:
- `guests`: Stores guest ID data (room, date, image binary, mimetype, extracted text, upload time).
- `access_logs`: Stores access events.

## Running the Application

1. Run the application:
   ```
   python app.py
   ```
   - It will attempt to start on port 5001 with SSL. If the port is in use, it falls back to 5000.
   - Self-signed SSL certificates (`ssl_cert.crt` and `ssl_cert.key`) are generated automatically if missing.

2. Access the app:
   - Open your browser and go to `https://localhost:5001` (or `https://localhost:5000` if on fallback port).
   - Accept the self-signed certificate warning.

## Usage

1. **Login**: Navigate to `/login` and enter your credentials.
2. **Upload Guest ID**:
   - On the main page (`/`), enter the room number, check-in date (defaults to today), and select one or more ID images.
   - Submit the form to upload. Images are processed with OCR, and data is stored in MongoDB.
3. **View Guests**: Click "View All Guests" (`/view`) to see a grid of guests grouped by room, with images and dates displayed.
4. **Access Logs**: Navigate to `/logs` to view a table of all access events (requires login).
5. **Logout**: Use the logout link to end the session.

Flash messages provide feedback for login/logout actions.

## Project Structure

- `app.py`: Main Flask application with routes for login, upload, view, logs, and logout. Handles OCR, MongoDB interactions, and SSL setup.
- `templates/`:
  - `index.html`: Upload form with room, date, and file inputs.
  - `login.html`: Authentication form.
  - `view.html`: Guest display grid, grouped by room.
  - `logs.html`: Table for access logs.
- `static/`:
  - Background images (e.g., `patrick-fischer-niGsD4QOBTo.jpg` for hotel-themed UI).
- `README.md`: This file.
- `TODO.md`: Task tracking.
- `.gitignore`: Ignores virtual env, certs, etc.
- SSL files (`ssl_cert.crt`, `ssl_cert.key`): Auto-generated for HTTPS.

## Contributing

Contributions are welcome! Please fork the repository, make your changes, and submit a pull request. Ensure code follows PEP 8 standards and includes tests if adding features.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details (or add one if missing).
