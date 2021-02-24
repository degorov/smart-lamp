import React, { useContext } from 'react';

import { ConnectionContext } from './AppContexts';

export default function Effects() {
  const [connected] = useContext(ConnectionContext);

  // Отключен
  // Случайные пиксели
  // Цвета по кругу

  // Выбранный цвет
  // Цифры
  // Матрица
  // Вспышки
  // Снег
  // Светлячки
  // Огонь
  // Плазма

  return <p>Эффекты {String(connected)}</p>;
}
