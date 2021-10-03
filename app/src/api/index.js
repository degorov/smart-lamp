import { Capacitor } from '@capacitor/core';
import { Http } from '@capacitor-community/http';

import ping from './ping';
import geteffects from './geteffects';
import setbrightness from './setbrightness';
import seteffect from './seteffect';
import getsettings from './getsettings';
import savesettings from './savesettings';
import getalarm from './getalarm';
import savealarm from './savealarm';

const TIMEOUT = 5000;
const LOADING = 500;

const FUNCTIONS = {
  ping,
  geteffects,
  setbrightness,
  seteffect,
  getsettings,
  savesettings,
  getalarm,
  savealarm,
};

export default function Api(showLoader, storageIp) {
  const fetcher = async (ip = storageIp(), payload) => {
    if (Capacitor.isNativePlatform()) {
      const loading = setTimeout(() => showLoader(true), LOADING);
      try {
        const result = await Http.post({
          url: `http://${ip}/`,
          headers: { 'Content-Type': 'application/json' },
          connectTimeout: TIMEOUT,
          readTimeout: TIMEOUT,
          data: payload,
        });
        return result.data;
      } finally {
        clearTimeout(loading);
        showLoader(false);
      }
    } else {
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), TIMEOUT);
      const loading = setTimeout(() => showLoader(true), LOADING);
      try {
        const response = await fetch(`http://${ip}/`, {
          signal: controller.signal,
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(payload),
        });
        return await response.json();
      } finally {
        clearTimeout(timeout);
        clearTimeout(loading);
        showLoader(false);
      }
    }
  };

  // Using FUNCTIONS Object instead of Array because minification in production ruins fn.name
  return Object.fromEntries(
    Object.entries(FUNCTIONS).map(([fnname, fn]) => [fnname, fn.bind(null, fetcher)]),
  );
}
