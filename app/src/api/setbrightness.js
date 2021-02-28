export default async function setbrightness(fetcher, value, ip) {
  try {
    const json = await fetcher(ip, { action: 'setbrightness', value });
    if (json.error === 'OK') {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}
