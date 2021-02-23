export default async function ping(ip) {
  try {
    const response = await window.fetchWithLoading(`http://${ip}/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ action: 'ping' }),
    });
    const data = await response.json();

    if (data.error === 'OK') {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    return false;
  }
}
