import { createContext } from 'react';

const ConnectionContext = createContext();
ConnectionContext.displayName = 'ConnectionContext';

const ApiContext = createContext();
ApiContext.displayName = 'ApiContext';

export { ConnectionContext, ApiContext };
