import React, { useContext } from 'react';

import { ConnectedContext } from './AppContexts';

export default function Alarm() {
  const connected = useContext(ConnectedContext);

  return <p>Будильник {String(connected)}</p>;
}
