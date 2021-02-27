import React, { useContext } from 'react';

import { ConnectionContext, ApiContext } from './AppContexts';

export default function Effects() {
  const [, setConnected] = useContext(ConnectionContext);

  // Общая яркость = MIN-MAX (def = 16-184)

  // Отключен N
  // Выбранный цвет  0-255 hue * 256 + 0-255 sat  [255]
  // Цвета по кругу N
  // Вертикальная радуга 0 32  [20]
  // Горизонтальная радуга 0 32   [20]
  // Матрица  150-5   [40]
  // Вспышки  1-32    [4]
  // Светлячки  1-16   [5]
  // Огонь  0/1   [1]
  // Плазма  5-50   [10]

  return <p>Эффекты</p>;
}
