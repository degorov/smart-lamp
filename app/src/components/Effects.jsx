import React, { useContext } from 'react';

import { ConnectionContext, ApiContext } from './AppContexts';

export default function Effects() {
  const [, setConnected] = useContext(ConnectionContext);

  // Отключен N
  // Выбранный цвет  0-255 hue * 256 + 0-255 sat
  // Цвета по кругу N
  // Матрица  150-5
  // Вспышки  1-32
  // Светлячки  1-16
  // Огонь  0/1
  // Плазма  5-50

  return <p>Эффекты</p>;
}
