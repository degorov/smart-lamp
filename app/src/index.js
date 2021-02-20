import '@fontsource/roboto/300.css';
import '@fontsource/roboto/400.css';
import '@fontsource/roboto/500.css';
import '@fontsource/roboto/700.css';

import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';

var mountNode = document.getElementById('app');
ReactDOM.render(<App name="Lamp" />, mountNode);
