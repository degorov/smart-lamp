export default async function savesettings(fetcher, ssid, password, timezone, maxbrightness, ip) {
  try {
    const json = await fetcher(ip, {
      action: 'savesettings',
      ssid,
      password,
      timezone,
      maxbrightness,
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
