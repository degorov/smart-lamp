export default async function ping(fetcher, ip) {
  try {
    const json = await fetcher(ip, { action: 'ping' });
    if (json.error === 'OK') {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}
