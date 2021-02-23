import React, { useContext } from 'react';

import { ConnectedContext } from './AppContexts';

export default function Effects() {
  const connected = useContext(ConnectedContext);

  return <p>Эффекты {String(connected)}</p>;
}
