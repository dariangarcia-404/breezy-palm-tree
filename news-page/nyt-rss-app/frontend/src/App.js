import React, { useEffect, useState } from 'react';
import axios from 'axios';
import './App.css';
import config from './config';

const GOOGLE_TRANSLATE_API_KEY = process.env.REACT_APP_GOOGLE_TRANSLATE_API_KEY;

const App = () => {
  const [articles, setArticles] = useState([]);
  const [originalArticles, setOriginalArticles] = useState([]);
  const [language, setLanguage] = useState('ENG'); // Default language

  // Get the current date for display
  const todayDate = new Date().toLocaleDateString('en-US', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });

  useEffect(() => {
    axios
      .get(`${config.BACKEND_URL}/rss`)
      .then((response) => {
        setArticles(response.data.items);
        setOriginalArticles(response.data.items); // Store original articles for English
      })
      .catch((error) => console.error('Error fetching RSS feed:', error));
  }, []);

  // Translate the content using Google Translate API
  const translateContent = async (text, targetLanguage) => {
    try {
      const response = await axios.post(
        `https://translation.googleapis.com/language/translate/v2`,
        {},
        {
          params: {
            q: text,
            target: targetLanguage,
            key: GOOGLE_TRANSLATE_API_KEY,
          },
        }
      );
      return response.data.data.translations[0].translatedText;
    } catch (error) {
      console.error('Error translating text:', error);
      return text;
    }
  };

  const changeLanguage = async () => {
    const targetLanguage = language === 'ENG' ? 'es' : 'en';
    if (targetLanguage === 'es') {
      const translatedArticles = await Promise.all(
        originalArticles.map(async (article) => {
          const translatedTitle = await translateContent(article.title, targetLanguage);
          const translatedDescription = await translateContent(article.description, targetLanguage);
          return { ...article, title: translatedTitle, description: translatedDescription };
        })
      );
      setArticles(translatedArticles);
    } else {
      setArticles(originalArticles);
    }
    setLanguage(language === 'ENG' ? 'ESP' : 'ENG');
  };

  return (
    <div className="App">
      <header className="header">
        <div className="header-content">
          <span className="date">{todayDate}</span>
          {/* Make the NYT logo clickable by wrapping it in an anchor tag */}
          <a href="https://www.nytimes.com" target="_blank" rel="noopener noreferrer">
            <img src="/nyt-logo.png" alt="The New York Times" className="nyt-logo" />
          </a>
          <button onClick={changeLanguage} className="lang-toggle">
            {language === 'ENG' ? 'ESP' : 'ENG'}
          </button>
        </div>
      </header>

      <div className="articles">
        {articles.map((article, index) => (
          <div key={index} className="article">
            <img src={article.image || 'https://via.placeholder.com/150'} alt="Article" />
            <div className="article-content">
              <h2>
                <a href={article.link} target="_blank" rel="noopener noreferrer">
                  {article.title}
                </a>
              </h2>
              <p>{article.description}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default App;
