export default async function savealarm(fetcher, enabled, repeat, time, before, after, ip) {
  try {
    const json = await fetcher(ip, {
      action: 'savealarm',
      enabled: +enabled,
      repeat,
      time,
      before,
      after,
    });
    if (json.error === 'OK') {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}
