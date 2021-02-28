export default async function getsettings(fetcher, ip) {
  try {
    const json = await fetcher(ip, { action: 'getsettings' });
    if (json.error === 'OK') {
      return {
        ssid: json.ssid,
        password: json.password,
        timezone: +json.timezone,
        maxbrightness: +json.maxbrightness,
      };
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}
