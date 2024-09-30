# New York Times Technology News App

This is a single-page application that displays the latest technology news from the New York Times. The app fetches data from the New York Times Technology RSS feed and allows users to toggle between English and Spanish translations for the article titles and descriptions using the Google Translate API.

## Project Overview
- **Frontend**: Built using React, styled with CSS.
- **Backend**: A simple Flask server that fetches and serves the RSS feed data.
- **Language Toggle**: Switch between English and Spanish using the Google Cloud Translation API.
- **Live Date Display**: The current date is displayed at the top.
- **Clickable NYT Logo**: Clicking on the New York Times logo redirects to the main [New York Times](https://www.nytimes.com) homepage.

## Project Structure
```
nyt-rss-app/
├── backend/                # Flask backend folder
│   ├── server.py           # Main backend server script
│   └── requirements.txt    # Python dependencies for the backend
├── frontend/               # React frontend folder
│   ├── public/
│   │   └── nyt-logo.png    # The New York Times logo image
│   ├── src/
│   │   ├── App.js          # Main React component for the frontend
│   │   ├── App.css         # CSS for styling the application
│   │   └── index.js        # Entry point for the React application
│   └── package.json        # Node.js dependencies for the frontend
├── README.md
```

## Features
- **RSS Feed Integration**: Fetches technology news from the [New York Times Technology RSS Feed](https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml).
- **Language Toggle**: Toggle between English and Spanish for titles and descriptions.
- **Live Date Display**: Displays the current date at the top of the page.
- **Clickable New York Times Logo**: Clicking the New York Times logo redirects to the main [New York Times](https://www.nytimes.com) homepage.

## Prerequisites
- **Node.js**: Ensure that Node.js is installed on your system.
- **Python 3**: Required for the backend server.
- **Google Translate API Key**: Set up a Google Cloud project and enable the Translation API to obtain an API key. Refer to [Google Cloud Translation API](https://cloud.google.com/translate/docs/setup) for more information.

## Setup Instructions
### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/nyt-rss-app.git
cd nyt-rss-app
```

### 2. Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
   
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Activate the virtual environment
   pip install -r requirements.txt
   ```

3. Start the Flask server:
   ```bash
   python server.py
   ```
   The backend server will run on `http://localhost:5001`.

### 3. Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd ../frontend
   ```
   
2. Install React dependencies:
   ```bash
   npm install
   ```

3. Set up your environment variables:
   - Create a `.env` file in the `frontend` directory and add your Google Translate API key:
     ```
     REACT_APP_GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here
     ```

4. Start the React development server:
   ```bash
   npm start
   ```
   The frontend server will run on `http://localhost:3000`.

### 4. Verify the Application
1. Open your browser and navigate to `http://localhost:3000`.
2. Ensure that you can see the technology news articles and the layout matches the design.
3. Toggle the language between English and Spanish using the button at the top-right corner.

## Environment Variables
The following environment variables should be set in the `frontend/.env` file:

```
REACT_APP_GOOGLE_TRANSLATE_API_KEY=your_google_translate_api_key_here
```

> **Note**: Ensure that the `.env` file is not committed to version control by adding it to `.gitignore` if necessary.

## Project Structure and Files
### Backend (`backend/`)
- **`server.py`**: The main Flask backend server that fetches data from the RSS feed and optionally caches it.
- **`requirements.txt`**: Lists the Python dependencies needed for the backend.

### Frontend (`frontend/`)
- **`public/nyt-logo.png`**: The New York Times logo used in the header.
- **`src/App.js`**: The main React component that fetches data from the backend and displays it.
- **`src/App.css`**: Styles for the application, including the header, articles, and other UI components.
- **`src/index.js`**: The entry point for the React application.
- **`.env`**: Environment variables to store sensitive information like the Google Translate API key.

## Known Issues
- **Google Translate Quota**: Make sure you have sufficient quota for the Google Translate API, as this project translates text dynamically.
- **CORS Issues**: If you encounter CORS issues when the frontend makes requests to the backend, ensure that CORS is properly configured in `server.py`.

## Future Improvements
- Implement better caching mechanisms for translated content.
- Add additional languages for translation.
- Improve responsiveness for smaller screen sizes.
- Enhance error handling and loading states.

## License
This project is open-source and available under the [MIT License](LICENSE).

## Contact
For any questions or feedback, feel free to reach out!