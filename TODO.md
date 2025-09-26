# Project Construction Guide: Hotel Mahajan International Guest ID Management System

This TODO list outlines the step-by-step construction of the Flask-based hotel guest ID management system from scratch. It covers setting up the project structure, implementing features, and ensuring security. Each item includes implementation details for clarity.

## Project Setup and Structure
- [x] Initialize Flask project with basic app.py structure
- [x] Create templates/ directory with base HTML files (login.html, index.html, view.html, logs.html)
- [x] Create static/ directory for background images and CSS
- [x] Set up MongoDB connection and define collections (guests, access_logs)
- [x] Configure SSL support with self-signed certificate generation

## Authentication System
- [x] Implement session-based login/logout with flash messages
- [x] Add environment variable support for configurable username/password
- [x] Create login.html template with form for username/password input
- [x] Add @app.before_request decorator to enforce authentication on protected routes

## ID Upload and OCR Processing
- [x] Create upload form in index.html with fields for room, date, and multiple file uploads
- [x] Implement /upload route to handle POST requests with file processing
- [x] Integrate Tesseract OCR for text extraction from uploaded images
- [x] Store processed data (image binary, mimetype, extracted text, metadata) in MongoDB guests collection
- [x] Handle image conversion to RGB and error handling for unsupported formats

## Guest Viewing Interface
- [x] Implement /view route to retrieve and display guests from database
- [x] Sort guests by date (descending) then room (ascending)
- [x] Group guests by room for organized display in view.html
- [x] Convert stored image binaries to base64 for inline display in templates
- [x] Add timezone conversion for upload timestamps (UTC to local time)

## Access Logging
- [x] Add @app.before_request logging for all non-static requests
- [x] Store log data (path, method, IP, user agent, timestamp) in access_logs collection
- [x] Create /logs route and logs.html template to display logs in a table format
- [x] Include startup event logging on app initialization

## UI/UX Enhancements
- [x] Apply glassmorphism styling with backdrop blur and transparency
- [x] Set background images from static/ directory
- [x] Ensure responsive design for upload forms and guest grids
- [x] Add navigation links between pages (upload, view, logout)

## Security and Configuration
- [x] Implement HTTPS with SSL context and port fallback (5001 -> 5000)
- [x] Add .gitignore for virtual environment, certificates, and sensitive files
- [x] Configure session secret key using os.urandom for security
- [x] Validate file uploads and limit to image types

## Documentation
- [x] Write comprehensive README.md with project description, features, prerequisites, installation, configuration, usage, and structure
- [x] Remove sensitive default credentials from documentation to prevent exposure in version control

## Testing and Deployment
- [ ] Test all routes and functionality (login, upload, OCR accuracy, viewing, logging)
- [ ] Verify MongoDB data persistence and retrieval
- [ ] Ensure SSL certificate generation and HTTPS access
- [ ] Deploy to production environment with proper SSL certificates and environment variables
